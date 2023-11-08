from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)


def run():
    pass


load_dotenv()

chat = ChatOpenAI(verbose=True)

memory = ConversationSummaryMemory(
    # chat_memory=FileChatMessageHistory("messages.json"),
    llm=chat,
    memory_key="messages",
    return_messages=True,
)

prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}"),
    ],
)

chain = LLMChain(llm=chat, memory=memory, prompt=prompt, verbose=True)

while True:
    try:
        content = input(">> ")
    except EOFError:
        break

    result = chain({"content": content})
    print(result["text"])
