# backend/app/services/insight_generator.py

from app.utils.vector_store import load_vector_store
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

class InsightGenerator:
    def __init__(self, collection_name="default"):
        print(f"[Insight] Initializing Insight Generator for collection '{collection_name}'...")
        self.vector_store = load_vector_store(collection_name=collection_name)
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
        print("[Insight] Retriever ready ✅")

    def generate_insights(self, question: str) -> str:
        print(f"[Insight] Generating insights for question: {question}")

        # Use Ollama with your local Mistral
        llm = Ollama(model="mistral", base_url="http://localhost:11434")

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=self.retriever,
            chain_type="stuff"
        )

        response = qa_chain.run(question)
        print(f"[Insight] Response: {response}")
        return response