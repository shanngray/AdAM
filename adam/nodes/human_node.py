"""
This is a special node that doesn't contain an AI agent instead it will house a function to 
receive inoput from the human. This is the second node in the graph and its purpose is to get
feedback from the human and make sure that the re-engineered prompt is on track. It servers a 
similar purpose to active listening and makes sure that the AI agent understood the human's
intent.
"""
from langchain_core.messages import HumanMessage

def human_node(state):
    print("###Human Node###\n")

    #last_message = state["messages"][-1]
    #content = last_message.content

    human_response = input("Does this look good? Or do you want to make any changes? ")

    human_message = HumanMessage(content=human_response, name="human")

    return {"messages":[human_message]}
