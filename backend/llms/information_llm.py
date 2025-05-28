from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

from backend.llms.prompts import prompt_info_system, prompt_pre_info_system
from langchain_core.runnables.history import RunnableWithMessageHistory
from backend.llms.information_agent.information_agent import get_information_multiagent
from langchain.memory import ChatMessageHistory
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")


def run_info_llm(query: str, chat_history: ChatMessageHistory):
    chain = prompt_info_system | llm

    chain_with_message_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: chat_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    return chain_with_message_history.stream({"input": query}, {"configurable": {"session_id": "unused"}})


