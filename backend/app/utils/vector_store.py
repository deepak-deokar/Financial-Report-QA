from pinecone import Pinecone
from app import config

def get_pinecone_index():
    pc = Pinecone(api_key=config.PINECONE_API_KEY)
    return pc.Index(config.PINECONE_INDEX_NAME)

def save_vector_store(chunks, collection_name="default", batch_size=96):
    print(f"[Pinecone] Saving {len(chunks)} chunks using server-managed embedding with `upsert_records()`")

    index = get_pinecone_index()
    batch = []

    for i, chunk in enumerate(chunks):
        # Extract plain text from LangChain Document or dict
        if hasattr(chunk, "page_content"):
            text = chunk.page_content
            metadata = chunk.metadata if hasattr(chunk, "metadata") else {}
        elif isinstance(chunk, dict):
            text = chunk.get("text", "")
            metadata = chunk.get("metadata", {})
        else:
            text = str(chunk)
            metadata = {}

        vector_id = f"{collection_name}_{i}"

        batch.append({
            "id": vector_id,
            "text": text
        })

        if len(batch) >= batch_size:
            index.upsert_records(namespace=collection_name, records=batch)
            print(f"[Pinecone] ✅ Uploaded batch of {len(batch)}")
            batch = []

    if batch:
        index.upsert_records(namespace=collection_name, records=batch)
        print(f"[Pinecone] ✅ Uploaded final batch of {len(batch)}")