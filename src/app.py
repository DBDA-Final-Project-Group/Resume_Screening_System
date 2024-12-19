from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/resumeSubmit', methods=['GET'])
def resume_page():
    return render_template("resumeSubmit.html")

@app.route('/save_jd', methods=['POST'])
def save_jd_file():
    content = request.form.get('jobDescription')
    if content:
        with open("/home/piyush/Documents/dbda/project/ml/jd_sample/jd.txt", "w", encoding="utf-8") as file:
            file.write(content)
        return "File saved successfully!"
    return "No content to save."

@app.route('/save_resume', methods=['POST'])
def save_resume_file():
    content = request.form.get('resume_text')
    if content:
        with open("/home/piyush/Documents/dbda/project/ml/resumes_samples/resume.txt", "w", encoding="utf-8") as file:
            file.write(content)
        return "File saved successfully!"
    return "No content to save."

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000,debug=True)
