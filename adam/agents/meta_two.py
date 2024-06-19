"""Meta Agent Two"""


from langchain_core.output_parsers import StrOutputParser
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

def meta_two(state: dict):
    system_prompt = state["meta_prompt_two"]

    llm = ChatCohere(model="command-r-plus", temperature=0.2)
    
    # The ChatPromptTemplate class in LangChain is used to create and format prompts for 
    # conversational models. It provides a structured way to define the messages that will be sent
    # to the model, allowing for consistent and reusable prompt engineering.
    # The from_messages method is a constructor that allows you to create an instance of ChatPromptTemplate
    # from a list of messages. The messages are structured as tuples, where the first element is the role
    # of the message (i.e. "system" or "user"), and the second element is the content of the message.
    # As the name suggests, MessagesPlaceholder allows us to create a placeholder for the messages that 
    # make up the conversational history.
    meta_two_prompt = ChatPromptTemplate.from_messages([("system", system_prompt)])

    output_parser = StrOutputParser()
 
    meta_two_chain = meta_two_prompt | llm | output_parser

    return meta_two_chain
    