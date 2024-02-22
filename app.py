from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfMerger
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge():
    files = request.files.getlist('pdfs')
    # Merge PDF files in memory
    merger = PdfMerger()
    for pdf in files:
        pdf_bytes = pdf.read()
        merger.append(BytesIO(pdf_bytes))

    merged_pdf_bytes = BytesIO()
    merger.write(merged_pdf_bytes)
    merged_pdf_bytes.seek(0)

    return send_file(merged_pdf_bytes, as_attachment=True, download_name='merged.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
