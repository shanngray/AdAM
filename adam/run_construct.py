from fastapi import WebSocket
from langchain_core.messages import HumanMessage
from adam.constructor_graph import constructflow
from adam.database import db, MessageModel, MetaAgentModel
from adam.connection_manager import manager

import json
async def run_construct(inputs: dict, websocket: WebSocket, data: str, thread: dict):
    """
    Processes the conversation graph asynchronously.
    """
    from adam.server import main_graph
    json_message = json.loads(data)
    user_input = json_message.get("content")
    print(f"[process_graph] Started for {websocket} with message: {json_message}")
    if user_input:
        print(f"[process_graph] user_input: {user_input}\n")
        async for output in main_graph.astream(inputs, thread, stream_mode="updates"):
            for node, state in output.items():
                print(f"[process_graph] <NODE: {node}>\n")
                #print(f"[process_graph] STATE IN FOR LOOP: {state}")
                #print(f"rewritten_prompt: {state['rewritten_prompt']}")
                if node == "human_node":
                    print(f"[process_graph] human_node called (graph loop)")
                    print(f"[process_graph] human_node_content: {json_message['content']}")

                # Handle messages
                if 'messages' in state:
                    last_message = state['messages'][-1]
                    print(f"[process_graph] {last_message.name}: \"{last_message.content}\"\n")
                    
                    await manager.send_personal_message(
                        json.dumps({
                            "conversation_id": json_message["conversation_id"],
                            "message": last_message.content,
                            "sender_name": last_message.name,
                            "type": "new_message",  # client-side type
                            "conversation_state": "user_input"
                        }), 
                        websocket
                    )
                    
                    node_message = MessageModel(
                        conversation_id=json_message["conversation_id"],
                        message=last_message.content,
                        sender_name=last_message.name,
                        type="outer"
                    )
                    await db.add_message(node_message)
                else:
                    print("[process_graph] No messages found in state.\n")
                
                # Handle agent blueprints
                if state.get('agent_blueprints'):
                    new_agent = state['agent_blueprints'][-1]  # Get the latest agent
                    blueprint_id = len(state['agent_blueprints'])
                    print(f"[process_graph] agent_blueprint: {new_agent['name']}")
                    
                    await manager.send_personal_message(
                        json.dumps({
                            "conversation_id": json_message["conversation_id"],
                            "agent_blueprints": [new_agent],  # Send as a list with a single agent
                            "blueprint_id": blueprint_id,
                            "type": "agent_blueprints",
                        }), 
                        websocket
                    )
                    
                    if node == "builder_node":
                        node_agent = MetaAgentModel(
                            conversation_id=json_message["conversation_id"],
                            name=new_agent['name'],
                            personality=new_agent['personality'],
                            temperament=new_agent['temperament'],
                            temperature=new_agent['temperature'],
                            role=new_agent['role'],
                            url=new_agent['url'],
                            system_prompt=new_agent['system_prompt']
                        )
                        await db.add_meta_agent(node_agent)
                else:
                    print("[process_graph] No agent blueprints found in state.\n")  

                # Update conversation
                update_conv = await db.update_conversation(
                    json_message["conversation_id"], 
                    conversation_state="user_input",
                    rewritten_prompt=state.get("rewritten_prompt"),
                    analyser_decision=state.get("analyser_decision"),
                    conversation_name=state.get("conversation_name"),
                    subject=state.get("subject"),
                )
                
                updated_fields = {
                    "conversationState": "user_input", 
                    "rewrittenPrompt": state.get("rewritten_prompt"),
                    "analyserDecision": state.get("analyser_decision"),
                    "conversationName": state.get("conversation_name"),
                    "subject": state.get("subject"),
                }
                
                if update_conv:
                    print("sending updated conversation to web client.")
                    print(f"updated_fields: {updated_fields}")
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "conversation_updated",
                            "conversation_id": json_message["conversation_id"],
                            "updated_fields": updated_fields
                        }), 
                        websocket
                    )
    else:
        print("[process_graph] No user input found.\n")