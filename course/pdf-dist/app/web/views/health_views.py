import logging

import redis as redis_client
from flask import Blueprint, current_app, jsonify
from sqlalchemy import text

from app.web.db import db

bp = Blueprint("health", __name__)

logger = logging.getLogger(__name__)


def check_db() -> bool:
    try:
        db.session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error("DB health check failed: %s", e)
        return False


def check_redis() -> bool:
    redis_uri = current_app.config.get("CELERY", {}).get("broker_url")
    if not redis_uri:
        return True
    try:
        r = redis_client.from_url(redis_uri)
        r.ping()
        return True
    except Exception as e:
        logger.error("Redis health check failed: %s", e)
        return False


@bp.route("/api/healthz")
def health_check():
    checks = {
        "db": check_db(),
        "redis": check_redis(),
    }
    status = "healthy" if all(checks.values()) else "unhealthy"
    http_status = 200 if status == "healthy" else 503
    return jsonify({"status": status, "checks": checks}), http_status
