"""
This is a special node that doesn't contain an AI agent; instead, it houses a function to
receive input from the human. This is the second node in the graph, and its purpose is to get
feedback from the human and ensure that the re-engineered prompt is on track. It serves a
similar purpose to active listening and makes sure that the AI agent understood the human's
intent.
"""
import asyncio
from langchain_core.messages import HumanMessage
from typing import Any, Dict

# Import the ConnectionManager from connection_manager.py
from adam.connection_manager import manager

async def human_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print(f"[human_node] Called with state: {state}")
    ws_id = state.get("ws_id")
    print(f"[human_node] WebSocket ID: {ws_id}")
    if not ws_id:
        print("[human_node] WebSocket ID not found in state.")
        return {"messages": [HumanMessage(content="WebSocket ID not provided", name="System")]}

    for attempt in range(5):
        input_queue = manager.input_queues.get(ws_id)
        if input_queue:
            print(f"[human_node] Input queue found for WebSocket ID {ws_id}")
            break
        print(f"[human_node] Input queue not found for WebSocket ID {ws_id}. Retry {attempt + 1}/5")
        await asyncio.sleep(0.5)
    else:
        print(f"[human_node] Failed to find input queue for WebSocket ID {ws_id} after retries.")
        return {"messages": [HumanMessage(content="Input queue not available", name="System")]}

    try:
        print("[human_node] Waiting for user input...")
        web_input = await input_queue.get()
        print(f"[human_node] Received input: {web_input}")

        human_message = HumanMessage(content=web_input, name="User")
        print(f"[human_node] HumanMessage created: {human_message}")

        return {"messages": [human_message]}
    except asyncio.CancelledError:
        print("[human_node] Task cancelled")
        return {"messages": [HumanMessage(content="No input received", name="System")]}
    except Exception as e:
        print(f"[human_node] Error: {e}")
        return {"messages": [HumanMessage(content="An error occurred", name="System")]}
