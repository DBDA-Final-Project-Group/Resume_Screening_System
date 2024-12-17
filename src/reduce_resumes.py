from Util import Util
import google.generativeai as genai
import os, configparser, time

config = configparser.ConfigParser()
project_path = Util.get_project_folder_path()
print(f"project_path: {project_path}")
linkedIn_properties_filepath = os.path.join(project_path,"resources","linkedIn.properties")
config.read(linkedIn_properties_filepath)

my_api_key = config['gemini_api_key']['GOOGLE_GEMINI_API_KEY']
print(my_api_key)
genai.configure(api_key=my_api_key)

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

directory = '/home/sunbeanm/Documents/dbda/project/ml/resumes_samples/'

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
                    Please return the extracted information in a key-value format.
                    Resume Text: {text}"""
                response = get_gemini_repsonse(input_prompt)

                # new_file_name = filename.replace(".txt",".npy")

                # Define the path to the shortned resume folder
                dependent_folder = '/home/sunbeanm/Documents/dbda/project/ml/shortned_resumes/'

                # Create the full path for the new file
                new_file_path = os.path.join(dependent_folder, filename)
                with open(new_file_path, 'w') as file_writter:
                    # Write some content to the file
                    file_writter.write(response)
            count+=1