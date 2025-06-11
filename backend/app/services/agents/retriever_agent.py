# backend/app/services/agents/retriever_agent.py

from langchain_core.messages import AIMessage

def retrieve_relevant_docs(messages: list, vector_store, graph_nodes):
    print("[Agent] Retrieving relevant documents...")

    # Use rewritten question
    query = messages[-1].content

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    docs = retriever.get_relevant_documents(query)

    kg_context = " ".join(graph_nodes)
    combined_context = "\n\n".join([doc.page_content for doc in docs]) + "\n\n" + kg_context

    print(f"[Agent] Retrieved {len(docs)} docs + KG context")

    return [AIMessage(content=combined_context)]