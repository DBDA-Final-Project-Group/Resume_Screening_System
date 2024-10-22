import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

directory = '/home/mahendra/PycharmProjects/ProjectResume/Dataset/independent/'

for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='latin-1') as file:
            text = file.read()
            # Prompt Template
            input_prompt = f"""
                I will provide you with the text content of a resume. Your task is to extract the following important details from it:
                Skills, Total Experience, College Name, Degree, Designation, Company Names
                Please return the extracted information in a JSON object format and don't include any header or footer in it. Ensure the keys in the JSON are exactly as listed above.
                Resume Text: {text}"""
            response = get_gemini_repsonse(input_prompt)

            new_file_name = filename.replace(".txt",".lab")

            # Define the path to the dependent folder
            dependent_folder = '/home/mahendra/PycharmProjects/ProjectResume/Dataset/dependent/'

            # Create the full path for the new file
            new_file_path = os.path.join(dependent_folder, new_file_name)
            with open(new_file_path, 'w') as file_writter:
                # Write some content to the file
                file_writter.write(response)