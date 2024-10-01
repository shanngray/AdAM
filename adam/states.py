"""
This module defines the State data structure used in the LLM project to manage and pass conversational data between AI agents. 
The State structure holds the conversational history and other relevant data such as the subject and prompt of the conversation, 
enabling AI agents to effectively collaborate and maintain context throughout interactions.
"""
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from fastapi import WebSocket

class Constructor_State(TypedDict):
    """
    Defines a protocol of how data is passed from one node (i.e. agent) to the next. The messages attribute is a list
    of responses from the AI agents and human. By passing the full conversational history from one agent to the next, the
    agents can work as a team when solving problems. Other variables in the State vary depending on the use case of the LLM
    project. We will use variables to hold the 'subject' or topic of the initial prompt. The re-engineered prompt that will
    be fed to our team of meta-agents and the system prompts for the meta-agents. We will populate these nodes with responses
    from our AI agents rather than adding those particular responses to the list of messages.

    Attributes:
        messages (Annotated[list[AnyMessage], add_messages]): A list of messages that have been processed or are to be processed,
            annotated with a function that adds messages to a graph structure for further analysis or processing.
        subject (str): The subject or main topic of the current state or conversation.
        prompt (str): The initial or current prompt used to guide the conversation or interaction.
    """
    messages: Annotated[list[AnyMessage], add_messages] # List of messages for constructor agents
    conversation_name: str # Name of the conversation
    subject: str # Subject of the conversation
    rewritten_prompt: str # Rewritten prompt using prompt engineering techniques
    analyser_decision: str # Decision of the analyser agent
    meta_team_size: int # Number of meta-agents in the team
    agent_blueprints: list[dict] # List of agent blueprints


class Meta_State(TypedDict):
    """
    Defines a protocol of how data is passed from one node (i.e. agent) to the next. The messages attribute is a list
    of responses from the AI agents and human. By passing the full conversational history from one agent to the next, the
    agents can work as a team when solving problems.
    """
    meta_messages: Annotated[list[AnyMessage], add_messages] # List of messages for meta-agents
    meta_agents: list[dict] # List of meta-agents in the conversation