from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from backend.mongo_manager import MongoManager

mongo = MongoManager()
fees = mongo.get_fees()
activities = mongo.get_activities()

# History context prompt for guide_agent
_contextualize_q_system_prompt = (
        "Dado un historial de mensajes de un chat y un último mensaje "
        "que hace referencia al contexto en el historial dado, "
        "formula una pregunta estándar que pueda ser interpretada "
        "sin el historial del chat. NO respondas la pregunta, "
        "solo reformulala si es necesario y si no devuélvela como es."
    )

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", _contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# System context prompt for guide_agent
_system_guide_prompt = """
Usa las siguientes piezas de contexto para responder la pregunta al final. 
Si no sabes la respuesta di que no lo sabes, no intentes generar una respuesta.
Responde como si fueras un guía del Museo Nacional Thyssen-Bornemisza.
Añade lenguaje propio de un guía y sé cordial.
Al responder no digas que tu conocimiento proviene del texto dado. 

{context}

"""

_system_guide_prompt = """
Use the following pieces of context to answer the final query.
If you don't know the answer say that you don't know the answer, do NOT try to generate an answer.
Answer always as a guide for Museo Nacional Thyssen-Bornemisza.
Add guide language and be friendly.
When you answer do not say that your knowledge come from the given text.
Try to use as much as posibble of the context to answer the query.
The context given is about artworks from the thyssen museum.
Answer always in spanish.

{context}
"""

system_guide_prompt = PromptTemplate(
    template=_system_guide_prompt, input_variables=["context"]
)

# System context prompt for information_llm
_prompt_fees = ""
_prompt_activities = ""

for fee in fees:
    _prompt_fees += f"""TARIFA: {fee['fee_name']}
PRECIO: {fee['price']}
CONDICIONES: {fee['conditions']}
________________________________________________
"""

for activity in activities:
    _prompt_activities += f"""ACTIVIDAD: {activity['activity_name']}
DESCRIPCION: {activity['description']}
DETALLES: {activity['details']}
PRECIO: {activity['price']}
LINK_DE_COMPRA: {activity['buy_url']}
________________________________________________
"""

_prompt_info_system_template = f"""
Eres un asistente virtual para el Museo Nacional Thyssen-Bornemisza, dispones de la siguiente información respecto a 
tarifas y actividades del museo. 
Responde siempre con la opción que mejor se adapte a la pregunta, o si dudas presenta opciones similares. 
Al responder no digas que tu conocimiento proviene del texto dado. 
El historial del chat provisto incluye información acerca de la conversación que estás manteniendo. 
Si preguntan acerca de precios de entradas responde con los precios y condiciones de las tarifas disponibles.
Las entradas al museo permiten el acceso a las exposiciones.

Las tarifas tendrán el siguiente formato:

TARIFA: Nombre de la tarifa
PRECIO: Precio de la tarifa
CONDICIONES: Condiciones sujetas a la tarifa

Las actividades tendrán el siguiente formato:

ACTIVIDAD: Nombre de la actividad
DESCRIPCIÓN: Descripción de la actividad
DETALLES: Detalles de la actividad (idioma, condiciones, horarios, temas, etc.)
PRECIO: Precio de la actividad
LINK_DE_COMPRA: URL de la página de compra de entradas de la actividad

Las entradas se pueden obtener en taquilla, por teléfono llamando al +34 917911370 o a través de la página: https://entradas.museothyssen.org/es
La siguiente lista corresponde a la lista de tarifas disponibles:
----------------------------------------------------------------------
{_prompt_fees}

La siguiente lista corresponde a la lista de actividades disponibles:
----------------------------------------------------------------------
{_prompt_activities}
"""

prompt_info_system = ChatPromptTemplate.from_messages([(
        "system",
        _prompt_info_system_template
    ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"), ])


prompt_pre_info_system = ChatPromptTemplate.from_messages([(
        "system",
        "No respondas a la pregunta."
        "Devuelve exactamente lo mismo que has recibido.",
    ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"), ])

