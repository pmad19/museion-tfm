from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json

from backend.llms.guide_agent.agent.tools.guide_tools import GuideTools
from backend.llms.retrievers.description_retriever.description_retriever import DescriptionRetriever
from backend.llms.retrievers.location_retriever.location_retriever import LocationRetriever
from backend.llms.guide_agent.prompts import get_filter_system_prompt, get_mongo_system_prompt, \
    get_location_system_prompt, rewrite_query_system_prompt
from backend.mongo_manager import MongoManager
from backend.utils import parser_artwork_location_info

load_dotenv()


class Nodes:
    def __init__(self):
        self.mongo_manager = MongoManager()
        self.llama_70 = ChatGroq(model_name="llama-3.3-70b-versatile")
        self.llama_8 = ChatGroq(model_name="llama-3.1-8b-instant")
        self.guide_tools = GuideTools()
        self.tools = self.guide_tools.get_tools()
        self.str_tools = self.guide_tools.get_str_tools()
        self.tools_map = {tool.name: tool.func for tool in self.tools}
        self.location_retriever = LocationRetriever()
        self.description_retriever = DescriptionRetriever()

    def entry_node_70(self, state):
        print("ENTRY NODE 70: Called")
        history_str = state['memory'].buffer
        rewrite_prompt = rewrite_query_system_prompt()
        rewrite_chain = rewrite_prompt | self.llama_8
        state['query'] = rewrite_chain.invoke({"history": history_str, "input": state['query']}).content
        system_prompt = get_filter_system_prompt()
        filter_chain = system_prompt | self.llama_70
        state['query_type'] = filter_chain.invoke({"history": history_str, "input": state['query']}).content
        print("ENTRY NODE 70: Finished")
        return state

    def entry_node_8(self, state):
        print("ENTRY NODE 8: Called")
        history_str = state['memory'].buffer
        rewrite_prompt = rewrite_query_system_prompt()
        rewrite_chain = rewrite_prompt | self.llama_8
        history_str = state['memory']
        state['query'] = rewrite_chain.invoke({"history": history_str, "input": state['query']}).content
        system_prompt = get_filter_system_prompt()
        filter_chain = system_prompt | self.llama_8
        state['query_type'] = filter_chain.invoke({"history": history_str, "input": state['query']}).content
        print(f"ENTRY NODE 8: Finished with {state['query_type']}")
        return state

    def mongo_location_node(self, state):
        print("MONGO LOCATION NODE: Called")
        state['artworks_location_info'] = []
        system_prompt = get_mongo_system_prompt(self.str_tools)
        filter_chain = system_prompt | state['llm']
        response = filter_chain.invoke({"history": state['memory'], "input": state['query']})
        state['tools_workflow'] = json.loads(response.content)['tools']
        print("MONGO LOCATION NODE: Finished")
        return state

    def mongo_location_agent(self, state):
        print("MONGO LOCATION AGENT: Called")
        tool = state['tool_function']
        tool_fun = self.tools_map[tool.get('function')]
        tool_params = tool.get('input')
        artworks_list_location = tool_fun(**tool_params)
        state['artworks_location_info'] = artworks_list_location
        print(f"MONGO LOCATION AGENT: Finished with {tool.get('function')}")
        return state

    def pinecone_location_node(self, state):
        print("PINECONE LOCATION: Called")
        state['artworks_location_info'] = self.location_retriever.get_artworks(state['query'])
        print("PINECONE LOCATION: Finished")
        return state

    def conversation_location_node(self, state):
        artworks_location_info_str = parser_artwork_location_info(self.mongo_manager, state['artworks_location_info'])
        memory = state['memory']
        conversation_sum_bufw = ConversationChain(
            llm=state['llm'], prompt=get_location_system_prompt(artworks_location_info_str),
            memory=memory)
        state['memory'] = memory
        state['message'] = conversation_sum_bufw.run(state['query'])
        return state

    def description_node(self, state):
        documents = self.description_retriever.get_artworks(state['query'])
        document_strings = "\n\n".join(
            f"Contexto de la obra: {doc.metadata.get('artwork_name', 'Desconocida')} del autor {doc.metadata.get('artist_name', 'Desconocido')}, expuesta en la sala: {doc.metadata.get('exposed_room', 'No especificada')}\n{doc.page_content}"
            for doc in documents
        )
        memory = state['memory']
        conversation_sum_bufw = ConversationChain(
            llm=state['llm'], prompt=get_location_system_prompt(document_strings),
                memory=memory)
        state['memory'] = memory
        state['message'] = conversation_sum_bufw.run(state['query'])
        return state

    def n_related_llm(self,state):
        return "Esto no tiene nada que ver puñeta"

    def other_llm(self,state):
        return "No venga a mamar verga, aquí no respondemos eso mamayema"
