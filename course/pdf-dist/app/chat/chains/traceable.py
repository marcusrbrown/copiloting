from typing import Any

from langchain_core.callbacks import BaseCallbackHandler


class TraceableChain:
    """Mixin that adds Langfuse tracing callbacks to a chain invocation."""

    def _get_trace_callbacks(self) -> list[BaseCallbackHandler]:
        """Return a list of Langfuse callbacks if tracing metadata is present."""
        callbacks: list[BaseCallbackHandler] = []
        if not hasattr(self, "metadata"):
            return callbacks
        try:
            from langfuse.model import CreateTrace

            from app.chat.tracing.langfuse import langfuse

            trace = langfuse.trace(
                CreateTrace(
                    id=self.metadata.get("conversation_id"),
                    metadata=self.metadata,
                )
            )
            callbacks.append(trace.get_langchain_handler())
        except Exception:
            pass
        return callbacks
