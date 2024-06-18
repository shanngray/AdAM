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

from agents.analyser import analyser

def analyser_node(state):
    """
    """
    print("###Analyser Node###\n")

    human_response = state["messages"][-1]

    analyser_chain = analyser(state)

    #not sure if human response needs []
    analyser_response = analyser_chain.invoke({"human_response": [human_response]})
    
    analyser_decision = analyser_response.next_action
    print(f"analyser: {analyser_decision}\n")
    return {"analyser_decision": analyser_decision}

