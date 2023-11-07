import sqlite3
from pydantic.v1 import BaseModel
from typing import Any, List
from langchain.tools import Tool

from course.utilities import get_module_path

__all__ = ["describe_tables_tool", "list_tables", "run_query_tool"]

db_path = get_module_path("../db.sqlite")


def run_sqlite_query(query: str) -> list[Any] | str:
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        try:
            c.execute(query)
            return c.fetchall()
        except sqlite3.OperationalError as e:
            return f"The following error ocurred: {e}"


class RunQueryArgsSchema(BaseModel):
    query: str


run_query_tool = Tool.from_function(
    args_schema=RunQueryArgsSchema,
    description="Run a SQLite query",
    func=run_sqlite_query,
    name="run_sqlite_query",
)


def list_tables() -> str:
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = run_sqlite_query(query)
    return "\n".join(table[0] for table in tables if table[0] is not None)


def describe_tables(table_names: list[str]) -> str:
    tables = ", ".join("'" + table + "'" for table in table_names)
    rows = run_sqlite_query(
        f"SELECT sql FROM sqlite_master WHERE type='table' and name IN ({tables});"
    )
    return "\n".join(row[0] for row in rows if row[0] is not None)


class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]


describe_tables_tool = Tool.from_function(
    args_schema=DescribeTablesArgsSchema,
    description="Given a list of table names, returns the schema of those tables",
    func=describe_tables,
    name="describe_tables",
)
