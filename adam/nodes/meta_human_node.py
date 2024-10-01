"""
This is a special node that doesn't contain an AI agent; instead, it houses a function to
receive input from the human. This is the second node in the graph, and its purpose is to get
feedback from the human and ensure that the re-engineered prompt is on track. It serves a
similar purpose to active listening and makes sure that the AI agent understood the human's
intent.
"""
import asyncio
from langchain_core.messages import HumanMessage

async def meta_human_node(state: dict) -> dict:
    print("###Human Node###\n")

    message_to_human = HumanMessage(content="placeholder to human", name="AdAM")

    state["meta_messages"].append(message_to_human)
    return state
