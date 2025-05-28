from langgraph.graph import StateGraph, END
from typing import Annotated, TypedDict
from backend.llms.information_agent.functions import analyze_question, answer_fees_act_question, answer_location_question


class AgentState(TypedDict):
    input: str
    output: str
    decision: str


def create_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("analyze", analyze_question)
    workflow.add_node("fees_agent", answer_fees_act_question)
    workflow.add_node("location_agent", answer_location_question)

    workflow.add_conditional_edges(
        "analyze",
        lambda x: x["decision"],
        {
            "location": "location_agent",
            "fees": "fees_agent"
        }
    )

    workflow.set_entry_point("analyze")
    workflow.add_edge("fees_agent", END)
    workflow.add_edge("location_agent", END)

    return workflow.compile()

