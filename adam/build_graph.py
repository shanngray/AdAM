"""
This module sets up a state graph for a project workflow, defining various nodes and edges that represent 
different states and transitions in the workflow.
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

from langgraph.graph import END, StateGraph
from state import State
from nodes.engineer_node import engineer_node
from nodes.analyser_node import analyser_node
from nodes.human_node import human_node
from nodes.subject_node import subject_node
from nodes.builder_node import builder_node
from nodes.meta_node_one import meta_node_one
from nodes.meta_node_two import meta_node_two
from nodes.meta_node_supervisor import meta_node_supervisor

from edges.analyser_edge import analyser_edge
from edges.supervisor_edge import supervisor_edge

# Initialize the state graph with the base state
# StateGraph: A graph structure that manages states and transitions.
# State: The base state class used for initializing the graph.
metaflow = StateGraph(State)

# Add nodes to the graph, each node will house an agent or tool within the graph
metaflow.add_node("engineer_node", engineer_node)
metaflow.add_node("analyser_node", analyser_node)
metaflow.add_node("human_node", human_node)
metaflow.add_node("subject_node", subject_node)
metaflow.add_node("builder_node", builder_node)
metaflow.add_node("meta_node_one", meta_node_one)
metaflow.add_node("meta_node_two", meta_node_two)
metaflow.add_node("meta_node_supervisor", meta_node_supervisor)

# add_conditional_edges: Adds edges to the graph that are conditional based on the outcome of a node.
# The first argument is the source node, the second is the function that determines the edge to take,
# and the third is a dictionary of nodes to use as the destination. The keys in the dictionary are the
# possible output strings from the edge function, and the values are the names of the nodes that the edge will go to.
# The flow branches after the analyser node. The analyser_edge function determines which branch (or edge) will be taken.
metaflow.add_conditional_edges("analyser_node", analyser_edge, {"Try Again": "engineer_node", "Proceed": "subject_node"})
# The flow branches after the analyser node. The analyser_edge function determines which branch (or edge) will be taken.
metaflow.add_conditional_edges("meta_node_supervisor", supervisor_edge, {"Continue": "meta_node_one", "Stop": END})

# Standard edges. These are used where the flow always takes the same path between nodes/agents.
# The source node is always on the left and the destination node is always on the right.
# So the output from the engineer always goes to the human. The response from the human then
# always goes to the analyser node, but then the analyser node has a conditional edge after it that can
# either go back to the engineer (if the human had feedback that needs to be incorporated into the prompt)
# or go to the subject node (if the human was happy with the re-engineered prompt).
metaflow.add_edge("engineer_node", "human_node")  # Direct transition from engineer to human
metaflow.add_edge("human_node", "analyser_node")  # Direct transition from human to analyser
metaflow.add_edge("subject_node", "builder_node") # Transition from subject to builder
metaflow.add_edge("builder_node", "meta_node_one") # Transition from builder to meta_node_one
metaflow.add_edge("meta_node_one", "meta_node_two") # Transition from meta_node_one to meta_node_two
metaflow.add_edge("meta_node_two", "meta_node_supervisor") # Transition from meta_node_two to meta_node_supervisor

# Set the initial node where the graph processing will start.
metaflow.set_entry_point("engineer_node")
