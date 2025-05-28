from langchain_core.prompts import PromptTemplate

from backend.utils import tools_parser
from backend.llms.guide_agent.agent.tools.guide_tools import GuideTools


def rewrite_query_system_prompt():
    template = """Rephrase the following question so that it is fully understandable on its own, without relying on any prior context or conversation history. Keep the original meaning intact and ensure it makes sense independently. 
    Return only the new query and do it in the original language.
    If the current conversations refer to an ARTWORK or an ARTIST, please, add it into the new query.
        
    Current conversation:
    {history}
    Original question: {input}
    New question:"""
    return PromptTemplate(input_variables=["history", "input"], template=template)


def get_location_system_prompt(info: str):
    template = """La siguiente conversación es una conversación entre un visitante al museo Thyssen-Bornesmiza y una IA que funciona como un asistente virtual para el museo. Si la Ia no sabe responder di no lo sé. Responde en el idioma original de la pregunta. Saluda siempre en el primer mensaje
    No digas que tu información viene del contexto dado. Si la información dada como contexto no contiene información sobre la consulta del visitante di que crees que no puedes responder la pregunta.
    Para responder la pregunta tienes la información del historial del chat y la siguiente información acerca de localizaciones y descripciones de obras dentro del museo:
    {artworks_info}

    Current conversation:
    {history}
    Human: {input}
    AI:"""
    template = template.replace("{artworks_info}", info)
    return PromptTemplate(input_variables=["history", "input"], template=template)


def get_filter_system_prompt():
    template = """La siguiente conversación es una conversación entre un visitante al museo Thyssen-Bornesmiza y una IA que funciona como un asistente virtual para el museo. Eres un agente diseñado para filtrar los mensajes del visitante según su finalidad. Para ello ten en cuenta el contexto de la conversación.
    Las categorías disponibles son las siguientes:
    ## Categorias
    - description: mensajes en los que el usuario busca obtener una explicación, descripción o relaciones de una o varias obras.
    - location: mensajes en los que el usuario busca la localización de una obra dentro del museo o pregunta si existen algún tipo de obra concreta.
    - other: otro tipo de información que no tenga que ver directamente con las descripciones o localizaciones de las obras.
    - n_related: mensajes que no tengan relación alguna con el museo.

    ## Reglas adcionales:
    - Responde ÚNICAMENTE con el tipo de categoría.
    - NO añadas información adicional.

    ## Ejemplos:
    - Dónde está la obra en la que salía una mujer en una bañera? - location
    - Estoy buscando una obra en la que salía un paisaje de venecia de la época renacentista - location
    - Tengo dudas de esta obra - description
    - Cúando cierra el museo? - other
    - Cuánto cuesta el recorrido de mujeres? - other
    - Dónde compro la entrada de la exposición colonial? - other
    - Qué entra dentro de la entrada de la exposición colonial? - other
    - tenéis alguna obra que se centre en el vino? - location
    - Estoy haciendo un estudio y busco obras de mujeres - location

    Current conversation:
    {history}
    Human: {input}
    AI:"""
    return PromptTemplate(input_variables=["history", "input"], template=template)


def get_mongo_system_prompt(tools_str):
    template = '''Eres un agente diseñado para especificar el workflow de tareas a realizar para obtener la localización de las obras dentro de un museo.
  Ten en cuenta el historial del chat para seleccionar las herramientas a utilizar:

  Tienes acceso a las siguientes tools:
  {tools}

  Responde utilizando el siguiente formato:
  {{"tools": [{{"function": "name-function", "input": {{"param_name": "value"}}}}, ...]}}

  ## Additional Rules:
  - La pregunta SOLO DEBE contener el json. NO añádas más información
  - Si la pregunta NO hace referencia a ningún autor o título concreto devolver {{"tools": []}}

  Current conversation:
  {history}
  Human: {input}
  AI:"""
  '''

    template = template.replace("{tools}", tools_str)
    return PromptTemplate(input_variables=["history", "input"], template=template)
