from dotenv import load_dotenv
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage

from .handlers.chat_model_start_handler import ChatModelStartHandler
from .tools.report import write_report_tool
from .tools.sql import describe_tables_tool, list_tables, run_query_tool

load_dotenv()


def main():
    handler = ChatModelStartHandler()
    chat = ChatOpenAI(callbacks=[handler])
    tables = list_tables()
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessage(
                content=(
                    "You are an AI that has access to a SQLite database.\n"
                    f"The database has tables of: {tables}\n"
                    "Do not make any assumptions about what tables exist "
                    "or what columns exist. Instead, use the 'describe_tables' function"
                )
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    tools = [describe_tables_tool, run_query_tool, write_report_tool]
    agent = OpenAIFunctionsAgent(llm=chat, prompt=prompt, tools=tools)
    executor = AgentExecutor(agent=agent, memory=memory, tools=tools)

    executor(
        "How many orders are there? Write the result to an html report.",
    )
    executor(
        "Repeat the exact same process for users.",
    )
