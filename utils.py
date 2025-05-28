from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import re

from langchain_pinecone import PineconeEmbeddings
from langchain_openai import AzureOpenAIEmbeddings


PROMPT_TEMPLATE_SOURCE = """
Dado el siguiente texto:
{source}

Devuelve al menos 4 de las siguientes categorías (únicamente en las siguientes) a las que puede hacer referencia: 
{topics} 

Y devuelvelo en una lista entre []
___________________________
Ejemplo: ["RENACIMIENTO", "SIGLO_XVI", "SIGLO_XV", "PINTURA_ITALIANA"]
"""

PROMPT_TEMPLATE_QUESTION = """
Dada la siguiente pregunta acerca de arte: 
{question}

Y dadas las siguientes posibles temáticas a las que puede hacer referencia la pregunta: 
{topics}

Devuelve al menos 4 de las temáticas anteriores en una lista entre [] o devuelve [] si la pregunta no hace referencia a 
ninguno de estos temas directamente y pregunta sobre un cuadro. Devúelve una lista como las que aparecen tras Respuesta:
__________________________
Pregunta: ¿Me puedes explicar la moda en el renacimiento?
Respuesta: ["MODA", "JOYAS", "RENACIMIENTO", "PINTURA_ITALIANA", "SIGLO_XV", "SIGLO_XVI"]
Pregunta: ¿Por qué la mujer de la obra Retrato de Giovanna degli porta tantas joyas?
Respuesta: ["MODA", "JOYAS", "RENACIMIENTO", "PINTURA_ITALIANA", "SIGLO_XV", "SIGLO_XVI"]
"""


def read_txt(path):
    with open(path, 'r', encoding='utf-8') as archivo:
        content = archivo.read()
    return content


def format_list(input_str):
    regex = r'\["(.*?)"\]'
    matches = re.findall(regex, input_str)
    res = []
    for match in matches:
        items = [item.strip().replace('"', "") for item in match.split(',')]
        res.extend(items)
    return res


def get_embedding_function():
    #embeddings = OllamaEmbeddings(model="nomic-embed-text")
    #embeddings = OllamaEmbeddings(model="intfloat-multilingual-e5-large:f16")
    embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-3-large",
    )
    return embeddings


def generate_topic_question(question: str):
    topics_file_path = 'sources/categorias.txt'
    topics = read_txt(topics_file_path)

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_SOURCE)
    prompt = prompt_template.format(topics=topics, source=source)
    model = Ollama(model="mistral", temperature=0)
    response = model.invoke(prompt)
    topics_list = format_list(response)
    return topics_list


def generate_topic_source(source: str):
    topics_file_path = 'sources/categorias.txt'
    topics = read_txt(topics_file_path)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_SOURCE)
    prompt = prompt_template.format(topics=topics, source=source)
    model = Ollama(model="mistral", temperature=0)
    response = model.invoke(prompt)
    topics_list = format_list(response)
    return topics_list
