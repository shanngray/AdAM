"""
Meta Graph
"""
import sys
import os
import functools
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables from .env file
load_dotenv(".env")

# Retrieve the project directory path from environment variables
PROJECT_DIRECTORY = os.getenv("PROJECT_DIRECTORY")

# Insert the project directory into the system path for module resolution
sys.path.insert(1, PROJECT_DIRECTORY)

from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from states import Meta_State
from nodes.meta_node_supervisor import meta_node_supervisor
from nodes.meta_node_search import meta_node_search
from nodes.meta_human_node import meta_human_node

from agents.meta_agent_helper import meta_agent_helper
from nodes.meta_node_helper import meta_node_helper

from edges.supervisor_edge import supervisor_edge
from edges.human_edge import human_edge


def build_metaflow(meta_agents):
    
    meta_agents_dict = {}
    meta_nodes_dict = {}

    metaflow = StateGraph(Meta_State)

    metaflow.add_node("meta_node_supervisor", meta_node_supervisor)
    metaflow.add_node("meta_human_node", meta_human_node)
    metaflow.add_node("meta_node_search", meta_node_search)
    metaflow.add_edge("meta_node_search", "meta_node_supervisor")

    for num, meta_agent in enumerate(meta_agents):
        meta_agents_dict[num] = meta_agent_helper(meta_agent)
        meta_nodes_dict[num] = functools.partial(meta_node_helper, agent=meta_agents_dict[num], name=meta_agent["name"])
        metaflow.add_node(f"meta_node_{meta_agent['name']}", meta_nodes_dict[num])
        metaflow.add_edge(f"meta_node_{meta_agent['name']}", "meta_node_supervisor")

    conditional_edges = {meta_agent['name']: f"meta_node_{meta_agent['name']}" for meta_agent in meta_agents}
    conditional_edges["user"] = "meta_human_node"
    conditional_edges["meta_search"] = "meta_node_search"

    metaflow.add_conditional_edges(
        "meta_node_supervisor", 
        supervisor_edge, 
        conditional_edges
    )

    metaflow.add_conditional_edges("meta_human_node", human_edge, {"Continue": "meta_node_supervisor", "Stop": END})

    metaflow.set_entry_point("meta_node_supervisor") 

    meta_memory = MemorySaver()
    
    return metaflow.compile(checkpointer=meta_memory, interrupt_after=["meta_human_node"])