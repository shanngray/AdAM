from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
import json

from langchain_core.messages import HumanMessage
from adam.database import db, ConversationModel, MessageModel
from adam.constructor_graph import constructflow
from adam.connection_manager import manager  # Import from the new module
from nodes.human_node import human_node  # Keep if required elsewhere

router = APIRouter()

async def handle_user_input(ws_id: int):
    """
    Handles user input for a specific WebSocket connection.
    """
    print(f"[handle_user_input] Started for WebSocket ID {ws_id}")
    input_queue = manager.input_queues.get(ws_id)
    if not input_queue:
        print(f"[handle_user_input] Input queue not found for WebSocket ID {ws_id}")
        return

    while True:
        input_data = await input_queue.get()
        print(f"[handle_user_input] Received input for WebSocket ID {ws_id}: {input_data}")
        # Delegate processing asynchronously
        state = {"ws_id": ws_id}
        asyncio.create_task(process_human_node(state))

async def process_human_node(state: Dict[str, any]):
    """
    Processes the human_node asynchronously.
    """
    ws_id = state.get("ws_id")
    print(f"[process_human_node] Started with state: {state}")
    updated_state = await human_node(state)
    print(f"[process_human_node] Updated state from human_node: {updated_state}")
    # Placeholder for next steps

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    ws_id = await manager.connect(websocket)
    try:
        # Start handling user input for this websocket connection
        asyncio.create_task(handle_user_input(ws_id))

        while True:
            data = await websocket.receive_text()
            print(f"[WebSocket] Received data from WebSocket ID {ws_id}: {data}")
            json_message = json.loads(data)

            # Handle different message types with detailed logs
            if json_message["type"] == "first_message":
                print("[WebSocket] Handling first_message")
                db_message = MessageModel(
                    conversation_id=json_message["conversation_id"],
                    message=json_message["content"],
                    sender_name=json_message["sender_name"],
                    type="outer"
                )
                new_msg = await db.add_message(db_message)
                asyncio.create_task(process_graph(ws_id, json_message))

            elif json_message["type"] == "user_input":
                print(f"[WebSocket] Handling user_input: {json_message['content']}")
                await manager.receive_input(ws_id, json_message["content"])

            elif json_message["type"] == "get_latest_conversation":
                print("[WebSocket] Handling get_latest_conversation")
                latest_conversation_id = await db.get_latest_conversation_id()
                if latest_conversation_id:
                    async with db.session() as session:
                        conversation = await db.get_conversation(latest_conversation_id)
                        if conversation:
                            await manager.send_personal_message(json.dumps({
                                "type": "latest_conversation",
                                "data": {
                                    "conversationId": conversation.id,
                                    "conversationName": conversation.conversation_name,
                                    "conversationState": conversation.conversation_state,
                                    "subject": conversation.subject,
                                    "rewrittenPrompt": conversation.rewritten_prompt,
                                    "metaPromptOne": conversation.meta_prompt_one,
                                    "metaPromptTwo": conversation.meta_prompt_two
                                }
                            }), websocket)
                        else:
                            await manager.send_personal_message(json.dumps({
                                "type": "latest_conversation",
                                "data": None
                            }), websocket)
                else:
                    await manager.send_personal_message(json.dumps({
                        "type": "latest_conversation",
                        "data": None
                    }), websocket)

            elif json_message["type"] == "create_conversation":
                print("[WebSocket] Handling create_conversation")
                new_conv = await db.add_conversation(json_message["name"])
                await manager.send_personal_message(json.dumps({
                    "type": "new_conversation",
                    "data": {"conversationId": new_conv.id, "conversationName": new_conv.conversation_name}
                }), websocket)

            elif json_message["type"] == "update_conversation":
                print("[WebSocket] Handling update_conversation")
                # Update conversation in the database
                conversation_id = json_message["conversation_id"]
                updated_fields = json_message["updated_fields"]
                success = await db.update_conversation(conversation_id, **updated_fields)
                
                if success:
                    # Send only the updated fields back to the client
                    await manager.send_personal_message(json.dumps({
                        "type": "conversation_updated",
                        "conversation_id": conversation_id,
                        "updated_fields": updated_fields
                    }), websocket)
                else:
                    await manager.send_personal_message(json.dumps({
                        "type": "error",
                        "message": "Failed to update conversation."
                    }), websocket)

            elif json_message["type"] == "get_conversations":
                print("[WebSocket] Handling get_conversations")
                conversations = await db.get_conversations()
                await manager.send_personal_message(json.dumps({
                    "type": "conversations",
                    "data": [{"conversationId": conv.id, "conversationName": conv.conversation_name} for conv in conversations]
                }), websocket)

            elif json_message["type"] == "get_conversation_history":
                print("[WebSocket] Handling get_conversation_history")
                history, conversation_state = await db.get_conversation_messages(json_message["conversation_id"])
                await manager.send_personal_message(json.dumps({
                    "type": "conversation_history",
                    "data": [msg.dict() for msg in history],
                    "conversationState": conversation_state
                }), websocket)

            elif json_message["type"] == "get_message":
                print("[WebSocket] Handling get_message")
                msg = await db.get_message(json_message["message_id"])
                if msg:
                    await manager.send_personal_message(json.dumps({
                        "type": "message",
                        "data": msg.dict()
                    }), websocket)

            elif json_message["type"] == "post_message":
                print("[WebSocket] Handling post_message")
                db_message = MessageModel(
                    conversation_id=json_message["conversation_id"],
                    message=json_message["content"],
                    sender_name=json_message["sender_name"],
                    type="outer"
                ) 
                new_msg = await db.add_message(db_message)
                await manager.send_personal_message(json.dumps({
                    "type": "new_message",
                    "data": new_msg.dict()
                }), websocket)

            elif json_message["type"] == "get_latest_conversation_history":
                print("[WebSocket] Handling get_latest_conversation_history")
                latest_conversation_id, conversation_state = await db.get_latest_conversation_id()
                if latest_conversation_id:
                    history, _ = await db.get_conversation_messages(latest_conversation_id)
                    await manager.send_personal_message(json.dumps({
                        "type": "conversation_history",
                        "data": [msg.dict() for msg in history],
                        "conversation_id": latest_conversation_id,
                        "conversationState": conversation_state
                    }), websocket)
                else:
                    await manager.send_personal_message(json.dumps({
                        "type": "conversation_history",
                        "data": [],
                        "conversation_state": None
                    }), websocket)
            else:
                print(f"[WebSocket] Unhandled message type: {json_message['type']}")

    except WebSocketDisconnect:
        await manager.disconnect(ws_id)
        print(f"[WebSocket] Client disconnected: WebSocket ID {ws_id}")

