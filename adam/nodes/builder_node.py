"""
Builder Node
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

from agents.agent_builder import agent_builder

async def builder_node(state):
    """
    """
    print("###Builder Node###\n")

    agent_blueprint = state["agent_blueprints"][-1]
    subject = state["subject"]

    builder_chain = await agent_builder()

    meta_prompt = builder_chain.invoke({"subject": [subject], "agent_blueprint": [agent_blueprint]})
    print(f"meta prompt: {meta_prompt}\n")

    state["agent_blueprints"][-1]["system_prompt"] = meta_prompt

    builder_message = HumanMessage(content="Building Meta-Agents...", name="Builder")
    state["messages"].append(builder_message)

    return state
