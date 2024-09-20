"""

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

from agents.subject_agent import subject_agent

async def subject_node(state):
    """
    """
    print("###Subject Node###\n")

    rewritten_prompt = state["rewritten_prompt"]

    subject_chain = await subject_agent(state)

    #not sure if human response needs []
    subject_response = subject_chain.invoke({"rewritten_prompt": [rewritten_prompt]})
    
    print(f"subject: {subject_response}\n")
    return {"subject": subject_response}
