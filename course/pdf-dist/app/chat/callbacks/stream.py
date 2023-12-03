from queue import Queue
from typing import Any, Dict, List, Optional
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema.messages import BaseMessage
from langchain.schema.output import LLMResult


class StreamingHandler(BaseCallbackHandler):
    """Implements a callback handler for streaming chat models."""

    def __init__(self, queue: Queue):
        self.queue = queue
        self.streaming_run_ids = set()

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        if serialized["kwargs"].get("streaming", False):
            self.streaming_run_ids.add(run_id)

    def on_llm_new_token(self, token, **kwargs):
        self.queue.put(token)

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        if run_id in self.streaming_run_ids:
            self.queue.put(None)
            self.streaming_run_ids.remove(run_id)

    def on_llm_error(self, error: BaseException, **kwargs: Any) -> Any:
        return self.queue.put(None)
