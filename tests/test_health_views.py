"""Tests for health check views."""

import importlib
import json
import logging
import os
from unittest.mock import MagicMock, patch


def test_health_check_returns_200_when_db_ok(client):
    """Test that /api/healthz returns 200 with healthy status when DB is reachable."""
    with patch("app.web.views.health_views.check_redis", return_value=True):
        response = client.get("/api/healthz")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "checks" in data
    assert data["checks"]["db"] is True


def test_health_check_includes_redis_check(client):
    """Test that /api/healthz includes a redis check."""
    with patch("app.web.views.health_views.check_redis", return_value=True):
        response = client.get("/api/healthz")
    data = response.get_json()
    assert "redis" in data["checks"]


def test_health_check_redis_ok_when_not_configured(app, client):
    """Test that redis check passes when Redis is not configured (broker_url falsy)."""
    from app.web.views.health_views import check_redis

    with app.app_context():
        original_celery = app.config.get("CELERY", {}).copy()
        app.config["CELERY"] = {**original_celery, "broker_url": False}
        try:
            assert check_redis() is True
        finally:
            app.config["CELERY"] = original_celery


def test_check_redis_returns_false_when_ping_fails(app):
    """Test that check_redis returns False when the broker is configured but unreachable."""
    from app.web.views.health_views import check_redis

    with app.app_context():
        original_celery = app.config.get("CELERY", {}).copy()
        app.config["CELERY"] = {
            **original_celery,
            "broker_url": "redis://localhost:6379/0",
        }
        try:
            mock_conn = MagicMock()
            mock_conn.ping.side_effect = Exception("Connection refused")
            with patch(
                "app.web.views.health_views.redis_client.from_url",
                return_value=mock_conn,
            ):
                assert check_redis() is False
        finally:
            app.config["CELERY"] = original_celery


def test_health_check_returns_503_when_db_fails(client):
    """Test that /api/healthz returns 503 when DB is unreachable."""
    with patch("app.web.views.health_views.check_db", return_value=False), \
         patch("app.web.views.health_views.check_redis", return_value=True):
        response = client.get("/api/healthz")
    assert response.status_code == 503
    data = response.get_json()
    assert data["status"] == "unhealthy"
    assert data["checks"]["db"] is False


def test_health_check_returns_correlation_id_header(client):
    """Test that responses include X-Correlation-ID header."""
    with patch("app.web.views.health_views.check_redis", return_value=True):
        response = client.get("/api/healthz")
    assert "X-Correlation-ID" in response.headers


def test_health_check_propagates_request_correlation_id(client):
    """Test that a supplied X-Correlation-ID is echoed back in the response."""
    correlation_id = "test-correlation-id-1234"
    with patch("app.web.views.health_views.check_redis", return_value=True):
        response = client.get("/api/healthz", headers={"X-Correlation-ID": correlation_id})
    assert response.headers.get("X-Correlation-ID") == correlation_id


def test_invalid_log_level_falls_back_to_info():
    """Test that an invalid LOG_LEVEL env var falls back to INFO."""
    import app.web.config as config_module

    try:
        with patch.dict(os.environ, {"LOG_LEVEL": "GARBAGE"}):
            importlib.reload(config_module)
            assert config_module.Config.LOG_LEVEL == logging.INFO
    finally:
        importlib.reload(config_module)


def test_json_formatter_includes_extra_fields(app):
    """Test that JsonFormatter serializes extra fields into the JSON output."""
    from app.web import JsonFormatter

    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="hello",
        args=(),
        exc_info=None,
    )
    record.correlation_id = "abc-123"
    record.status = 200

    output = json.loads(formatter.format(record))
    assert output["message"] == "hello"
    assert output["correlation_id"] == "abc-123"
    assert output["status"] == 200
    assert "time" in output
    assert output["level"] == "INFO"
