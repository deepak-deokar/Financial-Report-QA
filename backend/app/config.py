# backend/app/config.py

import os
from dotenv import load_dotenv

# Load .env if present (optional)
load_dotenv()

# Neo4j Aura settings
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://91e40f31.databases.neo4j.io")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "qArxw-_vILQuc-nUh1IVmIC6yI6qDz0oJ7ekwJ8Mq-I")

# Chroma (no longer used, kept for fallback/debug)
CHROMA_DB_DIR = "./vector_store"

# Embedding model (for SentenceTransformers)
EMBEDDING_MODEL = "llama-text-embed-v2"

# Chunking params
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Ollama settings
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "phi4-mini"

# Dataset paths
SEC_FILINGS_RAW_DIR = "../datasets/sec_filings/raw/sec-edgar-filings"
FINQA_FILE = "../datasets/finqa/train.json"
TATQA_FILE = "../datasets/tatqa/tatqa_dataset_train.json"

# --- Pinecone Integration ---
PINECONE_API_KEY = "pcsk_4oiz17_ScaR4XUjUdPzLGGe8tgFCqiwDTygGssCF4Gm1iaXU42hYid8dwtvQyiM8QfFqFt"  # Replace this
PINECONE_ENVIRONMENT = "us-east-1"  # From screenshot
PINECONE_INDEX_NAME = "financial-qa-index"
PINECONE_DIMENSION = 768