import inspect
import os


def get_module_dir() -> str:
    """Returns the absolute path of the directory containing this module.

    Returns:
        str: The absolute path of the directory containing this module.
    """
    frame = inspect.currentframe().f_back
    code = frame.f_back.f_code
    return os.path.dirname(os.path.abspath(code.co_filename))


def get_module_path(file_name: str) -> str:
    """
    Returns the absolute path of a file relative to the directory containing this module.

    Args:
        file_name (str): The name of the file to get the path for.

    Returns:
        str: The absolute path of the file.
    """
    return os.path.abspath(os.path.join(get_module_dir(), file_name))
