def builder_edge(state):
    count = len(state["agent_blueprints"])

    if count < 5:
        return "Another"
    else:
        return "Enough"

