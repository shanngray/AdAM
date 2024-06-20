"""Agent for searching the web"""

from langchain_core.output_parsers import StrOutputParser
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults

def searcher(state):

    llm = ChatCohere(model="command-r-plus", temperature=0.1)

    search_tool = TavilySearchResults()

    tools = [search_tool]

    system_prompt = ("You are an expert at searching the web. You will be given a prompt and you"
                     " will search the web to find the most relevant information. You will then "
                     "return the most relevant information to the user."
    )

    llm_with_tools = llm.bind_tools(tools)

    agent = create_tool_calling_agent(llm, tools, system_prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
    )
