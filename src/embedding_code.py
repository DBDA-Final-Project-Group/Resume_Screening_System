from sentence_transformers import SentenceTransformer
import PyPDF2
import numpy

model = SentenceTransformer('all-MiniLM-L6-v2')
path = 'Resume0001.pdf'
numpy_path = 'Resume0001.npy'
with open(path,'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()

embeddings = model.encode(text)

np.save(numpy_path, embeddings)