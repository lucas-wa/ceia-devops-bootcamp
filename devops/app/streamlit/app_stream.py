import streamlit as st
import requests
import json
from PyPDF2 import PdfReader
import chromadb
from langchain.text_splitter import CharacterTextSplitter

prompt_template = """
Você é um assistente que precisa responder às dúvidas de um usuário com base em um documento fornecido como contexto.

Esse é o documento:
{context}

Essa é a pergunta do usuário:
{question}

Responda a pergunta do usuário com base no documento fornecido.
"""

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def store_document_in_chroma(client, document_text, collection_name="documents"):
    text_splitter = CharacterTextSplitter(chunk_size=128, chunk_overlap=0)
    texts = text_splitter.split_text(document_text)
    collection = client.get_or_create_collection(name=collection_name)
    collection.add(
        documents=texts,
        metadatas=[{"source": "uploaded_pdf"}] * len(texts),
        ids=[f"doc_{i}" for i in range(len(texts))]
    )

def retrieve_relevant_documents(client, question, collection_name="documents", n_results=1):
    collection = client.get_collection(name=collection_name)
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    return results["documents"]

def get_answer_from_llm(question, context):
    prompt = prompt_template.format(context=context, question=question)
    print("prompt", prompt)
    url = "http://localhost:8000/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "unsloth/Qwen3-8B-bnb-4bit",
        "messages": [
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": prompt},
        ],
        "stream": True,
        "max_tokens": 2048
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload), stream=True)
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                if decoded_line.startswith("data:"):
                    data = decoded_line[5:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        content = chunk["choices"][0]["delta"].get("content", "")
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        continue
    else:
        yield "Erro ao obter resposta do modelo."

st.title("Document QA with vLLM and ChromaDB")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "txt"])

if uploaded_file:
    document_text = uploaded_file.getvalue().decode("utf-8") if uploaded_file.type == "text/plain" else extract_text_from_pdf(uploaded_file)
    client = chromadb.Client()
    store_document_in_chroma(client, document_text)
    st.success("Documento carregado com sucesso!")

    question = st.text_input("Digite sua pergunta:")
    if question:
        context = retrieve_relevant_documents(client, question)
        answer_placeholder = st.empty()
        response = ""
        for answer_chunk in get_answer_from_llm(question, context):
            response += answer_chunk
            answer_placeholder.markdown(response)
