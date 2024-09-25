import asyncio
from fastapi import WebSocket

async def human_web_input(websocket: WebSocket):
    """
    Function to act as a conduit between the server and the LLM, awaiting
    the server to receive the message from the web client and send it to the LLM.

    Args:
        websocket (WebSocket): The WebSocket connection.

    Returns:
        str: The message content from the human.
    """
    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == "post_message":
                return data["content"]
    except Exception as e:
        raise ValueError(f"Error processing user input: {str(e)}")
