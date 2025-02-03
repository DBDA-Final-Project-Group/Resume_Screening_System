from flask import Flask, request, render_template, redirect
import time
import embedding_code as emb
import resume_similarity_search_logic as sim
import reduce_resumes as rr

app = Flask(__name__)
count = 0
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
    html_page = prediction_page(results)
    return html_page

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
        rr.reduce_jd_content()
        return redirect("/")
    return "No content to save."

@app.route('/save_resume', methods=['POST'])
def save_and_create_embedding_resume():
    save_resume_file()
    rr.reduce_resume_content()
    emb.create_embedding_for_resume()
    return "Saved Resume, and succesfully created the embedding for it!"

def save_content(content):
    # Get the current timestamp
    global count
    timestamp = time.time()
    random_number = str(int(timestamp))+str(count)
    count += 1
    if content:
        with open(f"/home/piyush/Documents/dbda/project/ml/temp_resumes/resume{random_number}.txt", "w",
                  encoding="utf-8") as file:
            file.write(content)
        with open(f"/home/piyush/Documents/dbda/project/ml/resumes_samples/resume{random_number}.txt", "w",
                  encoding="utf-8") as file:
            file.write(content)
        return "File saved successfully!"
    return "No content to save."

def save_resume_file():
    content = request.form.get('resume_text')
    save_content(content)
    content_list = request.form.getlist('resumes[]')
    print(len(content_list))
    for cont in content_list:
        print(cont)
        save_content(cont)

# import shutil
# import os
#
# def clear_and_recreate_directory(directory_path):
#     if os.path.exists(directory_path):
#         shutil.rmtree(directory_path)  # Remove directory and its contents
#     os.makedirs(directory_path)  # Recreate the directory

# dirsToClean = ["/home/piyush/Documents/dbda/project/ml/temp_resumes", "/home/piyush/Documents/dbda/project/ml/temp_shortned_resumes"]
# for dirs in dirsToClean:
#     clear_and_recreate_directory(dirs)


def prediction_page(result):
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dictionary Viewer</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f4f4f9;
            }
            .container {
                max-width: 800px;
                margin: auto;
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            .entry {
                margin-bottom: 20px;
                border-bottom: 1px solid #ddd;
                padding-bottom: 10px;
            }
            .entry:last-child {
                border-bottom: none;
            }
            .key {
                font-size: 1.2em;
                font-weight: bold;
                color: #333;
            }
            .value {
                margin-top: 10px;
                font-size: 1em;
                color: #555;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Top Resumes To Consider</h1>
            <div id="content">
    """

    # Add dynamic content
    for key, value in result.items():
        html_template += f"""
                <div class="entry">
                    <div class="key">Resume: {key}</div>
                    <div class="value">{value}</div>
                </div>
        """

    # Close the HTML structure
    html_template += """
            </div>
        </div>
    </body>
    </html>
    """

    return html_template


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000,debug=True)
