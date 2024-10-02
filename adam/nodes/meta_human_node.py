"""
Node for agent that sends a short question to the human
"""
import asyncio
from langchain_core.messages import HumanMessage
from agents.questioner import questioner

async def meta_human_node(state: dict) -> dict:
    print("###Meta Human Node###\n")

    messages = state["meta_messages"]

    questioner_chain = await questioner()

    question = await questioner_chain.ainvoke({"messages": messages})

    print(f"Question to Human: {question}")

    question_to_human = HumanMessage(content=question, name="AdAM")

    state["meta_messages"].append(question_to_human)
    return state
