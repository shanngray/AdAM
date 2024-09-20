"""Agent for searching the web"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_cohere import ChatCohere
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor

from langchain import hub

async def meta_search():

    llm = ChatCohere(model="command-r-plus", temperature=0.1)

    search_tool = TavilySearchResults(include_answer = True, include_raw_content = False, include_images = False)

    tools = [search_tool]

    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    system_prompt = base_prompt.partial(instructions=(
        "You are an expert at searching the web. You will be given a prompt and you"
        " will search the web to find the most relevant information. You will then "
        "return the most relevant information to the user."
    ))

    llm_with_tools = llm.bind_tools(tools)

    agent = create_cohere_react_agent(llm, tools, system_prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
    )

    return agent_executor
