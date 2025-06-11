import os
import json
import sys
from app.utils.vector_store import save_vector_store
from app.utils.graph_loader import save_chunks_to_neo4j
from app.utils.document_loader import split_documents

def ingest_tatqa_dataset(file_path: str):
    print(f"[TATQA Ingestion] Ingesting TAT-QA dataset: {file_path}")

    if not os.path.exists(file_path):
        print(f"[TATQA Ingestion] ERROR: File does not exist → {file_path}")
        return

    with open(file_path, "r") as f:
        data = json.load(f)
        data = data[:100]  # Limit to 100 samples for demo

    BATCH_SIZE = 50
    chunks_batch = []
    total_chunks = 0

    for i, entry in enumerate(data):
        q = entry.get("qa", {}).get("question", "")
        a = entry.get("qa", {}).get("answer", "")
        table = entry.get("table", "")
        combined_text = f"Question: {q}\nAnswer: {a}\nTable: {table}"

        split_chunks = split_documents(combined_text)
        chunks_batch.extend(split_chunks)

        if len(chunks_batch) >= BATCH_SIZE:
            save_vector_store(chunks_batch, collection_name="tatqa")
            save_chunks_to_neo4j(chunks_batch, source=file_path)
            total_chunks += len(chunks_batch)
            print(f"[Ingestion] ✅ Batch of {len(chunks_batch)} chunks uploaded")
            chunks_batch = []

    if chunks_batch:
        save_vector_store(chunks_batch, collection_name="tatqa")
        save_chunks_to_neo4j(chunks_batch, source=file_path)
        total_chunks += len(chunks_batch)
        print(f"[Ingestion] ✅ Final batch of {len(chunks_batch)} chunks uploaded")

    print(f"[Ingestion] 🎉 DONE — Total Chunks Ingested: {total_chunks}")