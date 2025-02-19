import json

from pyspark.sql import SparkSession
from pyspark.sql.functions import pandas_udf, col, regexp_replace
from pyspark.sql.types import StringType, IntegerType
import google.generativeai as genai
import pandas as pd
from functools import reduce
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, FloatType
from pyspark.sql.functions import regexp_extract
from sentence_transformers import SentenceTransformer
import pymongo

# Initialize Spark Session
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


# Define a Pandas UDF (Pass API Key as an Argument)
@pandas_udf(StringType())
def extract_resume_details(resume_series: pd.Series) -> pd.Series:
    responses = []
    for resume_text in resume_series:
        # input_prompt = f"""
        #     I will provide you with the text content of a resume. Your task is to extract the following important details from it:
        #     Skills, Total Experience, College Name, Degree, Designation, Company Names.
        #     Please return the extracted information, remove duplicate skills but keep important information.
        #     Resume Text: {resume_text}"""

        input_prompt = f"""You are an expert in IT and Computer Science job roles. Your task is to extract the following key details from the provided resume text: Skills, Total Experience, College Name, Degree, Designation, Company Names and category. And categorize the given resume or job description into one of the ten broad categories based on its content. Choose only one category that best represents the overall role. Categories: {categories}. Assign the most relevant category. Do not provide multiple categories. Please remove duplicate skills, but retain important information. Return the extracted details in dictionary without back quotes. Ensure the dictionary output includes the exact keys: skills, total_experience, college_name, degree, designation, company_names, and category without any additional keywords and back quotes. Resume Text: {resume_text}"""

        # Pass API key as a function argument
        response = get_gemini_response(my_api_key, input_prompt)
        response = response.strip('`')
        responses.append(response)

    return pd.Series(responses)

# Load the embedding model (you can use any model like 'all-MiniLM-L6-v2')
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Define a UDF to generate embeddings
def get_embedding(text):
    if text:  # Ensure text is not None or empty
        return embedding_model.encode(text).tolist()
    return None

# Function to process resumes

def extract_id(filepath):
    """Extracts the ID from the filepath using os.path.basename() and split()."""
    import os
    try:
        filename = os.path.basename(filepath)
        id_str = filename.split(".")[0]
        return int(id_str)  # Convert to integer
    except (ValueError, AttributeError, TypeError):  # Handle potential errors
        return None  # Or return a default value, or raise an exception if you want stricter error handling

def add_metadata_to_json(json_string, file_path, id_val, embedding):
    """Adds file_path, id, and embedding to the JSON string."""
    try:
        data = json.loads(json_string)  # Parse the JSON string
        data["file_path"] = file_path  # Add file_path
        data["_id"] = id_val  # Add id
        data["embedding"] = embedding  # Add embedding
        return json.dumps(data)  # Convert back to JSON string
    except (json.JSONDecodeError, TypeError):  # Handle errors
        return None  # Or handle errors as you see fit (e.g., return original string, raise exception)

def reduce_resume_content():
    directory = "hdfs://localhost:9000/user/project/temp_resumes/*.txt"

    # Read resumes from HDFS
    df = spark.sparkContext.wholeTextFiles(directory).toDF(["file_path", "content"])
    # df = df.select("content")
    # df.show(truncate=False)
    # print("Processing resumes...")

    # Register the function as a UDF (User-Defined Function)
    extract_id_udf = udf(extract_id, IntegerType())  # Specify the return type (IntegerType)

    # Assuming 'df' is your PySpark DataFrame with a 'file_path' column
    df_with_id = df.withColumn("id", extract_id_udf("file_path"))

    # Show the DataFrame with the new 'id' column
    # df_with_id.show()

    # Apply the Pandas UDF (Now the API key is directly passed)
    df_processed = df_with_id.withColumn("structured_info", extract_resume_details(col("content")))
    # df_processed.show(truncate=False)

    columns_to_clean = ["content", "structured_info"]
    df_cleaned = reduce(lambda df, col: df.withColumn(col, regexp_replace(col, "[\n\r]", " ")), columns_to_clean, df_processed)
    # df_cleaned.show(truncate=False)

    # Register UDF with Spark
    embedding_udf = udf(get_embedding, ArrayType(FloatType()))

    # Add embeddings to DataFrame
    df_with_embeddings = df_cleaned.withColumn("embedding", embedding_udf(df_cleaned["structured_info"]))

    # Show results
    # df_with_embeddings.show(truncate=False)

    # Register the function as a UDF
    add_metadata_udf = udf(add_metadata_to_json, StringType())

    # Apply the UDF to the DataFrame
    df_updated = df_with_embeddings.withColumn(
        "updated_structured_info",
        add_metadata_udf("structured_info", "file_path", "id", "embedding")
    )
    df_updated.show(truncate=False)
    # json_data_list = df_updated.select("structured_info").rdd.map(lambda row: json.loads(row[0])).collect()
    json_data_list = df_updated.select("updated_structured_info").rdd.map(
        lambda row: json.loads(str(row[0]))).collect()

    # MongoDB connection setup
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")  # Replace with your MongoDB URI
    db = client["project"]  # Replace with your database name
    collection = db["resumes"]  # Replace with your collection name

    # Insert data into MongoDB
    collection.insert_many(json_data_list)

    print("Data inserted successfully into MongoDB!")


# Run the function
reduce_resume_content()
spark.stop()