"""
Meta Graph Node
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
from meta_graph import build_metaflow

async def meta_graph_node(state):
    """
    """
    print("###Meta Graph Node###\n")

    adam_message = HumanMessage(content="Starting meta analysis...", name="AdAM")

    state["messages"].append(adam_message)

    return state
