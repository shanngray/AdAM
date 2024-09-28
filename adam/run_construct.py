from fastapi import WebSocket
from langchain_core.messages import HumanMessage
from adam.constructor_graph import constructflow
from adam.database import db, MessageModel
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
                print(f"[process_graph] STATE IN FOR LOOP: {state}")
                #print(f"rewritten_prompt: {state['rewritten_prompt']}")
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
                    conversation_state="user_input",
                    rewritten_prompt=state["rewritten_prompt"] if "rewritten_prompt" in state else None,
                    analyser_decision=state["analyser_decision"] if "analyser_decision" in state else None,
                    conversation_name=state["conversation_name"] if "conversation_name" in state else None,
                    subject=state["subject"] if "subject" in state else None,
                    plan=state["plan"] if "plan" in state else None,
                    meta_prompt_one=state["meta_prompt_one"] if "meta_prompt_one" in state else None,
                    meta_prompt_two=state["meta_prompt_two"] if "meta_prompt_two" in state else None
                )
                updated_fields = {
                    "conversationState": "user_input", 
                    "rewrittenPrompt": state["rewritten_prompt"] if "rewritten_prompt" in state else None,
                    "analyserDecision": state["analyser_decision"] if "analyser_decision" in state else None,
                    "conversationName": state["conversation_name"] if "conversation_name" in state else None,
                    "subject": state["subject"] if "subject" in state else None,
                    "plan": state["plan"] if "plan" in state else None,
                    "metaPromptOne": state["meta_prompt_one"] if "meta_prompt_one" in state else None,
                    "metaPromptTwo": state["meta_prompt_two"] if "meta_prompt_two" in state else None
                }
                if update_conv:
                   print("sending updated conversation to web client.")
                   print(f"updated_fields: {updated_fields}")
                   await manager.send_personal_message(json.dumps({
                        "type": "conversation_updated",
                        "conversation_id": json_message["conversation_id"],
                        "updated_fields": updated_fields
                    }), websocket)
    else:
        print("[process_graph] No user input found.\n")