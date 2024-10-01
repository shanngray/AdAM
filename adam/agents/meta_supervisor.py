"""Module for Meta Supervisor. The meta supervisor decides whether to keep iterating on the prompt or to stop.
"""
import sys
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_DIRECTORY = os.getenv("PROJECT_DIRECTORY")
sys.path.insert(1, PROJECT_DIRECTORY)  # Include project directory in the system path for module imports

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from typing import Literal


async def meta_supervisor(agent_list):
    """
    Meta Supervisor
    """
    class RouteResponse(BaseModel):
        """List of possible agents that the meta supervisor can route to next."""
        next: Literal[*agent_list]


    system_prompt = (
        "Your are an Agentic Maestro. A conductor of AI agents and always know which of the agents"
        " in your team is best placed to respond next. If you are not sure, you ask the user to respond."
        " The agents you can choose from are {{name: role}}: {agent_roster}"
    )

    # Initialize the language model with zero randomness for consistent outputs
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)

    # Structure the LLM's response using the AnalyserResponse model
    structured_llm = llm.with_structured_output(RouteResponse)

    meta_supervisor_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="meta_messages"),
            (
                "system",
                "Given the conversation above, who should act next?"
                " Or should we ask the user to respond? Select one of: {agent_list}",
            ),
        ]
    )

    meta_supervisor_chain = meta_supervisor_prompt | structured_llm  # Chain the prompt template with the structured language model

    return meta_supervisor_chain