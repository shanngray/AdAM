"""
Meta Graph
"""
import sys
import os
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
from nodes.meta_node_one import meta_node_one
from nodes.meta_node_two import meta_node_two
from nodes.meta_node_supervisor import meta_node_supervisor
from nodes.meta_node_search import meta_node_search
from edges.supervisor_edge import supervisor_edge

def build_metaflow(plan):
    metaflow = StateGraph(Meta_State)

    metaflow.add_node("meta_node_one", meta_node_one)
    metaflow.add_node("meta_node_two", meta_node_two)
    metaflow.add_node("meta_node_supervisor", meta_node_supervisor)
    
    if plan == "simple":
        metaflow.add_edge("meta_node_one", "meta_node_two")
        metaflow.add_edge("meta_node_two", "meta_node_supervisor")
        metaflow.set_entry_point("meta_node_one")
    elif plan == "complex":
        metaflow.add_node("meta_node_search", meta_node_search)
        metaflow.add_edge("meta_node_search", "meta_node_one")
        metaflow.add_edge("meta_node_one", "meta_node_two")
        metaflow.add_edge("meta_node_two", "meta_node_supervisor")
        metaflow.set_entry_point("meta_node_search")
    
    metaflow.add_conditional_edges("meta_node_supervisor", supervisor_edge, {"Continue": "meta_node_one", "Stop": END})

    meta_memory = MemorySaver()
    
    return metaflow.compile(checkpointer=meta_memory, interrupt_after=["meta_node_supervisor"])