from queue import Queue
from threading import Thread
from typing import Any, Optional
from flask import current_app
from langchain.chains.base import Chain
from langchain.schema.runnable.config import RunnableConfig
from langchain.schema.runnable.utils import Input

from app.chat.callbacks.stream import StreamingHandler


class StreamableChain(Chain):
    """A chain that can be streamed."""

    def stream(
        self,
        input: Input,  # pylint: disable=redefined-builtin
        config: Optional[RunnableConfig] = None,
        **kwargs: Optional[Any],
    ):
        queue = Queue()
        handler = StreamingHandler(queue)

        def task(app_context):
            app_context.push()
            self(input, config, callbacks=[handler])

        Thread(target=task, args=[current_app.app_context()]).start()

        while True:
            token = queue.get()
            if token is None:
                break
            yield token
