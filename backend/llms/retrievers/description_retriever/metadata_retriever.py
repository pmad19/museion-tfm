from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore
from utils import get_embedding_function
from dotenv import load_dotenv

load_dotenv()

INDEX_NAME = "thyssen-index"

vectorstore = PineconeVectorStore.from_existing_index(
        index_name=INDEX_NAME,
        embedding=get_embedding_function()
    )

metadata_field_info = [
    AttributeInfo(
        name="artist_name",
        description="The name of the artwork artist. Valid values are ['Caravaggio (Michelangelo Merisi)', 'Canaletto (Giovanni Antonio Canal)', 'Alberto Durero', 'Duccio di Buoninsegna', 'Velázquez (Diego Rodríguez de Silva y Velázquez)', 'Jan van Eyck', 'Harmensz. van Rijn Rembrandt', 'Édouard Manet', 'Joan Miró', 'Claude Monet', 'Piet Mondrian', 'Salvador Dalí', 'Edgar Degas', 'Berthe Morisot', 'Paul Gauguin', 'Francisco de Goya', 'El Greco (Doménikos Theotokópoulos)', 'Vincent van Gogh', 'Ernst Ludwig Kirchner', 'Georgia O'Keeffe', 'Edward Hopper']",
        type="list[string]",
    ),
    AttributeInfo(
        name="is_exposed",
        description="If the artwork is exposed in the museum or not",
        type="boolean"
    ),
    AttributeInfo(
        name="exposed_room",
        description="Room in which the artwork is exposed",
        type="string"
    ),
]

document_content_description = """
Summary of an artwork belongs to Thyssen Museum that the user wants to obtain information. 
If the query refers to an artist similar to the possible values try to rewrite the artist name to match the possible artist name values.
ALWAYS use the original query.
"""


def get_metadata_retriever():
    llm = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant")

    retriever = SelfQueryRetriever.from_llm(
        llm, vectorstore, document_content_description, metadata_field_info, enable_limit=True,
        search_kwargs={"k": 10}
    )
    return retriever


def get_vector_store():
    embedding_function = get_embedding_function()
    db = PineconeVectorStore(embedding=embedding_function, index_name=INDEX_NAME)
    return db


