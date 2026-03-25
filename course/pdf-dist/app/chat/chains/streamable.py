from queue import Queue
from threading import Thread
from typing import Any, Iterator, Optional

from flask import current_app
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.runnables.utils import Input

from app.chat.callbacks.stream import StreamingHandler


class StreamableChain:
    """Mixin that adds synchronous streaming support to a Runnable."""

    def stream(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None,
        **kwargs: Optional[Any],
    ) -> Iterator[str]:
        queue: Queue = Queue()
        handler = StreamingHandler(queue)

        merged_config: RunnableConfig = {**(config or {})}
        callbacks: list[BaseCallbackHandler] = list(
            merged_config.get("callbacks", [])
        )
        callbacks.append(handler)
        merged_config["callbacks"] = callbacks

        def task(app_context: Any) -> None:
            app_context.push()
            if isinstance(self, Runnable):
                self.invoke(input, merged_config)

        Thread(target=task, args=[current_app.app_context()]).start()

        while True:
            token = queue.get()
            if token is None:
                break
            yield token
