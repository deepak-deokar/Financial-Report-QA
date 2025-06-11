# backend/app/services/agents/answer_generator_agent.py

from langchain_core.messages import AIMessage

def generate_answer(messages: list, llm):
    print("[Agent] Generating answer...")

    context = messages[-1].content
    prompt = f"Answer the following based on context:\n\n{context}\n\nAnswer:"

    response = llm.invoke(prompt)

    print(f"[Agent] Generated Answer: {response}")

    return [AIMessage(content=response)]