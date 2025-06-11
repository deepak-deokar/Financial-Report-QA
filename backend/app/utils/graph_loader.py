# backend/app/utils/graph_loader.py

from neo4j import GraphDatabase
from app import config

# --- Neo4j driver ---
driver = GraphDatabase.driver(
    config.NEO4J_URI,
    auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
)

# --- Test Neo4j connection ---
def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 1 AS result")
        value = result.single()["result"]
        print(f"[Neo4j] Test connection successful: {value}")

# --- Ingest chunks into Neo4j as DocumentChunk nodes ---
def save_chunks_to_neo4j(chunks, source="unknown"):
    with driver.session() as session:
        count = 0
        for chunk in chunks:
            text = chunk.page_content if hasattr(chunk, "page_content") else chunk
            session.run("""
                CREATE (c:DocumentChunk {text: $text, source: $source})
            """, text=text, source=source)
            count += 1
        print(f"[Neo4j] Ingested {count} chunks as 'DocumentChunk' nodes ✅")

# --- Load knowledge graph (for HybridRAG context) ---
def load_knowledge_graph():
    print("[Neo4j] Loading knowledge graph...")
    with driver.session() as session:
        result = session.run("""
            MATCH (c:DocumentChunk)
            RETURN c.text AS text
            LIMIT 100
        """)
        nodes = [record["text"] for record in result]
    print(f"[Neo4j] Loaded {len(nodes)} nodes from graph ✅")
    return nodes