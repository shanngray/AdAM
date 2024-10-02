from langchain_core.messages import HumanMessage

def meta_node_helper(state, agent, name):

    print(f"<META NODE: {name}>")
    messages = state["meta_messages"]
    meta_chain = agent

    result = meta_chain.invoke({"messages": messages})

    print(f"{name} says: {result[50]}...")

    state["meta_messages"].append(HumanMessage(content=result, name=name))
    return state
