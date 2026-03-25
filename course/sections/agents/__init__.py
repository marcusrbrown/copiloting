from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver

from .handlers.chat_model_start_handler import ChatModelStartHandler
from .tools.report import write_report_tool
from .tools.sql import describe_tables_tool, list_tables, run_query_tool

load_dotenv()


def main():
    handler = ChatModelStartHandler()
    chat = ChatOpenAI(callbacks=[handler])
    tables = list_tables()
    system_msg = (
        "You are an AI that has access to a SQLite database.\n"
        f"The database has tables of: {tables}\n"
        "Do not make any assumptions about what tables exist "
        "or what columns exist. Instead, use the 'describe_tables' function"
    )
    tools = [describe_tables_tool, run_query_tool, write_report_tool]
    checkpointer = MemorySaver()
    executor = create_agent(
        model=chat, tools=tools, system_prompt=system_msg, checkpointer=checkpointer
    )

    config = {"configurable": {"thread_id": "default"}}

    for question in [
        "How many orders are there? Write the result to an html report.",
        "Repeat the exact same process for users.",
    ]:
        result = executor.invoke(
            {"messages": [HumanMessage(content=question)]}, config
        )
        last_msg = result["messages"][-1]
        if hasattr(last_msg, "content"):
            print(last_msg.content)
