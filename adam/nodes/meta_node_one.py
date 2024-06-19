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

def meta_node_one(state):
    """
    """
    print("###Meta Node One###\n")

    rewritten_prompt = state["rewritten_prompt"]

    # We turn the rewritten_prompt into a HumanMessage object and prime the meta_messages variable
    # in the state.
    initial_meta_message = HumanMessage(content=rewritten_prompt, name="human")

    meta_one_chain = meta_one(state)

    meta_one_response = meta_one_chain.invoke({"messages": [initial_meta_message]})

    # Wrap the rewritten prompt in a HumanMessage object for standardized handling
    meta_one_message = HumanMessage(content=meta_one_response, name="meta_one")
    
    print(f"meta one: {meta_one_response}\n")

    # We return both the rewritten_prompt and meta_one's response in meta_messages.
    return {"meta_messages": [initial_meta_message, meta_one_message]}
