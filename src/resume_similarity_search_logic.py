from sentence_transformers import SentenceTransformer
import faiss
import numpy as np,os

# Function to load embeddings from a .nyc file
def load_embeddings(file_path):
    return np.load(file_path)

def similarity_search():
    results = {}
    orignal_resume_directory = '/home/piyush/Documents/dbda/project/ml/resumes_samples/'
    resume_paths = []
    for filename in os.listdir(orignal_resume_directory):
        file_path = os.path.join(orignal_resume_directory, filename)
        resume_paths.append(file_path)

    resume_metadata = {i: resume for i, resume in enumerate(resume_paths)}
    print(resume_metadata)

    # Load the resume and job description embeddings (replace with actual file paths)

    directory = '/home/piyush/Documents/dbda/project/ml/encodings/resume_encodings/'
    resume_embeddings = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        resume_embeddings.append(load_embeddings(file_path))

    resume_embeddings = np.array(resume_embeddings)


    file_path_jd_embedding = '/home/piyush/Documents/dbda/project/ml/encodings/jd_encodings/jd.npy'
    job_description_embedding = np.array(load_embeddings(file_path_jd_embedding))


    if job_description_embedding.ndim == 1:
        job_description_embedding = job_description_embedding.reshape(1, -1)

    # Build a Faiss index for the resume embeddings
    dimension = resume_embeddings.shape[1]  # Dimension of the embeddings (ensure all embeddings are the same shape)
    index = faiss.IndexFlatL2(dimension)  # L2 distance metric (Euclidean distance)
    index.add(resume_embeddings)  # Add resume embeddings to the index

    # Query the Faiss index with the job description embedding
    k = 2 # Number of most similar resumes to return
    distances, indices = index.search(job_description_embedding, k)

    # Output the most similar resumes and their distances
    print(f"Top {k} most similar resumes to the job description:")
    for i in range(k):
        print(f"Resume {indices[0][i]} with distance {distances[0][i]}")

    for idx in indices[0]:
        resume_no = idx-1
        print(f"Resume no: {resume_no}")
        with open(resume_metadata[idx],"r", encoding='latin-1') as file:
            resume_content = file.read()
            results[str(resume_no)] = resume_content
            print(resume_content)

    return results
