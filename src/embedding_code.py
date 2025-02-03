from sentence_transformers import SentenceTransformer
import numpy as np, os
def create_embeddings(directory, output_directory):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                embeddings = model.encode(text)
            new_file_name = filename.replace(".txt", ".npy")
            new_file_path = os.path.join(output_directory, new_file_name)
            np.save(new_file_path, embeddings)

def create_embedding_for_resume():
    short_resume_directory = '/home/piyush/Documents/dbda/project/ml/temp_shortned_resumes/'
    resume_output_directory = '/home/piyush/Documents/dbda/project/ml/encodings/resume_encodings/'
    create_embeddings(short_resume_directory, resume_output_directory)

def create_embedding_for_jd():
    jd_directory = '/home/piyush/Documents/dbda/project/ml/jd_sample/'
    jd_output_directory = '/home/piyush/Documents/dbda/project/ml/encodings/jd_encodings/'
    create_embeddings(jd_directory, jd_output_directory)