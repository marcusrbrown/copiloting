import os
import sys
from unittest.mock import MagicMock

import pytest

# Set environment variables before any test modules are imported.
# The Flask Config class and several modules read these at import time,
# so they must be available before test collection.
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:")
os.environ.setdefault("UPLOAD_URL", "file:///tmp/test-uploads")
os.environ.setdefault("REDIS_URI", "redis://localhost:6379/0")

# Mock the app.chat package to avoid importing langchain/langfuse/redis
# which have Python 3.14 compatibility issues (stale Pydantic v1 usage).
# This allows testing Flask routes and DB models without the AI/LLM layer.
sys.modules["app.chat"] = MagicMock()
sys.modules["app.chat.create_embeddings"] = MagicMock()
sys.modules["app.chat.score"] = MagicMock()
sys.modules["app.chat.chat"] = MagicMock()
sys.modules["app.chat.models"] = MagicMock()


@pytest.fixture()
def app():
    """Create a Flask application configured for testing."""
    from app.web import create_app

    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with app.app_context():
        from app.web.db import db

        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """Create a Flask test client."""
    return app.test_client()
