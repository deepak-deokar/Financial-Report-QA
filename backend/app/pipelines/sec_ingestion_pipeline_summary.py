import os
from typing import List, Dict
import requests
from app.utils.vector_store import save_vector_store
from app.utils.graph_loader import save_chunks_to_neo4j
from app import config
import time

# ─────────────────────────────────────────────
# 1. — Summarise a long text file with Ollama
# ───────────────────────────────────────────--
def summarize_text(raw_text: str, model: str = config.OLLAMA_MODEL, retries: int = 4, timeout: int = 45) -> str:
    """Summarize SEC filing using Ollama with retry logic."""
    prompt = (
        "Summarise the following SEC filing very concisely (≈200 words). "
        "Focus on company, filing type, period covered, and 3-5 key financial points.\n\n"
        f"{raw_text[:8000]}"  # use first 8k chars, safer than 6k
    )

    for attempt in range(1, retries + 1):
        try:
            print(f"[Summary] 🔄 Attempt {attempt} — Sending request to Ollama...")
            response = requests.post(
                f"{config.OLLAMA_BASE_URL}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=timeout
            )
            response.raise_for_status()
            print("[Summary] ✅ Summary received")
            return response.json()["response"].strip()

        except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
            print(f"[Summary] ❌ Error summarizing text (attempt {attempt}): {e}")
            if attempt < retries:
                time.sleep(5)  # wait before retry
            else:
                raise RuntimeError(f"Failed after {retries} retries: {e}")

# ─────────────────────────────────────────────
# 2. — Build summary chunk
# ─────────────────────────────────────────────
def build_summary_chunk(title: str,
                        company: str,
                        form_type: str,
                        summary: str,
                        file_path: str) -> Dict:
    chunk_text = f"Company: {company}\nForm: {form_type}\nTitle: {title}\nSummary:\n{summary}"
    metadata = {
        "company": company,
        "form_type": form_type,
        "title": title,
        "source": file_path
    }
    return {"text": chunk_text, "metadata": metadata}

# ─────────────────────────────────────────────
# 3. — Main ingestion with debug steps
# ─────────────────────────────────────────────
def ingest_sec_dataset(root_folder: str,
                       max_files: int = 100,
                       pinecone_batch: int = 96,
                       neo4j_batch: int = 50):
    print(f"[SEC-Summary] Scanning: {root_folder}")
    if not os.path.isdir(root_folder):
        print("❌ Folder does not exist.")
        return

    txt_files: List[str] = []
    for dirpath, _, files in os.walk(root_folder):
        for fn in files:
            if fn.endswith(".txt"):
                txt_files.append(os.path.join(dirpath, fn))
                if len(txt_files) >= max_files:
                    break
        if len(txt_files) >= max_files:
            break
    print(f"[SEC-Summary] Found {len(txt_files)} filings")

    pc_batch, neo_batch, pc_accum, neo_accum = [], [], 0, 0

    for idx, file_path in enumerate(txt_files):
        print(f"\n[{idx+1}/{len(txt_files)}] Processing: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                raw_text = f.read()
        except Exception as e:
            print(f"[Skip] Could not read {file_path}: {e}")
            continue

        parts = file_path.split(os.sep)
        try:
            company, form_type = parts[-4], parts[-3]
        except IndexError:
            company, form_type = "UNKNOWN", "UNKNOWN"

        title = os.path.basename(file_path)
        summary = summarize_text(raw_text)

        if summary.startswith("[ERROR"):
            print(f"[Skip] Skipping file due to summary error: {file_path}")
            continue

        chunk = build_summary_chunk(title, company, form_type, summary, file_path)
        pc_batch.append(chunk)
        flattened_chunk = {
            "text": chunk["text"],
            **chunk["metadata"]
            }
        neo_batch.append(flattened_chunk)
        pc_accum += 1
        neo_accum += 1

        if pc_accum >= pinecone_batch:
            print(f"[Pinecone] 🔁 Uploading batch of {len(pc_batch)}")
            try:
                save_vector_store(pc_batch, collection_name="sec_summaries")
                print("[Pinecone] ✅ Batch uploaded")
            except Exception as e:
                print(f"[Pinecone] ❌ Upload error: {e}")
            pc_batch, pc_accum = [], 0

        if neo_accum >= neo4j_batch:
            print(f"[Neo4j] 🔁 Uploading batch of {len(neo_batch)}")
            try:
                save_chunks_to_neo4j(neo_batch, source="sec_summary_ingestion")
                print("[Neo4j] ✅ Batch uploaded")
            except Exception as e:
                print(f"[Neo4j] ❌ Upload error: {e}")
            neo_batch, neo_accum = [], 0

    # Final flush
    if pc_batch:
        print(f"[Pinecone] ⏳ Uploading final batch of {len(pc_batch)}")
        try:
            save_vector_store(pc_batch, collection_name="sec_summaries")
            print("[Pinecone] ✅ Final batch uploaded")
        except Exception as e:
            print(f"[Pinecone] ❌ Final upload error: {e}")

    if neo_batch:
        print(f"[Neo4j] ⏳ Uploading final batch of {len(neo_batch)}")
        try:
            save_chunks_to_neo4j(neo_batch, source="sec_summary_ingestion")
            print("[Neo4j] ✅ Final batch uploaded")
        except Exception as e:
            print(f"[Neo4j] ❌ Final upload error: {e}")

    print("\n🎉 SEC summary ingestion complete!")