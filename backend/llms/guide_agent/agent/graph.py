from typing import TypedDict

from langchain.memory import ConversationSummaryBufferMemory
from langchain_groq import ChatGroq
from langgraph.graph import Graph, END
from backend.llms.guide_agent.agent.nodes import Nodes
from backend.llms.guide_agent.agent.decision_forks import *


class AgentState(TypedDict):
    message: str
    query: str
    query_type: str
    memory: ConversationSummaryBufferMemory
    artworks_location_info: list
    llm: ChatGroq
    tools_workflow: list


def get_graph():
    nodes = Nodes()
    workflow = Graph()

    workflow.add_node("entry_node", nodes.entry_node_8)
    workflow.add_node("description_node", nodes.description_node)
    workflow.add_node("pinecone_location_node", nodes.pinecone_location_node)
    workflow.add_node("mongo_location_node", nodes.mongo_location_node)
    workflow.add_node("mongo_location_tools", nodes.mongo_location_agent)
    workflow.add_node("conversation_location_node", nodes.conversation_location_node)
    workflow.add_node("other_node", nodes.other_llm)
    workflow.add_node("n_related_node", nodes.n_related_llm)

    workflow.add_conditional_edges('entry_node', agent_decision_fork, {"other": "other_node", "n_related": "n_related_node", "description": "description_node", "location": "mongo_location_node"})
    workflow.add_conditional_edges('mongo_location_node', mongo_tools_decision, {"pinecone": "pinecone_location_node", "end": "conversation_location_node", "execute_tool": "mongo_location_tools"})
    workflow.add_conditional_edges('mongo_location_tools', mongo_tools_decision, {"pinecone": "pinecone_location_node", "end": "conversation_location_node", "execute_tool": "mongo_location_tools"})
    workflow.add_edge("pinecone_location_node", "conversation_location_node")

    workflow.set_entry_point("entry_node")

    workflow.add_edge("n_related_node", END)
    workflow.add_edge("other_node", END)
    workflow.add_edge("conversation_location_node", END)
    workflow.add_edge("description_node", END)

    app = workflow.compile()
    return app
