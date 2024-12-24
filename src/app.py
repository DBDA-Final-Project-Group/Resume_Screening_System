from flask import Flask, request, render_template, redirect
import time
import embedding_code as emb
import resume_similarity_search_logic as sim
import reduce_resumes as rr

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/resumeSubmit', methods=['GET'])
def resume_page():
    return render_template("resumeSubmit.html")

@app.route('/save_jd', methods=['POST'])
def predict():
    save_jd_file()
    emb.create_embedding_for_jd()
    results = sim.similarity_search()
    return results


def save_jd_file():
    content = request.form.get('jobDescription')
    # Get the current timestamp
    timestamp = time.time()
    random_number = int((timestamp * 1000) % 100000)

    if content:
        with open(f"/home/piyush/Documents/dbda/project/ml/jd_collection/jd{random_number}.txt", "w", encoding="utf-8") as file:
            file.write(content)
        with open(f"/home/piyush/Documents/dbda/project/ml/jd_sample/jd.txt", "w", encoding="utf-8") as file:
            file.write(content)
            print("File saved successfully!")
            return redirect("/")
    return "No content to save."

@app.route('/save_resume', methods=['POST'])
def save_and_create_embedding_resume():
    save_resume_file()
    rr.reduce_resume_content()
    emb.create_embedding_for_resume()
    return "Saved Resume, and succesfully created the embedding for it!"

def save_resume_file():
    content = request.form.get('resume_text')
    # Get the current timestamp
    timestamp = time.time()
    random_number = int((timestamp * 1000) % 100000)
    if content:
        with open(f"/home/piyush/Documents/dbda/project/ml/temp_resumes/resume{random_number}.txt", "w", encoding="utf-8") as file:
            file.write(content)
        with open(f"/home/piyush/Documents/dbda/project/ml/resumes_samples/resume{random_number}.txt", "w", encoding="utf-8") as file:
            file.write(content)
        return "File saved successfully!"
    return "No content to save."


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000,debug=True)
