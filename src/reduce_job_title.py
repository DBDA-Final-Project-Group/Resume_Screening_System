import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Load the file
file_path = "/home/sunbeanm/Downloads/normlized_classes.txt"  # Update this with the correct path
with open(file_path, 'r', encoding='latin-1') as f:
    job_titles = f.readlines()

# Clean and preprocess job titles
job_titles = [title.strip().lower() for title in job_titles if title.strip()]
job_titles = list(set(job_titles))  # Deduplicate
job_titles_cleaned = [re.sub(r'[^a-z\s]', '', title).strip() for title in job_titles]

# Vectorize using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(job_titles_cleaned)

# Perform clustering to group similar job titles
num_clusters = 100
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)

# Create a DataFrame with job titles and their clusters
clustered_titles = pd.DataFrame({'Job Title': job_titles_cleaned, 'Cluster': kmeans.labels_})
clustered_titles_grouped = clustered_titles.groupby('Cluster').head(1)

# Save the reduced list to a new file
output_path = "/home/sunbeanm/Downloads/reduced_job_titles.txt"  # Adjust path if needed
with open(output_path, 'w') as f:
    f.write('\n'.join(clustered_titles_grouped['Job Title'].tolist()))

print(f"Reduced job titles saved to {output_path}")
