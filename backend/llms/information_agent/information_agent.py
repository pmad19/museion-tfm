from backend.llms.information_agent.graph import create_graph
from typing import TypedDict


def get_information_multiagent():
    graph = create_graph()
    #res = graph.invoke({"input": query})['output']
    return graph