async def process_graph(ws_id: int, json_message: Dict):
    """
    Processes the conversation graph.
    """
    print(f"[process_graph] Processing graph for WebSocket ID {ws_id} with message: {json_message}")

    user_input = json_message.get("content")
    if user_input:
        main_graph = constructflow.compile()
        print(f"[process_graph] user_input: {user_input}\n")
        inputs = {
            "messages": [HumanMessage(content=user_input, name="human")],
            "ws_id": ws_id
        }

        async for output in main_graph.astream(inputs, stream_mode="updates"):
            for node, state in output.items():
                print(f"[process_graph] <NODE: {node}>\n")
                if node == "human_node":
                    print(f"[process_graph] human_node called (graph loop)")
                    print(f"[process_graph] human_node_content: {json_message['content']}")

                if 'messages' in state:
                    print(f"[process_graph] {state['messages'][-1].name}: \"{state['messages'][-1].content}\"\n")
                    await manager.send_personal_message(json.dumps({
                        "conversation_id": json_message["conversation_id"],
                        "message": state['messages'][-1].content,
                        "sender_name": state['messages'][-1].name,
                        "type": "new_message",  # client-side type
                        "conversation_state": "user_input"
                    }), websocket)
                    node_message = MessageModel(
                        conversation_id=json_message["conversation_id"],
                        message=state['messages'][-1].content,
                        sender_name=state['messages'][-1].name,
                        type="outer"
                    )
                    new_msg = await db.add_message(node_message)
                else:
                    print("[process_graph] No messages found in state.\n")
                update_conv = await db.update_conversation(
                    json_message["conversation_id"], 
                    conversation_state="user_input"
                )
                updated_fields = {"conversationState": "user_input"}
                if update_conv:
                    await manager.send_personal_message(json.dumps({
                        "type": "conversation_updated",
                        "conversation_id": json_message["conversation_id"],
                        "updated_fields": updated_fields
                    }), websocket)
                state["websocket"] = websocket
    else:
        print("[process_graph] No user input found.\n")
    '''# Implement the graph processing logic here
    # Ensure to pass the ws_id correctly to maintain context
    # Example placeholder logic:
    state = {"ws_id": ws_id, "data": json_message["content"]}
    updated_state = await human_node(state)
    # Continue with further processing based on updated_state
    print(f"[process_graph] Graph processing updated state: {updated_state}")
    # Example: send a response back to the client
    await manager.send_personal_message(json.dumps({
        "conversation_id": json_message["conversation_id"],
        "message": updated_state["messages"][0].content,
        "sender_name": updated_state["messages"][0].name,
        "type": "processed_message",
        "conversation_state": "processed"
    }), ws_id)'''

if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router, prefix="/server")  # Adjust the prefix as needed
    uvicorn.run(app, host="0.0.0.0", port=8080)
