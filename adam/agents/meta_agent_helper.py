from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

def meta_agent_helper(meta_agent):

    system_prompt = meta_agent["system_prompt"]
    temperature = meta_agent["temperature"]

    model = ChatOpenAI(model="gpt-4o-mini", temperature=temperature)

    meta_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    output_parser = StrOutputParser()
 
    meta_chain = meta_prompt | model | output_parser

    return meta_chain