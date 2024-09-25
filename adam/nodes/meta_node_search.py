"""
Meta Node Search
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
from agents.meta_search import meta_search

async def meta_node_search(meta_state):
    """
    """
    print("###Meta Node Search###\n")

    meta_messages = meta_state["meta_messages"]
    prompt = meta_messages[0].content

    search_agent = await meta_search()
##DEFINE PROMPT
    search_result = search_agent.invoke({"input": prompt})

    print(search_result['output'])

    search_message = HumanMessage(content=search_result['output'], name="meta_search")    

    meta_state["meta_messages"].append(search_message)

    return meta_state
