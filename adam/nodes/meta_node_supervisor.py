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

from agents.meta_supervisor import meta_supervisor

def meta_node_supervisor(state):
    """
    """
    print("###Meta Supervisor Node###\n")

    meta_messages = state["meta_messages"]
    subject = state["subject"]

    meta_supervisor_chain = meta_supervisor(state)

    #not sure if human response needs []
    meta_supervisor_response = meta_supervisor_chain.invoke({"meta_messages": meta_messages, "subject": [subject]})
    
    meta_supervisor_decision = meta_supervisor_response.next_action
    print(f"meta supervisor: {meta_supervisor_decision}\n")
    return {"meta_supervisor_decision": meta_supervisor_decision}
