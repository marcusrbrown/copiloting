from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
import os
from .redundant_filter_retriever import RedundantFilterRetriever


def get_module_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_module_path(file_name):
    return os.path.join(get_module_dir(), file_name)


def main():
    chat = ChatOpenAI()
    embeddings = OpenAIEmbeddings()
    chroma = Chroma(
        embedding_function=embeddings,
        persist_directory=get_module_path(".embeddings"),
    )
    retriever = RedundantFilterRetriever(
        embeddings=embeddings,
        chroma=chroma,
    )

    chain = RetrievalQA.from_chain_type(
        chain_type="stuff",
        llm=chat,
        retriever=retriever,
    )

    result = chain.run("What is an interesting fact about the English language?")
    print(result)


def create_embeddings():
    embeddings = OpenAIEmbeddings()

    text_splitter = CharacterTextSplitter(
        chunk_overlap=0,
        chunk_size=200,
        separator="\n",
    )

    file_path = get_module_path("facts.txt")
    loader = TextLoader(file_path=file_path)
    docs = loader.load_and_split(text_splitter=text_splitter)

    db = Chroma.from_documents(
        docs, embedding=embeddings, persist_directory=get_module_path(".embeddings")
    )

    results = db.similarity_search(
        "What is an interesting fact about the English language?"
    )

    for result in results:
        print("\n")
        print(result.page_content)


load_dotenv()
