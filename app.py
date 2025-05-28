import streamlit as st

from backend.ingestion.pinecone_ingestion import PineconeIngestion
from backend.helpers.exceptions import StoreExistingPineconeArtworkException, FindMongoArtworkException, FindMongoArtistException


def ingesta_completa():
    st.title("Ingesta de Datos Completos")

    option = st.selectbox("Selecciona una opción:", ["Artistas", "Obras", "Actividades"])

    if option == "Artistas":
        st.subheader("Añadir Artista")
        nombre = st.text_input("Nombre del artista")
        descripcion = st.text_area("Descripción del artista")
        lugar_nacimiento = st.text_input("Lugar de nacimiento")
        anio_nacimiento = st.text_input("Año de nacimiento")
        lugar_muerte = st.text_input("Lugar de muerte")
        fecha_muerte = st.text_input("Fecha de muerte")
        url = st.text_input("URL relacionada")

        if st.button("Añadir Artista"):
            st.success(f"Artista '{nombre}' añadido correctamente.")

    elif option == "Obras":
        st.subheader("Añadir obra de arte")
        nombre_obra = st.text_input("Nombre de la obra")

        col1, col2 = st.columns([1, 5])
        with col1:
            st.subheader('Artista')
        with col2:
            anonimo = st.checkbox("Anónimo", key="anonimo")

        artist_name = st.text_input("Nombre del artista", disabled=st.session_state.get("anonimo", False))
        artist_url = st.text_input("Link del artista", disabled=st.session_state.get("anonimo", False))


        col1, col2 = st.columns([5, 1])
        with col1:
            localizacion = st.text_input("Localización", disabled=st.session_state.get("no_expuesta", False))
        with col2:
            st.text('')
            st.text('')
            no_expuesta = st.checkbox("No expuesta", key="no_expuesta")

        fecha_obra = st.text_input("Fecha de la obra")
        descripcion_obra = st.text_area("Descripción de la obra")
        tamano = st.text_input("Tamaño de la obra")
        tipo_canvas = st.text_input("Tipo de canvas")
        url_obra = st.text_input("Link de la obra")

        if st.button("Añadir Obra"):
            st.success(f"Obra '{nombre_obra}' añadida correctamente.")

    elif option == "Actividades":
        st.subheader("Añadir Actividad")
        st.info("Esta sección está en desarrollo.")


def ingesta_simple():
    st.title("Ingesta de datos de localización")
    st.text("""En esta sección, tienes la posibilidad de insertar información sobre las obras que desees añadir al sistema de localización de obras dentro del museo. Los datos que proporciones serán fundamentales para que los usuarios puedan buscar y encontrar obras de manera eficiente.""")

    st.subheader("¿Qué tipo de información puedes incluir?")
    st.markdown("- **Título de la obra:** El nombre principal que identifica la pieza.")
    st.markdown("- **Autor:** El creador de la obra.")
    st.markdown("- **Descripción:** Un texto libre que describa la obra, su contexto, técnica utilizada, y cualquier detalle relevante.")

    st.subheader("¿Por qué es importante esta información?")
    st.text("Los usuarios podrán realizar búsquedas utilizando palabras, fragmentos de texto o términos que coincidan con la descripción, título o palabras clave que hayas proporcionado. Esto les permitirá encontrar obras de forma rápida y eficiente, incluso si no recuerdan el título exacto o el autor.")

    st.subheader("Ejemplo práctico")
    st.text('Imaginemos que añadimos la siguiente descripción de la obra "Autorretrato con gorra y dos cadenas" del reconocido autor Rembrandt: ')
    st.markdown('*_"Un retrato pintado al óleo de un hombre de mediana edad con bigote y expresión seria. Viste ropas oscuras con una textura densa y detalles dorados, como collares o adornos en la vestimenta. Lleva un gorro negro y tiene el cabello rizado y voluminoso a los lados. El fondo es oscuro, con un contraste claro entre la luz del rostro y las sombras, característico del claroscuro. La figura está representada de busto y casi de frente, sin demasiados adornos ni elementos adicionales. Parece un autorretrato de un pintor del siglo XVII."_*')
    st.text("El visitante podría encontrar la obra explicando la siguiente descripción de la misma: ")
    st.markdown("*_Estoy buscando un autorretrato de un señor con bigote y sombrero del siglo XVII, ¿Dónde está?_*")

    st.subheader("Información de la obra a insertar")
    artwork_name = st.text_input("Nombre de la obra")
    artwork_artist = st.text_input("Autor de la obra")
    artwork_description = st.text_area("Descripción de la obra")

    overwrite_requested = st.session_state.get("overwrite_requested", False)

    if st.button("Añadir obra") and not overwrite_requested:
        try:
            pinecone_ingestion.ingest_brief_artwork(
                artwork_name=artwork_name,
                artwork_artist=artwork_artist,
                artwork_description=artwork_description)
            st.success("Obra añadida correctamente.")
        except FindMongoArtistException as e:
            st.error(
                f"Error: No se ha encontrado al artista en nuestra base de datos. Por favor, para poder insertar una obra de arte primero debe introducirse al artista en la base de datos.")
        except FindMongoArtworkException as e:
            st.error(
                f"Error: No se ha encontrado la obra en nuestra base de datos. Por favor, para poder insertar una obra de arte primero debe introducirse la obra en la base de datos.")
        except StoreExistingPineconeArtworkException as e:
            st.error(f"Error: Parece que ya existe una obra con el mismo nombre y autor, ¿deseas sobrescribirla?")
            st.button('Sobreescribir',
                      on_click=pinecone_ingestion.ingest_brief_artwork,
                      args=[artwork_name, artwork_artist, artwork_description, True])



st.sidebar.title("Navegación")
page = st.sidebar.radio("Selecciona una página:", ["Ingesta de datos completos", "Ingesta de datos simples"])

pinecone_ingestion = PineconeIngestion()

if page == "Ingesta de datos completos":
    ingesta_completa()
elif page == "Ingesta de datos simples":
    ingesta_simple()