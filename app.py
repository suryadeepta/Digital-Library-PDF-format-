from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import shutil
import json

app = Flask(__name__)

# Define folders
UPLOAD_FOLDER = 'uploads'
ORG_FOLDER = 'organized'

# Create folders if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ORG_FOLDER, exist_ok=True)

# Load topics from topics.json
def load_topics():
    try:
        with open('topics.json', 'r') as f:
            topics = json.load(f)
            return topics
    except FileNotFoundError:
        print("topics.json not found.")
        return []
    except json.JSONDecodeError:
        print("topics.json is not valid JSON.")
        return []

@app.route('/')
def index():
    topics = load_topics()
    return render_template('index.html', topics=topics)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf' not in request.files or 'topic' not in request.form:
        return "Missing PDF file or topic", 400

    topic = request.form['topic']
    file = request.files['pdf']

    if file and file.filename.lower().endswith('.pdf'):
        filename = file.filename
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(upload_path)

        topic_path = os.path.join(ORG_FOLDER, topic)
        os.makedirs(topic_path, exist_ok=True)

        dest_path = os.path.join(topic_path, filename)
        shutil.move(upload_path, dest_path)

        return redirect(url_for('index'))
    else:
        return "Only PDF files are allowed.", 400

@app.route('/library')
def library():
    topics = load_topics()
    pdf_files = {}

    # For each topic, get all PDF files
    for topic in topics:
        topic_folder = os.path.join(ORG_FOLDER, topic)
        if os.path.exists(topic_folder):
            pdf_files[topic] = [f for f in os.listdir(topic_folder) if f.endswith('.pdf')]

    return render_template('library.html', pdf_files=pdf_files)

@app.route('/pdf/<topic>/<filename>')
def view_pdf(topic, filename):
    # Serve PDF file directly
    topic_folder = os.path.join(ORG_FOLDER, topic)
    return send_from_directory(topic_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)
