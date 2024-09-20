"""Module for Meta Supervisor. The meta supervisor decides whether to keep iterating on the prompt or to stop.
"""
import sys
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_DIRECTORY = os.getenv("PROJECT_DIRECTORY")
sys.path.insert(1, PROJECT_DIRECTORY)  # Include project directory in the system path for module imports

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_cohere import ChatCohere

# LangChain's BaseModel and Field are derived from pydantic's BaseModel class and Field attribute and can be used to
# enforce structure in an LLM's responses. Here we are using them to ensure that the LLM only responds in one of two
# ways. This can be extremely useful in flow engineering as it allows us to route the flow to the correct node
# without having to worry about variances in the LLM's responses.
class MetaSupervisorResponse(BaseModel):
    """Data model for analysing the meta conversation."""
    next_action: str = Field(description="The next action to be taken: 'Stop' or 'Continue'")

async def meta_supervisor(state):
    """
    Meta Supervisor
    """
    subject = state["subject"]
    meta_supervisor_preamble = (
        "You are the Supervisor for a team of two agents that are experts in {subject}. Your job is to decide whether to keep iterating "
        " on the prompt or to stop. You are to only ever respond with 'Stop' or 'Continue': \n"
        " - 'Stop': The feedback is complete and the response is satisfactory and answers the human's query in a truthful manner. \n"
        " - 'Continue': The response is not satisfactory and/or there is feedback that needs to be included. \n"
    )

    # Initialize the language model with zero randomness for consistent outputs
    llm = ChatCohere(model="command-r-plus", temperature=0)

    # Structure the LLM's response using the AnalyserResponse model
    structured_llm = llm.with_structured_output(MetaSupervisorResponse, preamble=meta_supervisor_preamble)

    meta_supervisor_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                meta_supervisor_preamble,
            ),
            MessagesPlaceholder(variable_name="meta_messages"),
        ]
    )

    meta_supervisor_chain = meta_supervisor_prompt | structured_llm  # Chain the prompt template with the structured language model

    return meta_supervisor_chain