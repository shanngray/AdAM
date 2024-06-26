import sys
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv(".env")

PROJECT_DIRECTORY = os.getenv("PROJECT_DIRECTORY")

sys.path.insert(1, PROJECT_DIRECTORY)

from build_graph import metaflow

def main():

    init_prompt = input("Hello, how can I help you today? \n")
    inputs = {"messages": [HumanMessage(content=init_prompt, name="human")]}

    graph = metaflow.compile()

    for output in graph.stream(inputs):
        for node, state in output.items():
            # Note how the print statements here appear after any print statements within the node and agent
            # functions. I think this is because the output is being streamed to the console in real-time.
            print(f"<NODE: {node}>\n")
            if 'messages' in state:
                print(f"{state['messages'][-1].name}: \"{state['messages'][-1].content}\"\n")
            elif 'meta_messages' in state:
                print(f"{state['meta_messages'][-1].name}: \"{state['meta_messages'][-1].content}\"\n")
            else:
                print("No messages found in state.\n")
            print("<END INNER LOOP>\n")  # Print a separator after each conversation turn
        print("<END OUTER LOOP>\n")

if __name__ == '__main__':
    main()
