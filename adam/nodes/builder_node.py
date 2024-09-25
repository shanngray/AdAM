"""
Builder Node
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

from agents.agent_builder import agent_builder
from agents.planner import planner

async def builder_node(state):
    """
    """
    print("###Builder Node###\n")

    subject = state["subject"]
    rewritten_prompt = state["rewritten_prompt"]

    builder_chain_one = await agent_builder(state, "one")
    builder_chain_two = await agent_builder(state, "two")
    planner_chain = await planner(state)

    meta_prompt_one = builder_chain_one.invoke({"subject": [subject]})
    print(f"meta prompt one: {meta_prompt_one}\n")

    meta_prompt_two = builder_chain_two.invoke({"subject": [subject]})
    print(f"meta prompt two: {meta_prompt_two}\n")
    
    plan = planner_chain.invoke({"rewritten_prompt": [rewritten_prompt]})
    print(f"plan: {plan}\n")
    
    complexity = plan.complexity

    state["meta_prompt_one"] = meta_prompt_one
    state["meta_prompt_two"] = meta_prompt_two
    state["plan"] = complexity
    builder_message = HumanMessage(content="Building Meta-Agents...", name="Builder")
    state["messages"].append(builder_message)

    return state
