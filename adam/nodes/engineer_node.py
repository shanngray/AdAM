"""The engineer node will house the agent responsible for using prompt engineering techniques to
re-engineer the initial prompt from the human. This is first node in the graph (also known as the
"Graph Entry Point").
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Retrieve the project directory path from environment variables
#PROJECT_DIRECTORY = os.getenv("PROJECT_DIRECTORY")

# Insert the project directory into the system path for module resolution
#sys.path.insert(1, PROJECT_DIRECTORY)

from langchain_core.messages import HumanMessage
from adam.agents.engineer import engineer

async def engineer_node(state):
    """
    Rewrite the user prompt using prompt engineering techniques.

    Args:
        state (dict): The current state of the application, expected to contain
                      a list of messages under the key "messages".

    Returns:
        dict: A dictionary with the rewritten user story encapsulated as a HumanMessage
              and the identifier of the last node processed.
    """

    print("###Engineer Node###\n")

    # Extract the current prompt from the state
    prompt = state["messages"]
    
    # Initialize the engineer agent with the current state
    engineer_chain = await engineer(state)
    
    engineer_output = await engineer_chain.ainvoke({"messages": prompt})

    # Wrap the rewritten prompt in a HumanMessage object for standardized handling
    engineer_message = HumanMessage(content=engineer_output, name="engineer")

    # Return the rewritten message
    state["rewritten_prompt"] = engineer_output
    state["messages"].append(engineer_message)
    return state
