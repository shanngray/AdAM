def builder_edge(state):
    count = len(state["agent_blueprints"])

    if count < 3:
        return "Another"
    else:
        return "Enough"

