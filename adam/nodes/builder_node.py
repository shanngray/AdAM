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

    builder_chain_one = agent_builder(state, "one")
    builder_chain_two = agent_builder(state, "two")

    meta_prompt_one = builder_chain_one.invoke({"subject": [subject]})
    meta_prompt_two = builder_chain_two.invoke({"subject": [subject]})

    print(f"meta prompt: {meta_prompt_one}\n")
    print(f"meta prompt: {meta_prompt_two}\n")

    return {"meta_prompt_one": meta_prompt_one, "meta_prompt_two": meta_prompt_two}
