from dotenv import load_dotenv
from langchain.agents import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from pymongo import MongoClient

load_dotenv()

client = MongoClient("localhost", 27017)
db = client.thyssen_db
artworks = db.thyssen_artworks

_react_prompt = """Responde las siguientes preguntas tan bien como puedas como si fueras un guía del Museo Nacional Thyssen-Bornemisza.
Si tras buscar la obra no encuentras resultado, asume que no existe la obra o tiene otro título.
Tienes acceso a las siguientes herramientas:

{tools}

Utiliza el siguiente formato:

Question: la pregunta que quieres responder

Thought: siempre debes pensar qué vas a hacer

Action: la acción a tomar, debe ser alguna de: [{tool_names}]

Action Input: la entrada de la acción

Observation: el resultado de la acción

... (El Thought/Action/Action Input/Observation puede repetirse N veces)

Thought: Sé la respuesta final

Final Answer: la respuesta final a la pregunta original

Hecho!

Question: {input}

Thought:{agent_scratchpad}
"""

react_prompt = PromptTemplate(
    template=_react_prompt, input_variables=["tools", "tool_names", "input", "agent_scratchpad"]
)


@tool
def get_artwork_location(artwork_name: str) -> list:
    """
    :param: el nombre de la obra que se quiere saber la ubicación
    :return: una lista con el nombre de la obra, el artista de la obra y la localización de la obra que se quiere conocer
    su ubicación
    """
    artwork_name = artwork_name.replace("\n", "").replace("\r", "").replace('"', "")
    print(artwork_name)
    artwork_location = artworks.find({'artwork_name_title': artwork_name},
                                     {'_id': 0, 'artwork_name_title': 1, 'artwork_artist_name': 1, 'artwork_location': 1})
    return list(artwork_location)


tools = [get_artwork_location]

llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")

react_agent_runnable = create_react_agent(llm, tools, react_prompt)

