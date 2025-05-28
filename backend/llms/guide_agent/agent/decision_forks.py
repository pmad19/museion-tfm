def agent_decision_fork(state):
    return state['query_type']


def mongo_tools_decision(state):
    if len(state['tools_workflow']) > 0:
        fun = state['tools_workflow'].pop(0)
        state['tool_function'] = fun
        return "execute_tool"
    else:
        if len(state['artworks_location_info']) == 0:
            return "pinecone"
        else:
            return "end"