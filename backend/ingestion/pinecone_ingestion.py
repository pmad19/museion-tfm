from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import pinecone
import os

from backend.mongo_manager import MongoManager
from utils import get_embedding_function
from backend.helpers.exceptions import StoreExistingPineconeArtworkException, FindMongoArtworkException, FindMongoArtistException

load_dotenv()


class PineconeIngestion:
    def __init__(self):
        self.embedding_function = get_embedding_function()
        self.brief_descriptions_index_name = os.getenv("BRIEF_PINECONE_INDEX")
        self.brief_descriptions_db = PineconeVectorStore(
            embedding=self.embedding_function,
            index_name=self.brief_descriptions_index_name)
        self.general_db = PineconeVectorStore(
            embedding=self.embedding_function,
            index_name=os.getenv("GENERAL_PINECONE_INDEX"))
        self.mongo_controller = MongoManager()

    def ingest_brief_artwork(self, artwork_name: str, artwork_artist: str, artwork_description: str, overwrite=False):
        # TODO: Esta función funciona bien pero el controlador de la mongo hay que revisarlo
        artwork_artist = self.mongo_controller.get_artist(artwork_artist.strip())
        if not artwork_artist:
            raise FindMongoArtistException("Porfavor, para poder insertar una obra de arte, el autor y la obra deben estar registrados en la base de datos")

        artwork_artist_ref = artwork_artist['artist_url_ref']

        artwork = self.mongo_controller.get_artwork_by_artist(artwork_name, artwork_artist_ref, artwork_name)
        if not artwork:
            raise FindMongoArtworkException("Porfavor, para poder insertar una obra de arte, el autor y la obra deben estar registrados en la base de datos")

        artwork_id = artwork['artwork_id']
        artwork_artist_id = artwork_artist['artist_id']
        pinecone_artwork_id = artwork_artist_id + artwork_id

        response = pinecone.Index(os.getenv('PINECONE_API_KEY'), os.getenv('BRIEF_PINECONE_HOST'))\
            .fetch(ids=[pinecone_artwork_id])

        if pinecone_artwork_id in response["vectors"] and (not overwrite):
            raise StoreExistingPineconeArtworkException("¿Estás seguro de que quieres sobrescribirla?")

        document = Document(
            page_content=artwork_description,
            metadata={"artwork-name": artwork['artwork_name_title'],
                      "artwork-artist": artwork_artist['artist_name']},
        )

        self.brief_descriptions_db.add_documents([document], ids=[artwork_artist_id + artwork_id])
        print(f"Meto {artwork_description}")



