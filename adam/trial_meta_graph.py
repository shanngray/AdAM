from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import Literal
from langchain_core.messages import HumanMessage



# team will be loaded with the names of the meta agents
team = {
    "adam": "Is good at math.",
    "bob": "Is good at science.",
    "charlie": "Is good at history.",
    "david": "Is good at art.",
    "edward": "Is good at music.",
    "frank": "Is good at sports.",
    "george": "Is good at computers.",
    "harry": "Is good at religion.",
    "ian": "Is good at english.",
    "jack": "Is good at comedy."
}

system_prompt = (
    "Your are an Agentic Maestro. A conductor of AI agents and always know who is best placed to "
    "respond next. If you are not sure, you ask the user to respond."
    " The agents you can choose from are {{name: description}}: {team}"
)

def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["messages"][-1].content, name=name)]}

options = ["FINISH"] + list(team.keys())

class routeResponse(BaseModel):
    next: Literal[*options]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Given the conversation above, who should act next?"
            " Or should we FINISH? Select one of: {options}",
        ),
    ]
).partial(options=str(options), members=", ".join(team))

llm = ChatOpenAI(model="gpt-4o-mini")

def supervisor_agent(state):
    supervisor_chain = (
        prompt
        | llm.with_structured_output(routeResponse)
    )
    return supervisor_chain.invoke(state)
