from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq

from backend.llms.guide_agent.guide_agent import run_guide_llm
from backend.llms.information_llm import run_info_llm
import streamlit as st
import frontend.utils as u
from frontend.tours.tour_stage import state_3
from langchain.memory import ChatMessageHistory, ConversationSummaryBufferMemory

st.title("Museion")
st.markdown('<h3 style="color: gray;">Museo Nacional Thyssen-Bornemisza</h3>', unsafe_allow_html=True)

if "tour" not in st.session_state:
    st.session_state.tour = 0

if "tour_stage" not in st.session_state:
    st.session_state.tour_stage = 0

if "tour_titles" not in st.session_state:
    st.session_state.tour_titles = []

if 'stage' not in st.session_state:
    st.session_state.stage = 1

if "chat_answer_history" not in st.session_state:
    st.session_state.chat_answer_history = []

if "user_prompt_history" not in st.session_state:
    st.session_state.user_prompt_history = []

if "inf_llm_history" not in st.session_state:
    st.session_state.inf_llm_history = ChatMessageHistory()

if "guide_llm_history" not in st.session_state:
    st.session_state.guide_llm_history = ConversationSummaryBufferMemory(
        llm=ChatGroq(model_name="llama-3.1-8b-instant"),
        max_token_limit=300
    )

if "tour_llm_history" not in st.session_state:
    st.session_state.tour_llm_history = ConversationSummaryBufferMemory(
        llm=ChatGroq(model_name="llama-3.1-8b-instant"),
        max_token_limit=300
    )

if "messages" not in st.session_state:
    first_message = """
    ¡Hola! 👋 Soy el guía virtual del Museo Thyssen-Bornemisza  🏛. Estoy aquí para acompañarte a lo largo tu estancia en el museo. ¿Por dónde empezamos?  🚀
    """
    st.session_state.messages = [({"role": "assistant", "content": first_message}, None)]

u.set_styles()

# Display all messages
for message, image in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if image:
            st.image(image)

# Print three initial modes
if st.session_state.stage == 1:
    col1, col2, col3 = st.columns(3)
    with col1:
        u.create_initial_card(
            "sources/images/museo-thyssen-bornemisza-2022-2.jpg",
            "<b>¿Quieres información del museo?</b><br><br>Conoce las exposiciones actuales, compra entradas, "
            "úbicate dentro del museo, conoce nuestras actividades... <br><br>En general, !Consulta cualquier "
            "duda acerca de tu visita! <br><br><br><br>",
            "Información del museo",
            2
        )

    with col2:
        u.create_initial_card(
            "sources/images/Museo-Thyssen-Bornemisza-6-1024x683.jpg",
            "<b>Conoce las obras del Museo Thyssen Bornemisza</b><br><br>Pregunta cualquier tipo de cuestión acerca de las obras de la "
            "colección permanente o la colección de Carmen Thyssen, soy tu guía dentro del museo. Desde información de "
            "la obra hasta preguntas sobre su contexto histórico o autor. <br><br>¡Estoy aquí para ayudarte!",
            "Consulta las obras",
            3
        )
    with col3:
        u.create_initial_card(
            "sources/images/145.jpg",
            "<b>Sigue uno de nuestros recorridos temáticos</b><br><br>Descubre otra forma de recorrer la colección permanente. "
            "Sigue alguno de nuestros recorridos temáticos y te iré guíando por el museo y explicando cada obra. "
            "Si tienes cualquier duda acerca de alguna obra del recorrido, ya sabes. <br><br>¡Pregúntame!",
            "Recorridos temáticos",
            4
        )

elif st.session_state.stage == 2:

    if len(st.session_state.messages) == 1:
        prompt = "Quiero información del museo"
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append(({"role": "user", "content": prompt}, None))

    if prompt := st.chat_input("Escribe un mensaje"):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append(({"role": "user", "content": prompt}, None))

        with st.chat_message("assistant"):
            response = st.write_stream(run_info_llm(query=prompt, chat_history=st.session_state["inf_llm_history"]))

        st.session_state.chat_answer_history.append(response)
        st.session_state.user_prompt_history.append(prompt)
        st.session_state.messages.append(({"role": "assistant", "content": response}, None))


elif st.session_state.stage == 3:

    if len(st.session_state.messages) == 1:
        prompt = "Quiero saber sobre las obras de la colección"
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append(({"role": "user", "content": prompt}, None))

    if prompt := st.chat_input("Escribe un mensaje"):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append(({"role": "user", "content": prompt}, None))

        with st.chat_message("assistant"):
            response = run_guide_llm(query=prompt, chat_history=st.session_state.guide_llm_history)
            st.write_stream(u.response_generator(response['message']))

        st.session_state.chat_answer_history.append(response['message'])
        st.session_state.user_prompt_history.append(prompt)
        st.session_state.guide_llm_history = response['memory']

        st.session_state.messages.append(({"role": "assistant", "content": response['message']}, None))


elif st.session_state.stage >= 4:
    state_3()
