from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from course.sections.utilities import get_module_path
from .redundant_filter_retriever import RedundantFilterRetriever


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

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Use the following context to answer the question:\n\n{context}",
            ),
            ("human", "{question}"),
        ]
    )

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | chat
        | StrOutputParser()
    )

    result = chain.invoke("What is an interesting fact about the English language?")
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
