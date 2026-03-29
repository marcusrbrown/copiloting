"""Tests for config module."""

import logging
import os


def test_invalid_log_level_falls_back_to_info_with_warning(caplog):
    """Test that invalid LOG_LEVEL env var falls back to INFO with warning."""
    original_value = os.environ.get("LOG_LEVEL")

    with caplog.at_level(logging.WARNING):
        os.environ["LOG_LEVEL"] = "INVALID_LEVEL"

        import importlib
        import app.web.config as config_module
        importlib.reload(config_module)

        assert config_module._LOG_LEVEL == logging.INFO
        assert any("Invalid LOG_LEVEL" in record.message and "falling back to INFO" in record.message for record in caplog.records)

    if original_value is not None:
        os.environ["LOG_LEVEL"] = original_value
    else:
        del os.environ["LOG_LEVEL"]
    importlib.reload(config_module)


def test_valid_log_level_is_used():
    """Test that valid LOG_LEVEL values are used correctly."""
    original_value = os.environ.get("LOG_LEVEL")

    os.environ["LOG_LEVEL"] = "DEBUG"

    import importlib
    import app.web.config as config_module
    importlib.reload(config_module)

    assert config_module._LOG_LEVEL == logging.DEBUG

    if original_value is not None:
        os.environ["LOG_LEVEL"] = original_value
    else:
        del os.environ["LOG_LEVEL"]
    importlib.reload(config_module)


def test_log_format_default_is_text():
    """Test that LOG_FORMAT defaults to 'text'."""
    from app.web.config import Config

    assert Config.LOG_FORMAT == "text"


def test_log_format_json_when_env_set():
    """Test that LOG_FORMAT can be set to 'json' via env var."""
    original_value = os.environ.get("LOG_FORMAT")

    os.environ["LOG_FORMAT"] = "json"

    import importlib
    import app.web.config as config_module
    importlib.reload(config_module)

    from app.web.config import Config

    assert Config.LOG_FORMAT == "json"

    if original_value is not None:
        os.environ["LOG_FORMAT"] = original_value
    else:
        del os.environ["LOG_FORMAT"]
    importlib.reload(config_module)
