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

from agents.analyser import analyser

async def analyser_node(state):
    """
    """
    print("###Analyser Node###\n")
    #print(f"state at analyser node: {state}")
    human_response = state["messages"][-1]
    ic(human_response)
    analyser_chain = await analyser(state)

    #not sure if human response needs []
    analyser_response = analyser_chain.invoke({"human_response": [human_response]})
    ic(analyser_response)
    analyser_decision = analyser_response.next_action
    print(f"analyser: {analyser_decision}\n")
    analyser_message = HumanMessage(content=f"Deciding what to do next...", name="Analyser")
    state["messages"].append(analyser_message)
    state["analyser_decision"] = analyser_decision
    return state
