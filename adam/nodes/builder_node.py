"""
Builder Node
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

from agents.agent_builder import agent_builder

def builder_node(state):
    """
    """
    print("###Builder Node###\n")

    subject = state["subject"]

    builder_chain = agent_builder(state)

    #not sure if human response needs []
    meta_prompt = builder_chain.invoke({"subject": [subject]})
    
    print(f"meta prompt: {meta_prompt}\n")
    return {"meta_prompt": meta_prompt}
