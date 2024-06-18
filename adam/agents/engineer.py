"""Agent that rewrites user story prompts"""


from langchain_core.output_parsers import StrOutputParser
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

def engineer(state: dict):
    system_prompt = (
        "#ROLE: You are an expert prompt engineer. \n\n"
        "#TASK: Rewrite the provided user prompt into clear and concise instructions for "
        "an LLM to follow using Prompt Enginnering best practices. The instructions should be in a "
        "step-by-step format. Make sure to include all details from the original prompt and "
        "importantly don't make anything up.\n\n"
        "#EXAMPLE: \n"
        "##Input: I need help writing a user story for creating and modifying process maps.\n"
        "##Output: Compose a user story for a software feature that allows users to design, "
        "update, and save process maps, including the ability to add, remove, or modify process "
        "steps and flow directions.\n\n"
        "#NOTES: \n"
        " - The goal is not to answer the user's prompt but to provide clear instructions in the form "
        "of an LLM prompt."
    )
    llm = ChatCohere(model_name="command-r-plus", temperature=0.2)
    
    engineer_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    output_parser = StrOutputParser()
 
    engineer_chain = engineer_prompt | llm | output_parser

    return engineer_chain
