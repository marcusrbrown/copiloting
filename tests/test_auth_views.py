"""Tests for authentication views."""

import json


def test_signup(client):
    """Test user signup creates a new user and sets session."""
    response = client.post(
        "/api/auth/signup",
        data=json.dumps({"email": "new@example.com", "password": "pass123"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["email"] == "new@example.com"
    assert "id" in data
    assert "password" not in data


def test_signin(client):
    """Test user signin with valid credentials."""
    client.post(
        "/api/auth/signup",
        data=json.dumps({"email": "signin@example.com", "password": "pass123"}),
        content_type="application/json",
    )

    response = client.post(
        "/api/auth/signin",
        data=json.dumps({"email": "signin@example.com", "password": "pass123"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["email"] == "signin@example.com"


def test_signin_wrong_password(client):
    """Test signin with incorrect password returns 400."""
    client.post(
        "/api/auth/signup",
        data=json.dumps({"email": "wrong@example.com", "password": "correct"}),
        content_type="application/json",
    )

    response = client.post(
        "/api/auth/signin",
        data=json.dumps({"email": "wrong@example.com", "password": "incorrect"}),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_signout(client):
    """Test signout clears the session."""
    response = client.post("/api/auth/signout")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Successfully logged out."


def test_get_user_unauthenticated(client):
    """Test getting user when not logged in returns null."""
    response = client.get("/api/auth/user")
    assert response.status_code == 200
    assert response.get_json() is None


def test_get_user_authenticated(client):
    """Test getting user when logged in returns user data."""
    client.post(
        "/api/auth/signup",
        data=json.dumps({"email": "auth@example.com", "password": "pass123"}),
        content_type="application/json",
    )

    response = client.get("/api/auth/user")
    assert response.status_code == 200
    data = response.get_json()
    assert data["email"] == "auth@example.com"
