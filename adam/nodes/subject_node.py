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

from agents.subject_agent import subject_agent

async def subject_node(state):
    """
    """
    print("###Subject Node###\n")

    rewritten_prompt = HumanMessage(content=state["rewritten_prompt"], name="Human")

    subject_chain = await subject_agent(state)

    #not sure if human response needs []
    subject_response = subject_chain.invoke({"rewritten_prompt": [rewritten_prompt]})
    
    print(f"subject: {subject_response}\n")
    state["subject"] = subject_response
    subject_message = HumanMessage(content=f"Thinking about the subject matter...", name="Subjectifier")
    state["messages"].append(subject_message)

    return state
