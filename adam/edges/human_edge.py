def human_edge(state):
    message = state["meta_messages"][-1].content

    if message.lower() in ["stop", "quit", "exit", "end", "finish", "STOP", "QUIT", "EXIT", "END", "FINISH"]:
        return "Stop"
    else:
        return "Continue"