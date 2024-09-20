"""
Meta Node Two
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
from agents.meta_two import meta_two

async def meta_node_two(meta_state):
    """
    """
    print("###Meta Node Two###\n")

    meta_messages = meta_state["meta_messages"]

    meta_two_chain = await meta_two(meta_state)

    meta_two_response = meta_two_chain.invoke({"messages": meta_messages})

    # Wrap the rewritten prompt in a HumanMessage object for standardized handling
    meta_two_message = HumanMessage(content=meta_two_response, name="meta_two")
    
    print(f"meta two: {meta_two_response}\n")
    return {"meta_messages": [meta_two_message]}
    