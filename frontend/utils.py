import streamlit as st
import time
import base64


def set_styles():
    st.markdown("""
        <style>
        .custom-card {
            background: #F1F1F1;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 15px;
            text-align: center;
            margin-bottom: 5px;
        }
        .custom-card-h {
            display: flex;
            align-items: center;
            background: #F1F1F1;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 15px;
            margin-bottom: 5px;
            max-width: 800px; 
            margin: 0 auto; 
            text-align: left; 
        }
        .custom-card-h img {
            border-radius: 10px;
            margin-right: 15px;
            height: 100%; /* La imagen ocupará toda la altura del contenedor */
            object-fit: cover; /* Mantiene las proporciones de la imagen */
            max-height: 150px; /* Limita la altura máxima de la imagen, puedes ajustar este valor */
        }
        .custom-card img {
            width: 100%;
            border-radius: 10px;
        }
        .custom-card p {
            font-size: 14px;
            color: #333;
            margin: 10px 0;
        }
        .custom-card-h p {
            font-size: 14px;
            color: #333;
            margin: 10px 0;
        }
        .custom-card-h .content {
            flex: 1;
        }
        .button {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            font-size: 14px;
        }
        </style>
        """, unsafe_allow_html=True)


def create_sources_string(source_urls: set[str]):
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i + 1}. {source}\n"
    return sources_string


def response_generator(res: str):
    for word in res.split():
        for char in word:
            yield char
            time.sleep(0.0000000001)
        yield " "
        time.sleep(0.000000001)

def response_generator_2(res: str):
    for word in res.split():
        for char in word:
            yield char
            time.sleep(0.0005)
        yield " "
        time.sleep(0.002)

def set_state(i):
    st.session_state.stage = i


def set_tour_stage(i):
    st.session_state.tour_stage = i


def set_tour(i):
    st.session_state.tour = i


def create_initial_card(image_path, description, button_text, id_state):
    image_file = open(image_path, "rb").read()
    encoded_image = base64.b64encode(image_file).decode()

    st.markdown(f"""
        <div class="custom-card">
            <img src="data:image/jpeg;base64,{encoded_image}" alt="Imagen">
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)

    if id_state == 2:
        st.button(button_text, on_click=set_state, type="primary", args=[2], use_container_width=True)
    elif id_state == 3:
        st.button(button_text, on_click=set_state, type="primary", args=[3], use_container_width=True)
    else:
        st.button(button_text, on_click=set_state, type="primary", args=[4], use_container_width=True)
