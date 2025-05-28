import streamlit as st
from backend.mongo_manager import MongoManager
import frontend.utils as u
from frontend.tours.tour_description import run_tour


def state_3():
    tour_mongo_index = 0
    if (st.session_state.tour % 4) == 0 and st.session_state.stage == 4:
        if st.session_state.tour == 0:
            prompt = "Cuéntame más acerca de los recorridos temáticos."
            st.session_state.messages.append(({"role": "user", "content": prompt}, None))

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = """
                    !De acuerdo! El Museo Nacional Thyssen-Bonersmiza dispone de varios recorridos temáticos. Algunos de ellos son los siguientes.
                    """
                st.markdown(response)
                st.session_state.messages.append(({"role": "assistant", "content": response}, None))

        mongo = MongoManager()
        tours = mongo.get_tours_dict()

        st.session_state.tour_titles.append("Más recorridos")
        for tour in tours[st.session_state.tour:st.session_state.tour+3]:
            if tour_mongo_index <= len(tours):
                tour_mongo_index += 1
                st.session_state.tour_titles.append(tour['title'])
                st.markdown(f"""
                        <div class="custom-card-h">
                            <img src="{tour['img']}" alt="Imagen">
                             <p><b>{tour['title']}</b><br>{tour['quote']}<br>Este recorrido está compuesto por <b>{tour['size']} obras</b>.</p>
                        </div>
                         """, unsafe_allow_html=True)

        with st.chat_message("assistant"):
            st.markdown("Puedes seleccionar alguno de los anteriores o consultar más recorridos.")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.button(st.session_state.tour_titles[st.session_state.tour+1], on_click=u.set_tour, args=[st.session_state.tour+1], use_container_width=True)
            with col2:
                st.button(st.session_state.tour_titles[st.session_state.tour+2], on_click=u.set_tour, args=[st.session_state.tour+2],  use_container_width=True)
            with col3:
                st.button(st.session_state.tour_titles[st.session_state.tour+3], on_click=u.set_tour, args=[st.session_state.tour+3],  use_container_width=True)
            with col4:
                st.button(st.session_state.tour_titles[st.session_state.tour], on_click=u.set_tour, args=[st.session_state.tour+4],  use_container_width=True)

    if (st.session_state.tour % 4) != 0:
        st.empty()
        st.empty()
        st.empty()
        st.empty()

        prompt = f'Me gustaría realizar el recorrido "{st.session_state.tour_titles[st.session_state.tour]}."'
        st.session_state.messages.append(({"role": "user", "content": prompt}, None))

        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.stage = 5

    if st.session_state.stage == 5:
        run_tour(st.session_state.tour-1)
