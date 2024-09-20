"""Module for planning which meta sub-flow to use
"""
import sys
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_DIRECTORY = os.getenv("PROJECT_DIRECTORY")
sys.path.insert(1, PROJECT_DIRECTORY)  # Include project directory in the system path for module imports

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_cohere import ChatCohere

# LangChain's BaseModel and Field are derived from pydantic's BaseModel class and Field attribute and can be used to
# enforce structure in an LLM's responses. Here we are using them to ensure that the LLM only responds in one of two
# ways. This can be extremely useful in flow engineering as it allows us to route the flow to the correct node
# without having to worry about variances in the LLM's responses.
class PromptComplexity(BaseModel):
    """Whether the prompt is simple(can be answered easily) or complex(needs internet research)."""
    complexity: str = Field(description="Prompt Complexity: 'simple' or 'complex'")

async def planner(state):

    planner_preamble = (
        "You are an analyst that assesses the complexity of the prompt and will *ALWAYS* return one of the following values: \n"
        " - simple: for any prompt where you know the answer. \n"
        " - complex: for any other prompt and if you need to lookup the internet to answer the question. \n"
    )

    # Initialize the language model with zero randomness for consistent outputs
    llm = ChatCohere(model="command-r-plus", temperature=0)

    # Structure the LLM's response using the AnalyserResponse model
    structured_llm = llm.with_structured_output(PromptComplexity, preamble=planner_preamble)

    # Here we are creating a ChatPromptTemplate that only has one message in it. This message is a placeholder
    # for the human's response that needs to be analysed.
    planner_prompt = ChatPromptTemplate.from_messages(
        [("human", "Prompt to be analysed: {rewritten_prompt}")]
    )

    planner_chain = planner_prompt | structured_llm  # Chain the prompt template with the structured language model

    return planner_chain
