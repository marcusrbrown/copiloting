from langchain.chains import ConversationalRetrievalChain

from app.chat.chains.streamable import StreamableChain
from app.chat.chains.traceable import TraceableChain


class RetrievalChain(TraceableChain, StreamableChain, ConversationalRetrievalChain):
    """A conversational retrieval chain that can be traced and streamed."""
