import os
from dotenv import load_dotenv
from icecream import ic
from langchain_core.messages import HumanMessage

load_dotenv(".env")

from agents.artist import artist

async def artist_node(state):
    """
    Adds a portrait URL to the latest agent blueprint in the state.
    """
    print("### Artist Node ###\n")
    print(f"State at artist node: {state}")
    
    # Generate the portrait URL using the artist function
    portrait_url = await artist(state["agent_blueprints"][-1])
    
    # Add the portrait URL to the last agent blueprint
    state["agent_blueprints"][-1]["url"] = portrait_url
    
    # Optional: Add a message to the conversation indicating the portrait creation
    from langchain_core.messages import HumanMessage

    portrait_message = HumanMessage(
        content=f"Portrait created for agent '{state['agent_blueprints'][-1]['name']}' at URL: {portrait_url}",
        name="Artist"
    )
    state["messages"].append(portrait_message)
    
    return state
