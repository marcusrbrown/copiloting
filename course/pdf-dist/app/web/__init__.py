import json
import logging

from flask import Flask
from flask_cors import CORS

from app.web.db import db, init_db_command
from app.web.db import models
from app.celery import celery_init_app
from app.web.config import Config
from app.web.hooks import load_logged_in_user, log_request, handle_error
from app.web.views import (
    auth_views,
    pdf_views,
    score_views,
    client_views,
    conversation_views,
    health_views,
)

# Attributes present on every LogRecord that should not be treated as extra fields.
_STANDARD_LOG_ATTRS = frozenset(
    {
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "id",
        "levelname",
        "levelno",
        "lineno",
        "message",
        "module",
        "msecs",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "taskName",
        "thread",
        "threadName",
    }
)


class JsonFormatter(logging.Formatter):
    """Formats log records as JSON, including any extra fields."""

    def format(self, record: logging.LogRecord) -> str:
        record.message = record.getMessage()
        data: dict = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.message,
        }
        for key, value in record.__dict__.items():
            if key not in _STANDARD_LOG_ATTRS:
                data[key] = value
        if record.exc_info and not record.exc_text:
            record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            data["exception"] = record.exc_text
        return json.dumps(data, default=str)


def create_app():
    app = Flask(__name__, static_folder="../../client/build")
    app.url_map.strict_slashes = False
    app.config.from_object(Config)

    configure_logging(app)
    register_extensions(app)
    register_hooks(app)
    register_blueprints(app)
    if Config.CELERY["broker_url"]:
        celery_init_app(app)

    return app


def configure_logging(app):
    log_level = app.config.get("LOG_LEVEL", logging.INFO)
    log_format = app.config.get("LOG_FORMAT", "text")

    if log_format == "json":
        formatter: logging.Formatter = JsonFormatter()
    else:
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    # force=True removes pre-existing handlers so reconfiguring in tests is idempotent.
    logging.basicConfig(level=log_level, handlers=[handler], force=True)
    app.logger.setLevel(log_level)


def register_extensions(app):
    db.init_app(app)
    app.cli.add_command(init_db_command)


def register_blueprints(app):
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(pdf_views.bp)
    app.register_blueprint(score_views.bp)
    app.register_blueprint(conversation_views.bp)
    app.register_blueprint(health_views.bp)
    app.register_blueprint(client_views.bp)


def register_hooks(app):
    CORS(app)
    app.before_request(load_logged_in_user)
    app.after_request(log_request)
    app.register_error_handler(Exception, handle_error)
