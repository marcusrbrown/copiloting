"""Tests for the Flask application factory."""

from flask import Flask


def test_create_app(app):
    """Test that create_app returns a Flask instance."""
    assert isinstance(app, Flask)


def test_app_testing_config(app):
    """Test that the app is configured for testing."""
    assert app.config["TESTING"] is True


def test_app_has_blueprints(app):
    """Test that all expected blueprints are registered."""
    expected = {"auth", "pdf", "score", "conversation", "client"}
    registered = set(app.blueprints.keys())
    assert expected.issubset(registered)
