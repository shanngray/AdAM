"""
Meta Supervisor Node
"""
import sys
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

# Retrieve the project directory path from environment variables
PROJECT_DIRECTORY = os.getenv("PROJECT_DIRECTORY")

# Insert the project directory into the system path for module resolution
sys.path.insert(1, PROJECT_DIRECTORY)

#TODO: pull out sanitize name to a utils file and santize the names as they are created
def sanitize_name(name):
    """Sanitize the name to comply with OpenAI's API requirements."""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

from langchain_core.messages import HumanMessage
from agents.meta_supervisor import meta_supervisor

async def meta_node_supervisor(meta_state):
    """
    Meta Supervisor Node function
    """
    print("###Meta Supervisor Node###\n")

    meta_messages = meta_state["meta_messages"]
    meta_agents = meta_state["meta_agents"]

    # Sanitize agent names in the roster
    agent_roster = {sanitize_name(agent["name"]): agent["role"] for agent in meta_agents}
    agent_roster["user"] = "The user tends to get lonely. Make sure you include them in the conversation."
    agent_roster["meta_search"] = "This special agent is only used when the need is dire and can search the internet for information."

    agent_list = list(agent_roster.keys())

    # Sanitize names in meta_messages
    for message in meta_messages:
        if hasattr(message, 'name'):
            message.name = sanitize_name(message.name)

    meta_supervisor_chain = await meta_supervisor(agent_list)

    meta_supervisor_response = meta_supervisor_chain.invoke(
        {
            "meta_messages": meta_messages, 
            "agent_roster": agent_roster, 
            "agent_list": agent_list
        }
    )

    print(f"meta supervisor: {meta_supervisor_response}\n")    
    meta_supervisor_decision = meta_supervisor_response.next
    print(f"meta supervisor: {meta_supervisor_decision}\n")

    meta_state["meta_supervisor_decision"] = meta_supervisor_decision
    meta_state["meta_messages"].append(HumanMessage(content="Supervisor deciding...", name="meta_supervisor"))
    return meta_state
