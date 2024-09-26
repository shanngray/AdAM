"""

"""
import sys
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Load environment variables from .env file
load_dotenv(".env")

# Retrieve the project directory path from environment variables
PROJECT_DIRECTORY = os.getenv("PROJECT_DIRECTORY")

# Insert the project directory into the system path for module resolution
sys.path.insert(1, PROJECT_DIRECTORY)

from agents.namer import namer_agent

async def namer_node(state):
    """
    """
    print("###Namer Node###\n")

    rewritten_prompt = HumanMessage(content=state["rewritten_prompt"], name="Human")

    namer_chain = await namer_agent(state)

    #not sure if human response needs []
    namer_response = namer_chain.invoke({"rewritten_prompt": [rewritten_prompt]})
    
    print(f"Namer: {namer_response}\n")
    state["conversation_name"] = namer_response
    namer_message = HumanMessage(content=f"Coming up with a name for the conversation...", name="Namer")
    state["messages"].append(namer_message)

    return state
