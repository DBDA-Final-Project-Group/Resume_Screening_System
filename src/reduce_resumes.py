from pyspark.sql.functions import pandas_udf, col

from Util import Util
import google.generativeai as genai
import os, configparser, time
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from pyspark import SparkContext
import pandas as pd

my_api_key = "AIzaSyAd-lL3B-Hi34Qr9pkfOdOefd_EJF09Wio"

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

spark = SparkSession.builder.appName("ReduceResumeContent").getOrCreate()

# hdfs_path = "hdfs://localhost:9000/user/project/temp_resumes/*.txt"

def extract_resume_details(resume_series: pd.Series) -> pd.Series:
    responses = []
    for resume_text in resume_series:
        # Prompt Template
        input_prompt = f"""
            I will provide you with the text content of a resume. Your task is to extract the following important details from it:
            Skills, Total Experience, College Name, Degree, Designation, Company Names
            Please return the extracted information, remove duplicate skills but keep important information.
            Resume Text: {resume_text}"""
        response = get_gemini_repsonse(input_prompt)
        print(response)
        responses.append(response)
    return pd.Series(responses)

# user defined function
extract_info_pandas_udf = pandas_udf(extract_resume_details, returnType=StringType())

def reduce_resume_content():
    genai.configure(api_key=my_api_key)

    # directory = '/home/piyush/Documents/dbda/project/ml/resumes_samples/'
    directory = 'hdfs://localhost:9000/user/project/temp_resumes/*.txt'

    # Define the path to the shortned resume folder
    # temp_dependent_folder = '/home/piyush/Documents/dbda/project/ml/temp_shortned_resumes/'
    dependent_folder = 'hdfs://localhost:9000/user/project/shrt_resumes'
    df = spark.read.text(directory)
    print("reduce_resume_called")
    df.show()
    # print(df.col('value'))
    # Apply LLM UDF to process resumes
    df_processed = df.withColumn("structured_info", extract_info_pandas_udf(col('value')))
    df_processed.show()
    # count = 0
    # for filename in os.listdir(directory):
    #     if count==10:
    #         print("waited")
    #         time.sleep(60)
    #         count=0
    #     else:
    #         if filename.endswith('.txt'):
    #             file_path = os.path.join(directory, filename)
    #             with open(file_path, 'r', encoding='utf-8') as file:
    #                 text = file.read()
    #                 # Prompt Template
    #                 input_prompt = f"""
    #                     I will provide you with the text content of a resume. Your task is to extract the following important details from it:
    #                     Skills, Total Experience, College Name, Degree, Designation, Company Names
    #                     Please return the extracted information, remove duplicate skills but keep important information.
    #                     Resume Text: {text}"""
    #                 response = get_gemini_repsonse(input_prompt)
    #
    #                 # new_file_name = filename.replace(".txt",".npy")
    #
    #                 # Create the full path for the new file
    #                 new_file_path = os.path.join(dependent_folder, filename)
    #                 with open(new_file_path, 'w') as file_writter:
    #                     # Write some content to the file
    #                     file_writter.write(response)
    #             count+=1


def reduce_jd_content():
    genai.configure(api_key=my_api_key)
    file_path = '/home/piyush/Documents/dbda/project/ml/jd_sample/jd.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        # Prompt Template
        input_prompt = f"""Summarize the following job description by extracting only the most important details, including the job title, key responsibilities, essential qualifications, and any unique aspects of the position. Omit repetitive or less critical information, and ensure the summary is concise and to the point. Job Description Text: {text}"""
        response = get_gemini_repsonse(input_prompt)
        with open(file_path, 'w') as file_writter:
            # Write some content to the file
            file_writter.write(response)


# ... process the DataFrame
reduce_resume_content()
spark.stop()