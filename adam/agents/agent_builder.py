"""Agent that builds the meta agents"""


from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

async def agent_builder():
    

    system_prompt = (
        "# ROLE:\nYou are an LLM and Generative AI expert specialises in writing system prompts. \n\n"
        "# TASK:\nWrite the system prompt for an agent that is a subject matter expert in {subject}.\n\n"
        "# NOTES:\n"
        " - The system prompt should use advanced prompt engineering techniques.\n"
        " - The *task* will be passed to the Agent separately.\n"
        " - Be concise and specific.\n"
        " - Only return the system prompt and nothing else.\n"
        " - Incorporate the agent's blueprint into the system prompt: \n"
        "{agent_blueprint}"
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    
    # The ChatPromptTemplate class in LangChain is used to create and format prompts for 
    # conversational models. It provides a structured way to define the messages that will be sent
    # to the model, allowing for consistent and reusable prompt engineering.
    # The from_messages method is a constructor that allows you to create an instance of ChatPromptTemplate
    # from a list of messages. The messages are structured as tuples, where the first element is the role
    # of the message (i.e. "system" or "user"), and the second element is the content of the message.
    # As the name suggests, MessagesPlaceholder allows us to create a placeholder for the messages that 
    # make up the conversational history.
    builder_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", "Please create the system prompt for an agent that is an expert in: {subject}"),
        ]
    )

    output_parser = StrOutputParser()
 
    builder_chain = builder_prompt | llm | output_parser

    return builder_chain

    