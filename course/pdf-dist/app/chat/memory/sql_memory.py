from app.chat.memory.history.sql_history import SqlMessageHistory


def build_memory(chat_args):
    return SqlMessageHistory(conversation_id=chat_args.conversation_id)
