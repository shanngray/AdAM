from typing import List, Dict
import asyncio
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # Maps WebSocket ID to its input queue
        self.input_queues: Dict[int, asyncio.Queue] = {}
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> int:
        await websocket.accept()
        ws_id = id(websocket)
        self.active_connections[ws_id] = websocket
        self.input_queues[ws_id] = asyncio.Queue()
        print(f"[ConnectionManager] WebSocket connected: ID {ws_id}")
        return ws_id

    async def disconnect(self, ws_id: int):
        websocket = self.active_connections.get(ws_id)
        if websocket:
            del self.active_connections[ws_id]
            del self.input_queues[ws_id]
            print(f"[ConnectionManager] WebSocket disconnected: ID {ws_id}")

    async def receive_input(self, ws_id: int, input_data: str):
        queue = self.input_queues.get(ws_id)
        if queue:
            await queue.put(input_data)
            print(f"[ConnectionManager] Input enqueued for WebSocket ID {ws_id}: {input_data}")
        else:
            print(f"[ConnectionManager] No input queue found for WebSocket ID {ws_id}")

    async def send_personal_message(self, message: str, ws_id: int):
        websocket = self.active_connections.get(ws_id)
        if websocket:
            await websocket.send_text(message)
            print(f"[ConnectionManager] Sent message to WebSocket ID {ws_id}: {message}")

manager = ConnectionManager()