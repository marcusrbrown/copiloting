"""Tests for health check views."""

from unittest.mock import patch


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
