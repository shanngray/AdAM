from typing import List, Dict
import asyncio
from fastapi import WebSocket
from starlette.websockets import WebSocketState

class ConnectionManager:
    def __init__(self):
        # Maps WebSocket to its input queue
        self.input_queues: Dict[WebSocket, asyncio.Queue] = {}
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.input_queues[websocket] = asyncio.Queue()
        print(f"[ConnectionManager] WebSocket connected: {websocket}")

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            del self.input_queues[websocket]
            print(f"[ConnectionManager] WebSocket disconnected: {websocket}")

    async def receive_input(self, websocket: WebSocket, input_data: str):
        queue = self.input_queues.get(websocket)
        if queue:
            await queue.put(input_data)
            print(f"[ConnectionManager] Input enqueued for {websocket}: {input_data}")
        else:
            print(f"[ConnectionManager] No input queue found for {websocket}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        if websocket.application_state == WebSocketState.CONNECTED:
            try:
                await websocket.send_text(message)
                print(f"[ConnectionManager] Sent message to {websocket}: {message}")
            except RuntimeError as e:
                print(f"RuntimeError while sending message: {e}")
        else:
            print(f"[ConnectionManager] Cannot send message, WebSocket state: {websocket.application_state}")

manager = ConnectionManager()