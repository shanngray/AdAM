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

    plan = state["plan"]
    start_meta_messages = state["rewritten_prompt"]
    meta_prompt_one = state["meta_prompt_one"]
    meta_prompt_two = state["meta_prompt_two"]

    inputs = {
        "meta_messages": [HumanMessage(content=start_meta_messages, name="human")], 
        "plan": plan, 
        "meta_prompt_one": meta_prompt_one, 
        "meta_prompt_two": meta_prompt_two
        }

    metagraph = build_metaflow(plan)

    async for output in metagraph.astream(inputs, stream_mode="updates"):
        for node, meta_state in output.items():
            # Note how the print statements here appear after any print statements within the node and agent
            # functions. I think this is because the output is being streamed to the console in real-time.
            print(f"<NODE: {node}>\n")
            if 'meta_messages' in meta_state:
                print(f"{meta_state['meta_messages'][-1].name}: \"{meta_state['meta_messages'][-1].content}\"\n")
            else:
                print("No meta messages found in state.\n")

    return 

