from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
import json

from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from adam.database import db, ConversationModel, MessageModel
from adam.constructor_graph import constructflow
from adam.run_construct import run_construct
from adam.run_meta_graph import run_meta_graph
from adam.connection_manager import manager  # Import from the new module
from adam.nodes.human_node import human_node  # Keep if required elsewhere

router = APIRouter()
construct_thread = {"configurable": {"thread_id": "1"}}
meta_thread = {"configurable": {"thread_id": "2"}}
construct_memory = MemorySaver()
main_graph = constructflow.compile(checkpointer=construct_memory, interrupt_before=["human_node", "meta_graph_node"])

async def handle_user_input(websocket: WebSocket):
    """
    Handles user input for a specific WebSocket connection.
    """
    print(f"[handle_user_input] Started for {websocket}")
    input_queue = manager.input_queues.get(websocket)
    if not input_queue:
        print(f"[handle_user_input] Input queue not found for {websocket}")
        return

    while True:
        input_data = await input_queue.get()
        print(f"[handle_user_input] Received input for {websocket}: {input_data}")
        # Instead of directly calling human_node, delegate processing
        # For example, enqueue the state for another handler or trigger an event
        # Here, we'll use asyncio.create_task to handle processing asynchronously
        state = {"websocket": websocket}
        asyncio.create_task(process_human_node(state))

async def process_human_node(state: Dict[str, any]):
    """
    Processes the human_node asynchronously.
    """
    print(f"[process_human_node] Started with state: {state}")
    updated_state = await human_node(state)
    # Further processing with updated_state as needed
    # For example, trigger the next node in the graph
    # This depends on the overall workflow architecture
    print(f"[process_human_node] Updated state from human_node: {updated_state}")
    # Placeholder for next steps

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    print("[WebSocket] Client connected")
    try:
        # Start handling user input for this websocket connection
        # asyncio.create_task(handle_user_input(websocket))

        while True:
            data = await websocket.receive_text()
            print(f"[WebSocket] Received data from {websocket}: {data}")
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
                user_input = json_message.get("content")
                inputs = {
                    "messages": [HumanMessage(content=user_input, name="human")]
                }
                asyncio.create_task(run_construct(inputs, websocket, data, construct_thread))
                print("--Interupt before Human Node--")
                #print(main_graph.get_state(thread))

            elif json_message["type"] == "user_input":
                print(f"[WebSocket] Handling user_input: {json_message['content']}")
                db_message = MessageModel(
                    conversation_id=json_message["conversation_id"],
                    message=json_message["content"],
                    sender_name=json_message["sender_name"],
                    type="outer"
                )
                new_msg = await db.add_message(db_message)
                human_msg = HumanMessage(content=json_message["content"], name="human")
                print("--State before update--")
                print(main_graph.get_state(construct_thread))
                main_graph.update_state(construct_thread, {"messages": [human_msg]}, as_node="human_node")
                print("--State after update--")
                print(main_graph.get_state(construct_thread))
                
                # Create tasks
                construct_task = asyncio.create_task(run_construct(None, websocket, data, construct_thread))
                
                # Wait for the first task to complete
                print("Waiting for construct task to complete")
                done, pending = await asyncio.wait([construct_task], return_when=asyncio.FIRST_COMPLETED)
                
                print("Running meta task")
                # Run the second task
                meta_task = asyncio.create_task(run_meta_graph(json_message["conversation_id"], websocket, data, meta_thread)) 
                await meta_task

            elif json_message["type"] == "get_latest_conversation":
                print("[WebSocket] Handling get_latest_conversation")
                latest_conversation_id = await db.get_latest_conversation_id()
                if latest_conversation_id:
                    async with db.session() as session:
                        conversation = await db.get_conversation(latest_conversation_id)
                        print(f"conversation: {conversation}")
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
                
                # Collect all required fields. Here, we're using default values.
                # Ideally, these should come from the `json_message`.
                conversation = ConversationModel(
                    conversation_name=json_message.get("name"),
                    subject=json_message.get("subject", "Default Subject"),
                    rewritten_prompt=json_message.get("rewritten_prompt", "Default Rewritten Prompt"),
                    meta_prompt_one=json_message.get("meta_prompt_one", "Default Meta Prompt One"),
                    meta_prompt_two=json_message.get("meta_prompt_two", "Default Meta Prompt Two"),
                    analyser_decision=json_message.get("analyser_decision", "Pending"),
                    plan=json_message.get("plan", "Default Plan"),
                )
                
                new_conv = await db.add_conversation(conversation)
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
        await manager.disconnect(websocket)
        print("[WebSocket] Client disconnected")



if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router, prefix="/server")  # Adjust the prefix as needed
    uvicorn.run(app, host="0.0.0.0", port=8080)
