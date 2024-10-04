"""

"""
import sys
import os
from dotenv import load_dotenv
from icecream import ic
from langchain_core.messages import HumanMessage

# Load environment variables from .env file
load_dotenv(".env")

# Retrieve the project directory path from environment variables
PROJECT_DIRECTORY = os.getenv("PROJECT_DIRECTORY")

# Insert the project directory into the system path for module resolution
sys.path.insert(1, PROJECT_DIRECTORY)

from agents.blueprinter import blueprinter

async def blueprinter_node(state):
    """
    """
    print("###Blueprinter Node###\n")
    #print(f"state at blueprinter node: {state}")
    blueprinter_chain = await blueprinter()

    rewritten_prompt = state["rewritten_prompt"]
    subject = state["subject"]
    existing_agents = state["agent_blueprints"]

    blueprinter_response = blueprinter_chain.invoke(
        {
            "rewritten_prompt": [rewritten_prompt], 
            "subject": subject, 
            "existing_agents": [existing_agents]
        }
    )
    ic(blueprinter_response) # Should be instance of AgentBlueprint
    blueprinter_dict = blueprinter_response.dict()
    print(f"blueprinter: {blueprinter_dict}\n")
    blueprinter_message = HumanMessage(content=f"Creating agent blueprint...", name="Blueprinter")
    state["messages"].append(blueprinter_message)
    state["agent_blueprints"].append(blueprinter_dict)
    return state