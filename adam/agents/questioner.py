"""Agent that rewrites user story prompts"""


from langchain_core.output_parsers import StrOutputParser
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

async def questioner():
    system_prompt = (
        
        "## ROLE:\nYou are a  curious and savvy communicator. \n\n"
        "## TASK:\nGiven the conversation history, write a concise question to the user "
        "to find out how they want to proceed.\n\n"
        "## NOTES:\n"
        " - The goal is not to answer the user's prompt but to keep them talking and engaged."
        " - Your reply should be no more than 2 sentences."
    )
    llm = ChatCohere(model="command-r-plus", temperature=0.9)
    
    # The ChatPromptTemplate class in LangChain is used to create and format prompts for 
    # conversational models. It provides a structured way to define the messages that will be sent
    # to the model, allowing for consistent and reusable prompt engineering.
    # The from_messages method is a constructor that allows you to create an instance of ChatPromptTemplate
    # from a list of messages. The messages are structured as tuples, where the first element is the role
    # of the message (i.e. "system" or "user"), and the second element is the content of the message.
    # As the name suggests, MessagesPlaceholder allows us to create a placeholder for the messages that 
    # make up the conversational history.
    questioner_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    output_parser = StrOutputParser()
 
    questioner_chain = questioner_prompt | llm | output_parser

    return questioner_chain
