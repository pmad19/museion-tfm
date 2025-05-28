from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_groq import ChatGroq

from backend.llms.retrievers.description_retriever.metadata_retriever import get_metadata_retriever, get_vector_store
from langchain_core.documents import Document
from collections import Counter


class DescriptionRetriever:
    def __init__(self):
        self.metadata_retriever = get_metadata_retriever()
        self.vector_store = get_vector_store()
        self.llm = ChatGroq( model="llama-3.1-8b-instant")

    def get_artworks(self, query: str) -> [Document]:
        non_filter_documents = []
        try:
            metadata_filtered_documents = self.metadata_retriever.invoke(query)
        except:
            metadata_filtered_documents = []
        similar_questions = self.get_similar_questions(query)
        non_filter_documents += self.vector_store.similarity_search(query, k=10)
        for question in similar_questions:
            non_filter_documents += self.vector_store.similarity_search(question, k=10)
        relevant_documents = metadata_filtered_documents + non_filter_documents
        documents = self.remove_duplicated_documents(relevant_documents)
        relevant_documents += self.filter_recurrent_documents(relevant_documents)
        return documents[:12]

    def filter_recurrent_documents(self, docs: [Document]) -> [Document]:
        root_documents = [document.metadata.get("artwork_id") for document in docs]
        counter = Counter(root_documents)
        docs_id = [doc for doc, quantity in counter.items() if quantity > 2]
        relevant_documents = self.vector_store.similarity_search("", k=15, filter={"artwork_id": {"$in": docs_id}})
        return relevant_documents

    @staticmethod
    def remove_duplicated_documents(docs: [Document]) -> [Document]:
        seen = set()
        unique_documents = []
        for doc in docs:
            if doc.id not in seen:
                unique_documents.append(doc)
                seen.add(doc.id)
        return unique_documents

    def get_similar_questions(self, query: str) -> [str]:
        prompt_template = PromptTemplate.from_template(
            "Dada la siguiente pregunta, reescríbela tres veces de manera breve, concisa, y enfocada en la idea principal. Devuelve únicamente las preguntas linea por linea, sin ninguna indexacción ni caracter. Ejemplo:\n"
            "¿Qué simbolizan las figuras más utilizadas en las obras del museo?\n¿Qué figuras alegóricas son las más comunes en las obras?\n¿Cuáles son las figuras alegóricas más representativas del museo?"
            "Pregunta: {question}\n"
            "Reescrituras (separadas por saltos de linea):")

        chain = prompt_template | self.llm
        reformulations = chain.invoke({"question": query}).content
        question_list = [q.strip() for q in reformulations.split('\n')]
        return question_list

