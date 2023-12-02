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
