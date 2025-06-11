import os
import json
from pathlib import Path
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
# Optional: DOCX support (if you want later):
# from langchain_community.document_loaders import UnstructuredWordDocumentLoader

from bs4 import BeautifulSoup  # for HTML support!

from app import config
from app.utils.vector_store import save_vector_store

# --- Universal load_text_file ---
def load_text_file(file_path: str) -> List[str]:
    print(f"[DocLoader] Loading TXT: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return [text]

# --- Load PDF ---
def load_pdf(file_path: str):
    print(f"[DocLoader] Loading PDF: {file_path}")
    loader = PyPDFLoader(file_path)
    return loader.load()

# --- Load HTML ---
def load_html(file_path: str) -> List[str]:
    print(f"[DocLoader] Loading HTML: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator="\n")
    return [text]

# --- Load FinQA JSON ---
def load_finqa_json(file_path: str):
    print(f"[DocLoader] Loading FinQA JSON: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = []
    for item in data:
        question = item.get("question", "")
        table = item.get("table", "")
        answer = item.get("answer_text", "")
        combined = f"Question: {question}\nTable: {table}\nAnswer: {answer}"
        chunks.append(combined)
    return chunks

# --- Load TAT-QA JSON ---
def load_tatqa_json(file_path: str):
    print(f"[DocLoader] Loading TAT-QA JSON: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = []
    for item in data:
        question = item.get("question", "")
        table = item.get("table", "")
        paragraph = item.get("paragraphs", "")
        answer = item.get("answer", {}).get("answer_text", "")
        combined = f"Question: {question}\nTable: {table}\nParagraph: {paragraph}\nAnswer: {answer}"
        chunks.append(combined)
    return chunks

# --- Split documents (standardized) ---
def split_documents(documents: List[str]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )
    chunks = splitter.create_documents(documents)
    print(f"[DocLoader] Split into {len(chunks)} chunks ✅")
    return chunks

# --- Ingest document (PDF/TXT/HTML Uploads) ---
def ingest_document(file_path: str, collection_name="default"):
    print(f"[Ingest] Ingesting document: {file_path}")

    # Detect file type
    if file_path.lower().endswith(".txt"):
        raw_docs = load_text_file(file_path)
    elif file_path.lower().endswith(".pdf"):
        raw_docs = load_pdf(file_path)
        raw_docs = [doc.page_content for doc in raw_docs]
    elif file_path.lower().endswith(".html"):
        raw_docs = load_html(file_path)
    else:
        print("[Ingest] Unsupported file type!")
        return

    print(f"[Ingest] Loaded document (length={len(raw_docs)} chunks)")

    # Split
    chunks = split_documents(raw_docs)

    # Save to vector store
    save_vector_store(chunks, collection_name=collection_name)

    print(f"[Ingest] Ingestion complete ✅")