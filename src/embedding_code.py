from sentence_transformers import SentenceTransformer
import numpy as np, os

model = SentenceTransformer('all-MiniLM-L6-v2')
directory = '/home/sunbeanm/Documents/dbda/project/ml/shortned_resumes/'
# directory = '/home/sunbeanm/Documents/dbda/project/ml/jd_sample/'
output_directory = '/home/sunbeanm/Documents/dbda/project/ml/encodings/resume_encodings/'
# output_directory = '/home/sunbeanm/Documents/dbda/project/ml/encodings/jd_encodings/'

for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='latin-1') as file:
            text = file.read()
            embeddings = model.encode(text)
        new_file_name = filename.replace(".txt",".npy")
        new_file_path = os.path.join(output_directory, new_file_name)
        np.save(new_file_path, embeddings)
        # with open(new_file_path, 'w') as file_writter:
        #     # Write embeddings to the file
        #     file_writter.write(str(embeddings))