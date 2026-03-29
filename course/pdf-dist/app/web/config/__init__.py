import logging
import os

from dotenv import load_dotenv

load_dotenv()

_LOG_LEVEL_NAME = os.environ.get("LOG_LEVEL", "INFO").upper()
_LOG_LEVEL = getattr(logging, _LOG_LEVEL_NAME, None)
if not isinstance(_LOG_LEVEL, int):
    logging.warning("Invalid LOG_LEVEL %r, falling back to INFO", _LOG_LEVEL_NAME)
    _LOG_LEVEL = logging.INFO


class Config:
    SESSION_PERMANENT = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    UPLOAD_URL = os.environ["UPLOAD_URL"]
    CELERY = {
        "broker_url": os.environ.get("REDIS_URI", False),
        "task_ignore_result": True,
        "broker_connection_retry_on_startup": False,
    }
    LOG_LEVEL: int = _LOG_LEVEL
    LOG_FORMAT: str = os.environ.get("LOG_FORMAT", "text")
