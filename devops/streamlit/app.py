import streamlit as st
import os
from PyPDF2 import PdfReader
import chromadb
from vllm import LLM
import numpy as np

llm = LLM(model="meta-llama/Llama-2-7b-chat-hf", gpu_memory_utilization=0.9, max_model_len=752)

# Função para extrair texto do PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Função para inicializar o cliente do chromadb
def init_chroma():
    client = chromadb.Client()
    return client

# Função para armazenar documento no ChromaDB
def store_document_in_chroma(client, document_text, collection_name="documents"):
    collection = client.create_collection(name=collection_name)
    collection.add(
        documents=[document_text],
        metadatas=[{"source": "uploaded_pdf"}],
        ids=["doc_1"]
    )

# Função para buscar uma resposta com vLLM
def get_answer_from_llm(question, context):
    prompt = f"Question: {question}\nContext: {context}\nAnswer:"
    response = llm.generate(prompt)
    return response['text']

# Interface Streamlit
st.title("Document QA with vLLM and Chromadb")

# Upload do documento
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "txt"])

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        document_text = extract_text_from_pdf(uploaded_file)
    else:
        document_text = uploaded_file.getvalue().decode("utf-8")

    # Inicializa o cliente do chromadb e armazena o documento
    client = init_chroma()
    store_document_in_chroma(client, document_text)

    st.success("Documento carregado com sucesso!")

    # Pergunta do usuário
    question = st.text_input("Digite sua pergunta:")

    if question:
        # Recupera a resposta do LLM
        answer = get_answer_from_llm(question, document_text)
        st.write(f"Resposta: {answer}")
