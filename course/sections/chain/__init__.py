from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import argparse


def main():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--task", default="return a list of numbers", type=str, help="task to perform"
    )
    parser.add_argument(
        "--language", default="python", type=str, help="language to use"
    )
    args = parser.parse_args()

    load_dotenv()

    llm = OpenAI()
    parser_out = StrOutputParser()

    code_prompt = PromptTemplate(
        template="Write a very short {language} function that will {task}",
        input_variables=["language", "task"],
    )
    test_prompt = PromptTemplate(
        input_variables=["language", "code"],
        template="Write a test for the following {language} code:\n{code}",
    )

    chain = RunnablePassthrough.assign(code=code_prompt | llm | parser_out) | RunnablePassthrough.assign(
        test=test_prompt | llm | parser_out
    )

    result = chain.invoke({"language": args.language, "task": args.task})

    print("Code:")
    print(result["code"])
    print("Test:")
    print(result["test"])
