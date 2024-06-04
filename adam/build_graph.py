import sys
import os
from dotenv import load_dotenv

load_dotenv(".env")

PROJECT_DIRECTORY = os.getenv("PROJECT_DIRECTORY")

sys.path.insert(1, PROJECT_DIRECTORY)

from langgraph.graph import END, StateGraph

from state import State

from nodes.engineer_node import engineer_node
from nodes.analyser_node import analyser_node
from nodes.human_node import human_node
from nodes.subject_node import subject_node
from edges.analyser_edge import analyser_edge

metaflow = StateGraph(State)

metaflow.add_node("engineer_node", engineer_node)
metaflow.add_node("analyser_node", analyser_node)
metaflow.add_node("human_node", human_node)
metaflow.add_node("subject_node", subject_node)

metaflow.add_conditional_edges("analyser_node", analyser_edge, {"engineer_node": "engineer_node", "subject_node": "subject_node"})

metaflow.add_edge("engineer_node", "human_node")
metaflow.add_edge("human_node", "analyser_node")
metaflow.add_edge("subject_node", END)

metaflow.set_entry_point("engineer_node")


