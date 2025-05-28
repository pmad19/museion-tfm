from langchain.memory import ConversationSummaryBufferMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv

from backend.llms.guide_agent.agent.graph import get_graph

load_dotenv()


def run_guide_llm(query: str, chat_history: ConversationSummaryBufferMemory):
    llama_70 = ChatGroq(model_name="llama-3.3-70b-versatile")
    inputs = {"query": query, "messages": [query], "memory": chat_history, "llm": llama_70}
    app = get_graph()
    return app.invoke(inputs)
