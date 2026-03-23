from langchain.embeddings import OpenAIEmbeddings


embeddings = None


def get_embeddings():
    global embeddings

    if embeddings is None:
        embeddings = OpenAIEmbeddings()

    return embeddings
