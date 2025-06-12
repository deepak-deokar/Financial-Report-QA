# app/utils/vector_store.py
import os
from pinecone import Pinecone, ServerlessSpec
import json
from app import config
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# Initialize Pinecone client
def get_pinecone_index():
    pc = Pinecone(api_key=config.PINECONE_API_KEY)
    return pc.Index(config.PINECONE_INDEX_NAME)

# Save documents into Pinecone (with server-side embedding)
def save_vector_store(chunks, collection_name="default", batch_size=96):
    print(f"[VectorStore] Received {len(chunks)} chunks.")

    if len(chunks) > 1000:
        # Save locally as fallback
        local_dir = f"./local_vectors/{collection_name}"
        os.makedirs(local_dir, exist_ok=True)
        local_path = os.path.join(local_dir, "vectors.json")

        local_data = []
        for i, chunk in enumerate(chunks):
            if hasattr(chunk, "page_content"):
                text = chunk.page_content
                metadata = chunk.metadata if hasattr(chunk, "metadata") else {}
            elif isinstance(chunk, dict):
                text = chunk.get("text", "")
                metadata = chunk.get("metadata", {})
            else:
                text = str(chunk)
                metadata = {}

            local_data.append({
                "id": f"{collection_name}_{i}",
                "text": text,
                "metadata": metadata,
            })

        with open(local_path, "w") as f:
            json.dump(local_data, f, indent=2)

        print(f"[VectorStore] ⚠️ Exceeded chunk limit. Saved {len(local_data)} chunks locally at: {local_path}")
        return

    # Else: continue to Pinecone upload
    print(f"[Pinecone] Saving {len(chunks)} chunks using server-managed embedding with `upsert()`")

    index = get_pinecone_index()
    texts = []
    metadatas = []

    for chunk in chunks:
        if hasattr(chunk, "page_content"):
            texts.append(chunk.page_content)
            metadatas.append(chunk.metadata if hasattr(chunk, "metadata") else {})
        elif isinstance(chunk, dict):
            texts.append(chunk.get("text", ""))
            metadatas.append(chunk.get("metadata", {}))
        else:
            texts.append(str(chunk))
            metadatas.append({})

    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")
    vectors = embeddings.embed_documents(texts)

    batch = []
    for i, (vec, meta) in enumerate(zip(vectors, metadatas)):
        batch.append({
            "id": f"{collection_name}_{i}",
            "values": vec,
            "metadata": meta,
        })

    index.upsert(vectors=batch, namespace=collection_name)
    print(f"[Pinecone] ✅ Uploaded {len(batch)} vectors to Pinecone namespace '{collection_name}'")

# Load vector store using LangChain wrapper and Ollama embeddings
def load_vector_store(collection_name="default"):
    local_path = f"./local_vectors/{collection_name}/vectors.json"

    # ✅ Fallback to local if file exists
    if os.path.exists(local_path):
        print(f"[LocalLoad] Loading vector store locally from: {local_path}")
        with open(local_path, "r") as f:
            data = json.load(f)

        texts = [item["text"] for item in data]
        metadata = [item.get("metadata", {}) for item in data]

        embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")
        return FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadata)

    # ✅ Default: Load from Pinecone
    print(f"[Pinecone] Loading vector store from namespace: {collection_name}")
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")

    return PineconeVectorStore(
        index=get_pinecone_index(),
        embedding=embeddings,
        namespace=collection_name,
    )