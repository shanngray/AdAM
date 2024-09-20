"""
Meta Node One
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
from agents.meta_one import meta_one

async def meta_node_one(meta_state):
    """
    """
    print("###Meta Node One###\n")

    meta_messages = meta_state["meta_messages"]

    meta_one_chain = await meta_one(meta_state)

    meta_one_response = meta_one_chain.invoke({"messages": meta_messages})

    # Wrap the rewritten prompt in a HumanMessage object for standardized handling
    meta_one_message = HumanMessage(content=meta_one_response, name="meta_one")
    
    print(f"meta one: {meta_one_response}\n")

    # We return both the rewritten_prompt and meta_one's response in meta_messages.
    return {"meta_messages": [meta_one_message]}
