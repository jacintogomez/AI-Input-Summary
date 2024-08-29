from flask import Flask,render_template,request
from dotenv import load_dotenv

import textwrap
import os
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('uploadfile.html')

@app.route('/process',methods=['POST'])
def process():
    return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=True)

