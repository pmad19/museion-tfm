from langchain_core.agents import AgentFinish
from langgraph.graph import END, StateGraph
from backend.llms.information_agent.location_agent.nodes import execute_tools, run_agent_reasoning_engine
from backend.llms.information_agent.location_agent.state import AgentState
from dotenv import load_dotenv

load_dotenv()

AGENT_REASON = "agent_reason"
ACT = "act"


def should_continue(state: AgentState) -> str:
    if isinstance(state["agent_outcome"], AgentFinish):
        return END
    else:
        return ACT


def create_location_graph():
    flow = StateGraph(AgentState)

    flow.add_node(AGENT_REASON, run_agent_reasoning_engine)
    flow.set_entry_point(AGENT_REASON)
    flow.add_node(ACT, execute_tools)

    flow.add_conditional_edges(
        AGENT_REASON,
        should_continue,
    )

    flow.add_edge(ACT, AGENT_REASON)

    return flow.compile()


def run_location_agent(query: str):
    location_graph = create_location_graph()
    res = location_graph.invoke(input={"input": query, })
    return res['agent_outcome'].return_values['output']
