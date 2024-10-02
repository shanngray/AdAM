"""Agent that rewrites user story prompts"""


from langchain_core.output_parsers import StrOutputParser
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

async def engineer(state: dict):
    system_prompt = (
        "# ROLE:\nYou are an expert prompt engineer. \n\n"
        "# TASK:\nRewrite the provided user prompt into clear and concise instructions for "
        "a team of LLM agents to have a conversation. Use Prompt Enginnering best practices. "
        "The instructions should be in a step-by-step format. Make sure to include all details "
        "from the original prompt and importantly don't make anything up.\n\n"
        "# EXAMPLE:\n"
        "## Input: I need help writing a user story for creating and modifying process maps.\n"
        "## Output: Explain the purpose of user stories and the different components. "
        "Ask the user clarifying questions to ensure you understand their requirements. "
        "Once you have a clear understanding of the user's requirements, provide a step-by-step "
        "guide on how to create a user story for the software feature that allows users to design, "
        "update, and save process maps, including the ability to add, remove, or modify process "
        "steps and flow directions.\n\n"
        "# NOTES:\n"
        " - The goal is not to answer the user's prompt but to provide clear instructions in the form "
        "of an LLM prompt.\n"
        " - Make sure your replies are short and that the user is involved in the conversation."
        " - Your reply should be no more than 3 to 4 sentences long."
    )
    llm = ChatCohere(model="command-r-plus", temperature=0.2)
    
    # The ChatPromptTemplate class in LangChain is used to create and format prompts for 
    # conversational models. It provides a structured way to define the messages that will be sent
    # to the model, allowing for consistent and reusable prompt engineering.
    # The from_messages method is a constructor that allows you to create an instance of ChatPromptTemplate
    # from a list of messages. The messages are structured as tuples, where the first element is the role
    # of the message (i.e. "system" or "user"), and the second element is the content of the message.
    # As the name suggests, MessagesPlaceholder allows us to create a placeholder for the messages that 
    # make up the conversational history.
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
