"""
This is a special node that doesn't contain an AI agent; instead, it houses a function to
receive input from the human. This is the second node in the graph, and its purpose is to get
feedback from the human and ensure that the re-engineered prompt is on track. It serves a
similar purpose to active listening and makes sure that the AI agent understood the human's
intent.
"""
import asyncio
from icecream import ic

async def human_node(state: dict) -> dict:
    print(f"[human_node] Called with state: {state}")
    ic(state)