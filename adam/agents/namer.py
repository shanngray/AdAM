"""Agent that assigns a name to the rewritten prompt"""


from langchain_core.output_parsers import StrOutputParser
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

async def namer_agent(state: dict):
    system_prompt = (
        "# ROLE:\nYou are a creative and witty savant. \n\n"
        "# TASK:\nAnalyse the prompt and come up with a short and unique name for the conversation.\n\n"
        "# EXAMPLE:\n"
        "## Input:\nCompose a user story for a software feature that allows users to design, "
        "update, and save process maps, including the ability to add, remove, or modify process "
        "steps and flow directions.\n\n"
        "## Output:\nMapper of Processes\n\n"
        "# NOTES:\n"
        " - The goal is not to answer the user's prompt but to come up with a fun "
        "and unique name for the conversation.\n"
        " - you are sometimes witty, sarcastic, creative, use puns, irony, etc.\n"
        " - Only return the name of the conversation and notting else.\n\n"
        "# PROMPT:\n"
        "## Input:\n{rewritten_prompt}\n\n"
        "## Output:\n"
    )
    llm = ChatCohere(model="command-r-plus", temperature=0.9)
    
    namer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="rewritten_prompt"),
        ]
    )

    output_parser = StrOutputParser()
 
    namer_chain = namer_prompt | llm | output_parser

    return namer_chain
