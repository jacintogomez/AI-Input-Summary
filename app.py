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
            print('pdf file')
            summary=langpdf(filename)
        elif filename.endswith('.txt'):
            text=''
            with open(os.path.join('uploads',filename),'r') as file:
                text=file.read()
            print('txt file: ',text)
            summary=langtxt(text)
        else:
            print('Not supported')
            summary='File type not supported'
    print('summary is ',summary)
    return render_template('results.html',summary=summary)

def langpdf(file):
    return 'answer'

def langtxt(text):
    return text.upper()

if __name__ == '__main__':
    app.run(debug=True)
