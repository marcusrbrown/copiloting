import os
import pinecone
from langchain_community.vectorstores.pinecone import Pinecone
from app.chat.embeddings.openai import get_embeddings


vectorstore = None


def get_vectorstore():
    global vectorstore

    if vectorstore is None:
        pinecone.init(
            api_key=os.environ["PINECONE_API_KEY"],
            environment=os.environ["PINECONE_ENVIRONMENT"],
        )

        vectorstore = Pinecone.from_existing_index(
            index_name=os.environ["PINECONE_INDEX_NAME"], embedding=get_embeddings()
        )

    return vectorstore


def build_retriever(chat_args, k):
    search_kwargs = {"filter": {"pdf_id": chat_args.pdf_id}, "k": k}
    return get_vectorstore().as_retriever(search_kwargs=search_kwargs)
