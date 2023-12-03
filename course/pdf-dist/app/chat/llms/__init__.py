from functools import partial
from .chat_openai import build_llm

llm_map = {
    "gpt-3.5-turbo": partial(build_llm, model_name="gpt-3.5-turbo"),
    "gpt-4": partial(build_llm, model_name="gpt-4"),
}
