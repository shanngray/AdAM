"""Agent that assigns a subject to the rewritten prompt"""


from langchain_core.output_parsers import StrOutputParser
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv(".env")

prompt = """
Provide an overview of trees, including their biology, ecological importance, and cultural significance. Detail the following: 

- Describe the biological characteristics of trees, including their structure, lifecycle, and methods of reproduction.
- Explain the ecological roles and benefits of trees, such as their impact on climate, soil health, and biodiversity.
- Discuss the cultural and symbolic significance of trees across different societies and historical contexts.
- Outline the variety of tree species, highlighting their unique adaptations and distributions.
- Finally, provide examples of the practical uses of trees, including their applications in medicine, industry, and daily life. 
"""
async def subject_agent():
    system_prompt = (
        "# ROLE:\nYou are an expert prompt engineer. \n\n"
        "# TASK:\nAnalyse the prompt and determine the subject matter.\n\n"
        "# EXAMPLE:\n"
        "## Input:\nCompose a user story for a software feature that allows users to design, "
        "update, and save process maps, including the ability to add, remove, or modify process "
        "steps and flow directions.\n\n"
        "## Output:\nProcess Maps\n\n"
        "# NOTES:\n"
        " - The goal is not to answer the user's prompt but to explain the subject matter "
        "of the prompt.\n"
        " - be concise and specific.\n"
        " - Only return the subject matter and notting else.\n\n"
        "# PROMPT:\n"
        "## Input:\n{rewritten_prompt}\n\n"
        "## Output:\n"
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
    subject_prompt = ChatPromptTemplate.from_messages([("system", system_prompt)])

    output_parser = StrOutputParser()
 
    subject_chain = subject_prompt | llm | output_parser

    return subject_chain

subject_chain = subject_agent()

human_prompt = HumanMessage(content=prompt)

response = subject_chain.invoke({"rewritten_prompt": [human_prompt]})

print(response)