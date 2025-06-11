# backend/app/services/hybrid_rag_agent_pipeline.py

from langgraph.graph import END, MessageGraph
from langchain_core.messages import HumanMessage, AIMessage
from app.utils.vector_store import load_vector_store
from app.utils.graph_loader import load_knowledge_graph
from langchain_ollama import OllamaLLM as Ollama
from app.services.agents.question_rewriter_agent import rewrite_question
from app.services.agents.retriever_agent import retrieve_relevant_docs
from app.services.agents.answer_generator_agent import generate_answer
from app.services.agents.postprocessing_agent import postprocess_answer

class HybridRAGAgentPipeline:
    def __init__(self, collection_name="default"):
        print("[HybridRAG] Initializing LangGraph Hybrid RAG Pipeline...")

        # Load Vector Store
        self.vector_store = load_vector_store(collection_name=collection_name)

        # Load KG
        self.graph_nodes = load_knowledge_graph()

        # LLM
        self.llm = Ollama(model="phi4-mini", base_url="http://localhost:11434")
        print("[HybridRAG] LLM ready ✅")

        # Build LangGraph
        self.graph = self.build_graph()

    def build_graph(self):
        graph = MessageGraph()

        # Define flow
        graph.add_node("rewrite_question", rewrite_question)
        graph.add_node("retrieve_docs", lambda x: retrieve_relevant_docs(x, self.vector_store, self.graph_nodes))
        graph.add_node("generate_answer", lambda x: generate_answer(x, self.llm))
        graph.add_node("postprocess", postprocess_answer)

        # Edges
        graph.set_entry_point("rewrite_question")
        graph.add_edge("rewrite_question", "retrieve_docs")
        graph.add_edge("retrieve_docs", "generate_answer")
        graph.add_edge("generate_answer", "postprocess")
        graph.add_edge("postprocess", END)

        return graph.compile()

    def run(self, question: str):
        print(f"[HybridRAG] Running LangGraph pipeline for: {question}")

        response = self.graph.invoke([HumanMessage(content=question)])
        
        final_answer = response[-1].content if isinstance(response[-1], AIMessage) else str(response)
        print(f"[HybridRAG] Final Answer: {final_answer}")

        return final_answer