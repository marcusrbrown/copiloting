from typing import List

from langchain_core.messages import BaseMessage

from app.chat.memory.history.sql_history import SqlMessageHistory
from app.chat.models import ChatArgs


class WindowedSqlMessageHistory(SqlMessageHistory):
    """SqlMessageHistory that returns only the last *k* human+AI message pairs.

    Each pair consists of two messages (one human, one AI), so the slice is
    ``k * 2`` messages.  This assumes messages are stored in human→AI order;
    messages beyond the window are excluded from the context passed to the LLM.
    """

    k: int = 2

    @property
    def messages(self) -> List[BaseMessage]:
        all_messages = super().messages
        return all_messages[-(self.k * 2) :]


def build_window_buffer_memory(chat_args: ChatArgs):
    return WindowedSqlMessageHistory(
        conversation_id=chat_args.conversation_id,
        k=2,
    )
