from dotenv import load_dotenv
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
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

    code_prompt = PromptTemplate(
        template="Write a very short {language} function that will {task}",
        input_variables=["language", "task"],
    )
    test_prompt = PromptTemplate(
        input_variables=["language", "code"],
        template="Write a test for the following {language} code:\n{code}",
    )

    code_chain = LLMChain(llm=llm, prompt=code_prompt, output_key="code")
    test_chain = LLMChain(llm=llm, prompt=test_prompt, output_key="test")

    chain = SequentialChain(
        chains=[code_chain, test_chain],
        input_variables=["language", "task"],
        output_variables=["code", "test"],
    )

    result = chain({"language": args.language, "task": args.task})

    print("Code:")
    print(result["code"])
    print("Test:")
    print(result["test"])
