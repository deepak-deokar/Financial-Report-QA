# backend/app/services/table_qa.py

import pdfplumber
import pandas as pd
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- Extract tables from PDF ---
def extract_tables_from_pdf(file_path: str):
    print(f"[TableQA] Extracting tables from: {file_path}")

    tables = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_tables = page.extract_tables()
            for table in page_tables:
                df = pd.DataFrame(table[1:], columns=table[0])
                print(f"[TableQA] Extracted table on page {i+1} with shape {df.shape}")
                tables.append(df)

    print(f"[TableQA] Total tables extracted: {len(tables)}")
    return tables

# --- Build Table QA Prompt ---
def build_table_qa_prompt(table_text: str, user_question: str) -> str:
    prompt_template = """
You are a financial data expert. Answer the user's question based on the following table:

TABLE:
{table}

QUESTION:
{question}

Answer clearly and concisely.
"""
    prompt = prompt_template.format(table=table_text, question=user_question)
    return prompt

# --- Run Table QA ---
def run_table_qa(file_path: str, user_question: str):
    print(f"[TableQA] Running Table QA...")

    # Step 1: Extract tables
    tables = extract_tables_from_pdf(file_path)

    if not tables:
        print("[TableQA] No tables found!")
        return "No tables found in document."

    # For simplicity → use first table (or implement selection logic)
    df = tables[0]
    table_text = df.to_string()

    # Step 2: Build prompt
    prompt = build_table_qa_prompt(table_text, user_question)

    # Step 3: Initialize Ollama LLM
    llm = Ollama(
        model="mistral",  # You can switch to "llama3", "phi3", etc.
        base_url="http://localhost:11434"
    )

    chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template("{input}")
    )

    # Step 4: Run chain
    response = chain.run(input=prompt)

    print(f"[TableQA] Response: {response}")
    return response