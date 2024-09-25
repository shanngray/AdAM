"""
Meta Supervisor Node
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

# Retrieve the project directory path from environment variables
PROJECT_DIRECTORY = os.getenv("PROJECT_DIRECTORY")

# Insert the project directory into the system path for module resolution
sys.path.insert(1, PROJECT_DIRECTORY)

from langchain_core.messages import HumanMessage
from agents.meta_supervisor import meta_supervisor

async def meta_node_supervisor(meta_state):
    """
    """
    print("###Meta Supervisor Node###\n")

    meta_messages = meta_state["meta_messages"]
    subject = meta_state["subject"]

    meta_supervisor_chain = await meta_supervisor()

    #not sure if human response needs []
    meta_supervisor_response = meta_supervisor_chain.invoke({"meta_messages": meta_messages, "subject": [subject]})
    print(f"meta supervisor: {meta_supervisor_response}\n")    
    meta_supervisor_decision = meta_supervisor_response.next_action
    print(f"meta supervisor: {meta_supervisor_decision}\n")

    meta_state["meta_supervisor_decision"] = meta_supervisor_decision
    meta_state["meta_messages"].append(HumanMessage(content="Supervisor deciding...", name="meta_supervisor"))
    return meta_state
