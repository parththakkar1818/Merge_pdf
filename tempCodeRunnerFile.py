from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from PyPDF2 import PdfMerger

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge():
    create_upload_folder()

    merger = PdfMerger()
    filenames = []

    if 'pdfs' in request.files:
        pdf_files = request.files.getlist('pdfs')

        for file in pdf_files:
            if file and allowed_file(file.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)
                filenames.append(file.filename)
                merger.append(filename)

    output_filename = 'merged.pdf'
    output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

    with open(output_filepath, 'wb') as output_file:
        merger.write(output_file)

    return send_from_directory(app.config['UPLOAD_FOLDER'], output_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
