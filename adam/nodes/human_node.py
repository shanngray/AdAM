"""
Node for agent that sends a short question to the human
"""
import asyncio
from langchain_core.messages import HumanMessage
from agents.questioner import questioner
from icecream import ic

async def human_node(state: dict) -> dict:
    print("###Human Node###\n")

    messages = state["messages"]

    questioner_chain = await questioner()

    ic(questioner_chain)    
    question = await questioner_chain.ainvoke({"messages": messages})

    print(f"Question to Human: {question}")

    question_to_human = HumanMessage(content=question, name="AdAM")

    state["messages"].append(question_to_human)
    return state
