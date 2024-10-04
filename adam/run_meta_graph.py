from fastapi import WebSocket
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph
from adam.database import db, MessageModel, ConversationModel
from adam.connection_manager import manager
from icecream import ic

import json

async def run_meta_graph(metagraph: StateGraph, conversation_id: int, websocket: WebSocket, data: str, thread: dict, context: str):
    """
    Processes the meta graph asynchronously.
    """
    print("RUN META GRAPH")
    # from adam.run_construct import updated_fields
    
    conversation = await db.get_conversation(conversation_id)

    if conversation is None:
        print(f"Conversation with id {conversation_id} not found")
        return

    if context == "start": #if not message is sent, then start with the initial meta_messages
        start_meta_messages = conversation.rewritten_prompt
        subject = conversation.subject
        meta_agent_models = await db.get_meta_agents(conversation_id)
        meta_agents = [meta_agent.dict() for meta_agent in meta_agent_models]
        inputs = {
            "meta_messages": [HumanMessage(content=start_meta_messages, name="human")], 
            "subject": subject,
            "meta_agents": meta_agents
        }
    else: #if message is sent, then add the human_message to the thread
        inputs = None        

    update_conv = await db.update_conversation(
        conversation_id, 
        conversation_state="meta_agent_input",
    )
    updated_fields = {
        "conversationState": "meta_agent_input", 
    }
    
    if update_conv:
        print("Starting Meta Conversation with web client.")
        print(f"updated_fields: {updated_fields}")
        await manager.send_personal_message(json.dumps({
            "type": "conversation_updated",
            "conversation_id": conversation_id,
            "updated_fields": updated_fields
        }), websocket)

    async for output in metagraph.astream(inputs, thread, stream_mode="updates"):
        for node, meta_state in output.items():
            print(f"<META NODE: {node}>\n")
            last_message = meta_state['meta_messages'][-1]
            if 'meta_messages' in meta_state:
                print(f"{last_message.name}: \"{last_message.content}\"\n")
                await manager.send_personal_message(json.dumps({
                    "conversation_id": conversation_id,
                    "message": last_message.content,
                    "sender_name": last_message.name,
                    "type": "new_message",  # client-side type
                    "conversation_state": "meta_agent_input"
                }), websocket)
                node_message = MessageModel(
                    conversation_id=conversation_id,
                    message=last_message.content,
                    sender_name=last_message.name,
                    type="inner"
                )
                new_msg = await db.add_message(node_message)                
            else:
                print("META: No meta messages found in state.\n")

    return
