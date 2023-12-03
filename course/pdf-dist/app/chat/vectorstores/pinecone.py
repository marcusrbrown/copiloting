import os
import pinecone
from langchain.vectorstores.pinecone import Pinecone
from app.chat.embeddings.openai import embeddings


pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT"],
)

vectorstore = Pinecone.from_existing_index(
    index_name=os.environ["PINECONE_INDEX_NAME"], embedding=embeddings
)


def build_retriever(chat_args, k):
    search_kwargs = {"filter": {"pdf_id": chat_args.pdf_id}, "k": k}
    return vectorstore.as_retriever(search_kwargs=search_kwargs)
