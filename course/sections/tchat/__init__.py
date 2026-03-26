from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables import RunnableWithMessageHistory


def main():
    chat = ChatOpenAI(verbose=True)

    prompt = ChatPromptTemplate(
        input_variables=["content", "messages"],
        messages=[
            MessagesPlaceholder(variable_name="messages"),
            HumanMessagePromptTemplate.from_template("{content}"),
        ],
    )

    chain = prompt | chat | StrOutputParser()

    history_store: dict = {}

    def get_history(session_id: str) -> InMemoryChatMessageHistory:
        if session_id not in history_store:
            history_store[session_id] = InMemoryChatMessageHistory()
        return history_store[session_id]

    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_history,
        input_messages_key="content",
        history_messages_key="messages",
    )

    while True:
        try:
            content = input(">> ")
        except EOFError:
            break

        result = chain_with_history.invoke(
            {"content": content},
            config={"configurable": {"session_id": "default"}},
        )
        print(result)


load_dotenv()
