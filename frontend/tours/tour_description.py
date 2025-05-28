from langchain_core.messages import HumanMessage, AIMessage

from backend.llms.guide_agent.guide_agent import run_guide_llm
from backend.tour_retriever import TourRetriever
import frontend.utils as u
import streamlit as st
import time

tour_retriever = TourRetriever()


def run_tour(n_tour):
    if st.session_state.tour_stage == 0:
        u.set_tour(0)
        tour_retriever.set_tour(n_tour)
        welcome_messages = tour_retriever.get_tour_welcome()

        st.session_state.description_len = 1
        for m in welcome_messages:
            st.session_state.description_len += 1
            st.session_state.messages.append(({"role": "assistant", "content": m}, None))
            with st.chat_message("assistant"):
                time.sleep(1.5)
                st.write_stream(u.response_generator(m))

        m = """
        A partir de ahora iré guíandole por el museo durante el recorrido. Antes de describir la obra le diré a que
        sala debe dirigirse y cuando esté en ella pulse el botón "Pulse para continuar" como el que 
        aparece ahora mismo.
        """

        st.session_state.messages.append(({"role": "assistant", "content": m}, None))
        with st.chat_message("assistant"):
            st.write_stream(u.response_generator(m))

        st.button('Pulse para continuar', on_click=u.set_tour_stage, args=[1], use_container_width=True)

    if st.session_state.tour_stage == 1:
        for _ in range(st.session_state.description_len):
            st.empty()

        prompt = f'Continuar con la explicación de la obra.'
        st.session_state.messages.append(({"role": "user", "content": prompt}, None))

        with st.chat_message("user"):
            st.markdown(prompt)

        m = """
        ¡Perfecto! Parece que entiendes la dinámica. Cuando pulses continuar procederé a describir la siguiente obra
        del recorrido, una vez terminada la explicación podrá preguntarme cualquier duda acerca de la obra o 
        pulsar el botón "Continuar con la siguiente obra" para continuar. ¡Probémoslo!
        """

        st.session_state.messages.append(({"role": "assistant", "content": m}, None))
        with st.chat_message("assistant"):
            st.write_stream(u.response_generator(m))

        st.button('Continuar con la siguiente obra', on_click=u.set_tour_stage, args=[2], use_container_width=True)

    if st.session_state.tour_stage == 2:
        prompt = f'Continuar con la siguiente obra.'
        st.session_state.messages.append(({"role": "user", "content": prompt}, None))

        with st.chat_message("user"):
            st.markdown(prompt)

        m = """
        ¡Pues esto es todo! Ya sabes como funcionan los recorridos dinámicos, por lo que podemos empezar.
        """

        st.session_state.messages.append(({"role": "assistant", "content": m}, None))
        with st.chat_message("assistant"):
            st.write_stream(u.response_generator(m))

        time.sleep(2)

        u.set_tour_stage(3)

    if st.session_state.tour_stage == 3:
        st.session_state.artwork_messages = tour_retriever.get_tour_artwork_messages()

        for m in st.session_state.artwork_messages[0:2]:
            st.session_state.messages.append(({"role": "assistant", "content": m}, None))
            with st.chat_message("assistant"):
                st.write_stream(u.response_generator(m))

        if st.session_state.artwork_messages[2] == 0:
            with st.chat_message("assistant"):
                st.image(st.session_state.artwork_messages[3])
            st.session_state.messages.append(
                ({"role": "assistant", "content": ""}, st.session_state.artwork_messages[3]))

        st.button('Pulse para continuar', on_click=u.set_tour_stage, args=[4], use_container_width=True)

    if st.session_state.tour_stage == 4:
        prompt = f'Continuar con la explicación de la obra.'
        st.session_state.messages.append(({"role": "user", "content": prompt}, None))

        with st.chat_message("user"):
            st.markdown(prompt)

        description = ""
        for m in st.session_state.artwork_messages[4:]:
            description += "\nm"
            st.session_state.messages.append(({"role": "assistant", "content": m}, None))
            with st.chat_message("assistant"):
                st.write_stream(u.response_generator(m))
        st.session_state.tour_llm_history.save_context(
            {"input": "Me puedes explicar " + st.session_state.artwork_messages[0]},
            {"outputs": description})

        m = """
                ¡Si tienes alguna duda de la obra es el momento de preguntar! Pregúntame lo que quieras de la obra.
                O si no, pulse "Continuar con la siguiente obra" para seguir con el recorrido.
                """

        st.session_state.messages.append(({"role": "assistant", "content": m}, None))
        with st.chat_message("assistant"):
            st.write_stream(u.response_generator(m))

        if prompt := st.chat_input("Escribe un mensaje", on_submit=u.set_tour_stage, args=[5]):
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

        st.button('Continuar con la siguiente obra', on_click=u.set_tour_stage, args=[3], use_container_width=True)

    if st.session_state.tour_stage == 5:
        if prompt := st.chat_input("Escribe un mensaje", on_submit=u.set_tour_stage, args=[5]):
            with st.chat_message("user"):
                st.markdown(prompt)
                st.session_state.messages.append(({"role": "user", "content": prompt}, None))

            with st.chat_message("assistant"):
                response = run_guide_llm(query=prompt, chat_history=st.session_state.tour_llm_history)
                st.write_stream(u.response_generator(response['message']))

            st.session_state.chat_answer_history.append(response['message'])
            st.session_state.user_prompt_history.append(prompt)
            st.session_state.tour_llm_history = response['memory']

            st.session_state.messages.append(({"role": "assistant", "content": response['message']}, None))

        st.button('Continuar con la siguiente obra', on_click=u.set_tour_stage, args=[3], use_container_width=True)

