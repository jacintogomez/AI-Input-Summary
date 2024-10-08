from flask import Flask,render_template,request
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader

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
            summary=langtxt(filename)
        else:
            print('Not supported')
            summary='File type not supported'
    print('summary completed')
    return render_template('results.html',summary=summary,docname=file.filename)

def langpdf(file):
    llm=ChatOpenAI()
    prompt=ChatPromptTemplate.from_template("""Answer the following request based only on the provided context:
    
    <context>
    {context}
    </context>
    
    Question: {input}""")
    documentchain=create_stuff_documents_chain(llm,prompt)
    loader=PyPDFLoader(os.path.join('uploads',file))
    pages=loader.load_and_split()

    embeddings=OpenAIEmbeddings()
    tsplitter=RecursiveCharacterTextSplitter()
    documents=tsplitter.split_documents(pages)
    vec=FAISS.from_documents(documents,embeddings)

    retriever=vec.as_retriever()
    retrievalchain=create_retrieval_chain(retriever,documentchain)
    question='Please summarize the given file in 5 sentences or less'
    response=retrievalchain.invoke({'input':question})
    print(question)
    cleanans=response['answer']
    print(consoleformat(cleanans))
    return cleanans

def langtxt(file):
    llm=ChatOpenAI()
    prompt=ChatPromptTemplate.from_template("""Answer the following request based only on the provided context:
    
    <context>
    {context}
    </context>
    
    Question: {input}""")
    documentchain=create_stuff_documents_chain(llm,prompt)
    loader=TextLoader(os.path.join('uploads',file))
    docs=loader.load()

    embeddings=OpenAIEmbeddings()
    tsplitter=RecursiveCharacterTextSplitter()
    documents=tsplitter.split_documents(docs)
    vec=FAISS.from_documents(documents,embeddings)

    retriever=vec.as_retriever()
    retrievalchain=create_retrieval_chain(retriever,documentchain)
    question='Please summarize the given file in 5 sentences or less'
    response=retrievalchain.invoke({'input':question})
    print(question)
    cleanans=response['answer']
    print(consoleformat(cleanans))
    return cleanans

def consoleformat(input,width=100):
    formatted=textwrap.fill(input,width)
    return formatted

if __name__ == '__main__':
    app.run(debug=True)

