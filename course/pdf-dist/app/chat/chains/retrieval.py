from typing import Any, Dict, Iterator, Optional

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig, RunnablePassthrough
from langchain_core.runnables.config import merge_configs

from app.chat.chains.streamable import StreamableChain
from app.chat.chains.traceable import TraceableChain


class RetrievalChain(TraceableChain, StreamableChain):
    """An LCEL-based conversational retrieval chain with streaming and tracing."""

    def __init__(
        self,
        llm: Any,
        condense_question_llm: Any,
        memory: BaseChatMessageHistory,
        retriever: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.llm = llm
        self.condense_question_llm = condense_question_llm
        self.memory = memory
        self.retriever = retriever
        self.metadata = metadata or {}

        parser = StrOutputParser()

        condense_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Given the chat history and the latest user question, "
                    "rephrase the question as a standalone question without the chat history.",
                ),
                MessagesPlaceholder("chat_history"),
                ("human", "{question}"),
            ]
        )

        answer_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Use the following context to answer the user's question:\n\n{context}",
                ),
                MessagesPlaceholder("chat_history"),
                ("human", "{question}"),
            ]
        )

        def get_context(inputs: Dict[str, Any]) -> str:
            chat_history: list[BaseMessage] = self.memory.messages
            standalone = condense_prompt | condense_question_llm | parser
            condensed_question: str = standalone.invoke(
                {"question": inputs["question"], "chat_history": chat_history}
            )
            docs = self.retriever.invoke(condensed_question)
            return "\n\n".join(doc.page_content for doc in docs)

        self._chain = (
            RunnablePassthrough.assign(
                context=get_context,
                chat_history=lambda _: self.memory.messages,
            )
            | answer_prompt
            | llm
            | parser
        )

    @classmethod
    def from_llm(
        cls,
        llm: Any,
        condense_question_llm: Any,
        memory: BaseChatMessageHistory,
        retriever: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "RetrievalChain":
        return cls(
            llm=llm,
            condense_question_llm=condense_question_llm,
            memory=memory,
            retriever=retriever,
            metadata=metadata,
        )

    def _invoke_with_tracing(
        self, question: str, config: Optional[RunnableConfig] = None
    ) -> str:
        trace_callbacks = self._get_trace_callbacks()
        if trace_callbacks:
            extra: RunnableConfig = {"callbacks": trace_callbacks}
            config = merge_configs(config or {}, extra)
        result: str = self._chain.invoke({"question": question}, config)
        self.memory.add_user_message(question)
        self.memory.add_ai_message(result)
        return result

    def stream(
        self,
        input: str,
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> Iterator[str]:
        self.memory.add_user_message(input)
        tokens = []

        for token in StreamableChain.stream(
            self, {"question": input}, config, **kwargs
        ):
            tokens.append(token)
            yield token

        self.memory.add_ai_message("".join(tokens))

    def run(self, question: str) -> str:
        return self._invoke_with_tracing(question)

    def invoke(
        self,
        input: Any,
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> str:
        question = input if isinstance(input, str) else input.get("question", "")
        return self._invoke_with_tracing(question, config)
