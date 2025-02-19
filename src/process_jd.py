# Initialize Spark Session
import json

import pymongo
from hdfs import InsecureClient
from pyspark.sql import SparkSession
import google.generativeai as genai
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import kafka_consumer_jd as kjd
spark = SparkSession.builder.appName("ReduceResumeContent").getOrCreate()

# Set API key
my_api_key = "AIzaSyAd-lL3B-Hi34Qr9pkfOdOefd_EJF09Wio"
categories = ["Software Development & Engineering", "Data Science & Machine Learning", "Cloud & DevOps", "Cybersecurity", "Networking & IT Support", "Networking & IT Support", "Database & Big Data", "Embedded Systems & IoT", "Game Development", "Software Testing & Quality Assurance", "IT Project Management & Business Analysis"]

# Function to call Gemini API
def get_gemini_response(api_key, input_text):
    try:
        genai.configure(api_key=api_key)  # Set API key inside function
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input_text)
        return response.text if response else "Error: No response"
    except Exception as e:
        return f"Error: {str(e)}"

def extract_jd_details(job_description):
    input_prompt = f"""
    You are an expert in IT and Computer Science job roles. Your task is to extract key details from the provided job description and categorize it into one of ten broad categories.

    Categories:
    1. Software Development & Engineering
    2. Data Science & Machine Learning
    3. Cloud & DevOps
    4. Cybersecurity
    5. Networking & IT Support
    6. Database & Big Data
    7. Embedded Systems & IoT
    8. Game Development
    9. Software Testing & Quality Assurance
    10. IT Project Management & Business Analysis

    Extract the following details:
    - Skills (List of required skills, removing duplicates)
    - Total Experience (Minimum years of experience required)
    - Degree (Required education qualification)
    - Designation (Job title)
    - Company Name (If mentioned)
    - Category (Best matching category from the given list)

    Assign the most relevant category. Do not provide multiple categories.

    Job Description: {job_description}

    Return the extracted details in dictionary format without backticks:
    """

    # Pass API key as a function argument
    response = get_gemini_response(my_api_key, input_prompt)
    response = response.strip('`')
    return response

# Load the embedding model (you can use any model like 'all-MiniLM-L6-v2')
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Define a UDF to generate embeddings
def get_embedding(text):
    if text:  # Ensure text is not None or empty
        return embedding_model.encode(text).tolist()
        #Single sentence: (384,)
    return None

def process_jd():
    print("inside pjd")
    jd = kjd.process_job_description()
    short_jd = extract_jd_details(jd)

    print(short_jd)

    jd_embedding = get_embedding(short_jd)
    print(jd_embedding)

    jd_obj = json.loads(short_jd)
    jd_category = jd_obj['Category']

    client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")  # Replace with your MongoDB URI
    db = client["project"]  # Replace with your database name
    collection = db["resumes"]  # Replace with your collection name

    # Insert data into MongoDB
    result = collection.find(
        {'category': jd_category},  # Filter by category
        {'_id': 1, 'embedding': 1}  # Include only the 'embedding' field and exclude '_id'
    )
    resume_documents = []
    resume_embedding_list = []
    for doc in result:
        resume_documents.append(doc)
        resume_embedding_list.append(doc['embedding'])

    print(resume_documents)
    resume_embeddings = np.array(resume_embedding_list)
    jd_embedding = np.array(jd_embedding)

    if jd_embedding.ndim == 1:
        jd_embedding = jd_embedding.reshape(1, -1)

    # Build a Faiss index for the resume embeddings
    dimension = resume_embeddings.shape[1]  # Dimension of the embeddings (ensure all embeddings are the same shape)
    index = faiss.IndexFlatL2(dimension)  # L2 distance metric (Euclidean distance)
    index.add(resume_embeddings)  # Add resume embeddings to the index

    # Query the Faiss index with the job description embedding
    k = 2 # Number of most similar resumes to return
    distances, indices = index.search(jd_embedding, k)

    print(indices)
    print(indices[0])

    resumes_hdfs_path = []
    for idx in indices[0]:
        if idx == -1:
            break
        matched_result = resume_documents[idx]
        print(type(matched_result))
        matched_resume_id = matched_result['_id']
        resumes_hdfs_path_cursor = collection.find(
            {'_id': matched_resume_id},  # Filter by category
            {'file_path': 1}  # Include only the 'file_path' field and exclude '_id'
        )
        for path in resumes_hdfs_path_cursor:
            resumes_hdfs_path.append(path['file_path'])
    resume_content_list = []
    for hdfs_path in resumes_hdfs_path:
        df = spark.read.format("text").load(hdfs_path)
        file_content = df.rdd.map(lambda row: row.value).collect()

        resume_content_list.append("\n".join(file_content))
    return resume_content_list
