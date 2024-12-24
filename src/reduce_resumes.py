from Util import Util
import google.generativeai as genai
import os, configparser, time

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text



import shutil
import os

def clear_and_recreate_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)  # Remove directory and its contents
    os.makedirs(directory_path)  # Recreate the directory

def reduce_resume_content():
    # config = configparser.ConfigParser()
    # project_path = Util.get_project_folder_path()
    # print(f"project_path: {project_path}")
    # properties_filepath = os.path.join(project_path, "resources", "config.properties")
    # config.read(properties_filepath)
    #
    # my_api_key = config['gemini_api_key']['GOOGLE_GEMINI_API_KEY']
    # print(my_api_key)
    my_api_key = "AIzaSyAd-lL3B-Hi34Qr9pkfOdOefd_EJF09Wio"
    genai.configure(api_key=my_api_key)

    # directory = '/home/piyush/Documents/dbda/project/ml/resumes_samples/'
    directory = '/home/piyush/Documents/dbda/project/ml/temp_resumes/'

    # Define the path to the shortned resume folder
    temp_dependent_folder = '/home/piyush/Documents/dbda/project/ml/temp_shortned_resumes/'
    dependent_folder = '/home/piyush/Documents/dbda/project/ml/shortned_resumes/'

    count = 0
    for filename in os.listdir(directory):
        if count==10:
            print("waited")
            time.sleep(60)
            count=0
        else:
            if filename.endswith('.txt'):
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r', encoding='latin-1') as file:
                    text = file.read()
                    # Prompt Template
                    input_prompt = f"""
                        I will provide you with the text content of a resume. Your task is to extract the following important details from it:
                        Skills, Total Experience, College Name, Degree, Designation, Company Names
                        Please return the extracted information, remove duplicate skills but keep important information.
                        Resume Text: {text}"""
                    response = get_gemini_repsonse(input_prompt)

                    # new_file_name = filename.replace(".txt",".npy")

                    # Create the full path for the new file
                    new_file_path = os.path.join(dependent_folder, filename)
                    with open(new_file_path, 'w') as file_writter:
                        # Write some content to the file
                        file_writter.write(response)
                    tmep_file_path = os.path.join(temp_dependent_folder, filename)
                    with open(tmep_file_path, 'w') as file_writter:
                        # Write some content to the file
                        file_writter.write(response)
                count+=1