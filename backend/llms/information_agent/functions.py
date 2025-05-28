from backend.llms.prompts import _prompt_info_system_template
from backend.llms.information_agent.location_agent.location_agent import run_location_agent
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")


def analyze_question(state):
    prompt = PromptTemplate.from_template("""
    Eres un agente que tiene que clasificar una pregunta como relacionada con (1) ubicaciones o (2) tarifas y actividades

    Question : {input}

    Analiza la pregunta. Responde solo con "location" si la pregunta es sobre la localización de una obra dentro del museo. 
    En cualquier otro caso responde "fees".

    Your answer (location/fees) :
    """)
    chain = prompt | llm
    response = chain.invoke({"input": state["input"]})
    decision = response.content.strip().lower()
    return {"decision": decision, "input": state["input"]}


def answer_fees_act_question(state):
    prompt = PromptTemplate.from_template(_prompt_info_system_template + """
    Responde a la siguiente pregunta: {input}
    """)
    chain = prompt | llm
    response = chain.invoke({"input": state["input"]})
    return {"output": response.content}


def answer_location_question(state):
    response = run_location_agent(state["input"])
    return {"output": response}
