"""Module for creating agent blueprints.
"""
import sys
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_DIRECTORY = os.getenv("PROJECT_DIRECTORY")
sys.path.insert(1, PROJECT_DIRECTORY)  # Include project directory in the system path for module imports

from pydantic import BaseModel, Field, confloat
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class AgentBlueprint(BaseModel):
    """Data model for creating a blueprint for an agent."""
    personality: str = Field(description="The personality of the agent.")
    role: str = Field(description="The role of the agent.")
    temperament: str = Field(description="The temperament of the agent.")
    temperature: confloat(ge=0.0, le=1.0) = Field(
        description="The temperature of the agent, constrained between 0.0 and 1.0."
    )
    name: str = Field(description="A short and witty nickname for the agent that describes their characteristics.")

async def blueprinter():

    system_prompt = (
        "Your are a creative agent that designs the blueprints for a team of agents that all have "
        "unique talents and qualities. The agents are all experts on {subject} or related fields. "
        "Your goal is to create a cohesive team of agents that complement each other and work well "
        "together though may occasionally argue or squabble. They are definitely happy to share "
        "differences of opinion and may even have heated debates.\n\n"
        "Each agent will have the following attributes: \n"
        "* Personality:  The core traits that define how the agentthinks, feels, and behaves "
        "across situations, shaping their overall identity (e.g., shy, confident, quirky).\n"
        "* Role: The specific responsibilities and tasks the agent is assigned to perform.\n"
        "* Temperament: The agent's emotional and behavioral responses to different situations.\n"
        "* Temperature: The level of creativity and uniqueness in the agent's responses.\n"
        "* Name: A short and witty nickname for the agent that describes their characteristics.\n\n"
        "The existing agents are: \n{existing_agents}"
    )

    # Initialize the language model with zero randomness for consistent outputs
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    # Structure the LLM's response using the AgentBlueprint model
    structured_llm = llm.with_structured_output(AgentBlueprint)

    # Here we are creating a ChatPromptTemplate that only has one message in it. This message is a placeholder
    # for the human's response that needs to be analysed.
    blueprinter_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "The topic the team are being assigned to discuss is: {rewritten_prompt}")
        ]
    )

    blueprinter_chain = blueprinter_prompt | structured_llm  # Chain the prompt template with the structured language model

    return blueprinter_chain