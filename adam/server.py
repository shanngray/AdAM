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
from adam.meta_graph import build_metaflow

router = APIRouter()
construct_thread = {"configurable": {"thread_id": "1"}}
meta_thread = {"configurable": {"thread_id": "2"}}
construct_memory = MemorySaver()
main_graph = constructflow.compile(checkpointer=construct_memory, interrupt_after=["human_node"])

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    print("[WebSocket] Client connected")
    try:
        while True:
            try:
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
                        "messages": [HumanMessage(content=user_input, name="human")],
                        "agent_blueprints": [],
                        "meta_team_size": 4
                    }
                    asyncio.create_task(run_construct(inputs, websocket, data, construct_thread))
                    print("--Interupt before Human Node--")
                    #print(main_graph.get_state(thread))

                elif json_message["type"] == "user_input":
                    print(f"[WebSocket] Handling user_input: {json_message['content']}")
                    conversation_id = json_message["conversation_id"]
                    db_message = MessageModel(
                        conversation_id=conversation_id,
                        message=json_message["content"],
                        sender_name=json_message["sender_name"],
                        type="outer"
                    )
                    new_msg = await db.add_message(db_message)
                    human_msg = HumanMessage(content=json_message["content"], name="human")

                    # Add the human message to the construct graph
                    main_graph.update_state(construct_thread, {"messages": [human_msg]}, as_node="human_node")
                    print("--Inspect Updated State--")
                    print(main_graph.get_state(construct_thread))
                    
                    # Create the construct_task
                    print("\n\n### RESTARTING CONSTRUCT GRAPH ###\n\n")
                    construct_task = asyncio.create_task(run_construct(None, websocket, data, construct_thread))
                    
                    # Loop to ensure construct_task completes before running meta_task
                    while True:
                        done, pending = await asyncio.wait(
                            [construct_task],
                            timeout=10,
                            return_when=asyncio.FIRST_COMPLETED
                        )
                        
                        if pending:
                            print("[WebSocket] construct_task is still pending, waiting 10 seconds...")
                            await asyncio.sleep(10)
                        if done:
                            print("[WebSocket] construct_task completed, running meta_task")
                            print("\n\n### STARTING META GRAPH ###\n\n")
                            meta_agent_models = await db.get_meta_agents(conversation_id)
                            meta_agents = [meta_agent.dict() for meta_agent in meta_agent_models]
                            metagraph = build_metaflow(meta_agents)
                            meta_task = asyncio.create_task(run_meta_graph(metagraph, conversation_id, websocket, data, meta_thread, "start"))
                            await meta_task
                            break  # Exit the loop after meta_task completes

                elif json_message["type"] == "meta_agent_input":
                    print(f"[WebSocket] Handling meta_agent_input: {json_message['content']}")
                    conversation_id = json_message["conversation_id"]
                    db_message = MessageModel(
                        conversation_id=conversation_id,
                        message=json_message["content"],
                        sender_name=json_message["sender_name"],
                        type="inner"
                    )
                    new_msg = await db.add_message(db_message)
                    human_msg = HumanMessage(content=json_message["content"], name="human")

                    metagraph.update_state(meta_thread, {"messages": [human_msg]}, as_node="meta_human_node")
                    print("--Meta State after update--")
                    print(metagraph.get_state(meta_thread))
                    
                    # Create the construct_task
                    meta_task = asyncio.create_task(run_meta_graph(metagraph, conversation_id, websocket, data, meta_thread, "continue"))
                    await meta_task

                elif json_message["type"] == "get_latest_conversation":
                    print("[WebSocket] Handling get_latest_conversation")
                    latest_conversation_id = await db.get_latest_conversation_id()
                    if latest_conversation_id:
                        async with db.session() as session:
                            conversation = await db.get_conversation(latest_conversation_id)
                            print(f"conversation: {conversation}")
                            if conversation:
                                # Send the latest conversation details
                                await manager.send_personal_message(json.dumps({
                                    "type": "latest_conversation",
                                    "data": {
                                        "conversationId": conversation.id,
                                        "conversationName": conversation.conversation_name,
                                        "conversationState": conversation.conversation_state,
                                        "subject": conversation.subject,
                                        "rewrittenPrompt": conversation.rewritten_prompt,
                                    }
                                }), websocket)

                                # **New Addition**: Send agent_blueprints for the conversation
                                meta_agent_models = await db.get_meta_agents(conversation.id)
                                meta_agents = [agent.dict() for agent in meta_agent_models]
                                await manager.send_personal_message(json.dumps({
                                    "type": "agent_blueprints",
                                    "data": meta_agents
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
                    
                    conversation = ConversationModel(
                        conversation_name=json_message.get("name"),
                        subject=json_message.get("subject", "Default Subject"),
                        rewritten_prompt=json_message.get("rewritten_prompt", "Default Rewritten Prompt"),
                        analyser_decision=json_message.get("analyser_decision", "Pending"),
                    )
                    
                    new_conv = await db.add_conversation(conversation)
                    print(f"new_conv: {new_conv}")

                    # Add initial message from AdAM
                    initial_message = MessageModel(
                        conversation_id=new_conv.id,
                        sender_name="AdAM",
                        message="How can I help you?",
                        type="outer"
                    )
                    new_msg_id = await db.add_message(initial_message)

                    # Send new conversation and initial message to the client
                    await manager.send_personal_message(json.dumps({
                        "type": "new_conversation",
                        "data": {
                            "conversationId": new_conv.id, 
                            "conversationName": new_conv.conversation_name,
                            "initialMessage": {
                                "id": new_msg_id,
                                "sender_name": "AdAM",
                                "message": "How can I help you?",
                                "type": "outer"
                            }
                        }
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
                print("[WebSocket] Client disconnected")
                await manager.disconnect(websocket)
                break
            except json.JSONDecodeError:
                print("[WebSocket] Received invalid JSON data")
                continue
            except Exception as e:
                print(f"[WebSocket] Unexpected error: {str(e)}")
                continue

    except Exception as e:
        print(f"[WebSocket] Fatal error in websocket connection: {str(e)}")
    finally:
        await manager.disconnect(websocket)
        print("[WebSocket] Connection closed")



if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router, prefix="/server")  # Adjust the prefix as needed
    uvicorn.run(app, host="0.0.0.0", port=8080)