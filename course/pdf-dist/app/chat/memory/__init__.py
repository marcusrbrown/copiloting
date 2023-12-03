from .sql_memory import build_memory
from .window_memory import build_window_buffer_memory

memory_map = {
    "sql_buffer_memory": build_memory,
    "sql_window_memory": build_window_buffer_memory,
}
