import sys
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv(".env")

PROJECT_DIRECTORY = os.getenv("PROJECT_DIRECTORY")

sys.path.insert(1, PROJECT_DIRECTORY)

from build_graph import metaflow

def main():

    inputs = {"messages": [HumanMessage(content="hello?", name="human")]}

    graph = metaflow.compile()

    for output in graph.stream(inputs):
        for state in output.items():
            # Check if the node's state contains messages
            
            print("XXX")  # Print a separator after each conversation turn

if __name__ == '__main__':
    main()
