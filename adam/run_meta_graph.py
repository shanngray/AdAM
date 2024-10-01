from fastapi import WebSocket
from langchain_core.messages import HumanMessage
from adam.meta_graph import build_metaflow
from adam.database import db, MessageModel, ConversationModel
from adam.connection_manager import manager
from icecream import ic

import json

async def run_meta_graph(conversation_id: int, websocket: WebSocket, data: str, thread: dict):
    """
    Processes the meta graph asynchronously.
    """
    print("RUN META GRAPH")
    # from adam.run_construct import updated_fields
    
    conversation = await db.get_conversation(conversation_id)
    meta_agent_models = await db.get_meta_agents(conversation_id)
    meta_agents = [meta_agent.dict() for meta_agent in meta_agent_models]

    if conversation is None:
        print(f"Conversation with id {conversation_id} not found")
        return

    start_meta_messages = conversation.rewritten_prompt
    subject = conversation.subject

    meta_graph = build_metaflow(meta_agents)

    inputs = {
        "meta_messages": [HumanMessage(content=start_meta_messages, name="human")], 
        "subject": subject,
        "meta_agents": meta_agents
    }

    async for output in meta_graph.astream(inputs, thread, stream_mode="updates"):
        for node, meta_state in output.items():
            print(f"<META NODE: {node}>\n")
            if 'meta_messages' in meta_state:
                print(f"{meta_state['meta_messages'][-1].name}: \"{meta_state['meta_messages'][-1].content}\"\n")
                await manager.send_personal_message(json.dumps({
                    "conversation_id": conversation_id,
                    "message": meta_state['meta_messages'][-1].content,
                    "sender_name": meta_state['meta_messages'][-1].name,
                    "type": "new_message",  # client-side type
                    "conversation_state": "user_input"
                }), websocket)
                node_message = MessageModel(
                    conversation_id=conversation_id,
                    message=meta_state['meta_messages'][-1].content,
                    sender_name=meta_state['meta_messages'][-1].name,
                    type="inner"
                )
                new_msg = await db.add_message(node_message)                
            else:
                print("META: No meta messages found in state.\n")

    return
