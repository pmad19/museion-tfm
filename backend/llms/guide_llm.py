from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_groq import ChatGroq
from backend.llms.prompts import _system_guide_prompt, contextualize_q_prompt
from dotenv import load_dotenv
from backend.llms.retrievers.description_retriever.metadata_retriever import get_metadata_retriever

load_dotenv()

llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")


def run_guide_llm(query: str, chat_history: ChatMessageHistory):
    retriever = get_metadata_retriever()
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", _system_guide_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    qa_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    qa_chain = qa_chain.pick('answer')

    return qa_chain.stream({"input": query, "chat_history": chat_history})

if __name__ == '__main__':
    hola = get_fine_retriever().invoke("Háblame del expresionismo")
    for document in hola:
        print(f"Pieza perteneciente a la obra {document.metadata.get('artwork_name')} del autor {document.metadata.get('artist_name')}")
        print(document.page_content)
        print("---------------")