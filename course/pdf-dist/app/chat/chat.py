from langchain.chat_models import ChatOpenAI
from app.chat.models import ChatArgs
from app.chat.vectorstores import retriever_map
from app.chat.llms import llm_map
from app.chat.memory import memory_map
from app.chat.chains.retrieval import RetrievalChain
from app.chat.score import random_component_by_score
from app.web.api import get_conversation_components, set_conversation_components


def select_component(component_type, component_map, chat_args):
    components = get_conversation_components(chat_args.conversation_id)
    previous_component = components.get(component_type)
    if previous_component:
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        random_name = random_component_by_score(component_type, component_map)
        builder = component_map[random_name]
        return random_name, builder(chat_args)


def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """

    retriever_name, retriever = select_component("retriever", retriever_map, chat_args)
    llm_name, llm = select_component("llm", llm_map, chat_args)
    memory_name, memory = select_component("memory", memory_map, chat_args)

    set_conversation_components(
        conversation_id=chat_args.conversation_id,
        llm=llm_name,
        memory=memory_name,
        retriever=retriever_name,
    )

    return RetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=ChatOpenAI(streaming=False),
        memory=memory,
        retriever=retriever,
        metadata=chat_args.metadata,
    )
