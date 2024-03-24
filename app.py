from flask import Flask,render_template,request
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('uploadfile.html')

@app.route('/process',methods=['POST'])
def process():
    if 'file' not in request.files:
        return 'No file part'
    file=request.files['file']
    if file.filename=='':
        return 'No selected file'
    summary=''
    if file:
        filename=file.filename
        file.save(os.path.join('uploads',filename))
        if filename.endswith('.pdf'):
            summary=langpdf(filename)
        elif filename.endswith('.txt'):
            text=file.read().decode('utf-8')
            summary=langtxt(filename)
        else:
            summary='File type not supported'
    return summary

def langpdf(file):
    return 'answer'

def langtxt(text):
    return text.upper()

if __name__ == '__main__':
    app.run(debug=True)
