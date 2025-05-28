from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document

from utils import get_embedding_function
from dotenv import load_dotenv

load_dotenv()


class LocationRetriever:
    def __init__(self):
        self.db = PineconeVectorStore(embedding=get_embedding_function(), index_name="artwork-location-descriptions")

    def get_artworks(self, query: str) -> [Document]:
        return self.db.similarity_search(query, k=5)
