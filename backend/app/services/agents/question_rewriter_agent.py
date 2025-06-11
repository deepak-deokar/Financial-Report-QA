# backend/app/services/agents/question_rewriter_agent.py

from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage

def rewrite_question(messages: list):
    print("[Agent] Rewriting question...")

    llm = Ollama(model="phi4-mini", base_url="http://localhost:11434")

    # Assume latest HumanMessage is the user input
    question = messages[-1].content

    prompt = f"Rewrite this user question to be more precise and suitable for document retrieval and keep dates or year as it is:\n\n{question}"
    response = llm.invoke(prompt)

    print(f"[Agent] Rewritten: {response}")

    return [AIMessage(content=response)]