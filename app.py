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
    if file:
        filename=file.filename
        file.save(os.path.join('uploads',filename))
        if filename.endswith('.pdf'):
            langpdf(filename)
        elif filename.endswith('.txt'):
            langtxt(filename)
        else:
            return 'File type not supported'

def langpdf(file):
    pass

def langtxt(file):
    pass

if __name__ == '__main__':
    app.run(debug=True)
