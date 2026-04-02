"""Tests for request hooks and error handling."""

import json

from werkzeug.exceptions import BadRequest


def test_bad_request_returns_400(app, client):
    """Test that BadRequest errors return 400, not 401."""
    from app.web.hooks import handle_error

    with app.app_context():
        response, status_code = handle_error(BadRequest("Invalid input"))
        assert status_code == 400
        assert "Invalid input" in response["message"]


def test_upload_no_file_returns_400(client):
    """Test that uploading without a file returns 400."""
    # Sign up to get authenticated
    client.post(
        "/api/auth/signup",
        data=json.dumps({"email": "upload@example.com", "password": "pass123"}),
        content_type="application/json",
    )

    response = client.post("/api/pdfs/", content_type="multipart/form-data")
    assert response.status_code == 400


def test_upload_non_pdf_file_returns_400(client):
    """Test that uploading a non-PDF file returns 400."""
    import io

    client.post(
        "/api/auth/signup",
        data=json.dumps({"email": "upload2@example.com", "password": "pass123"}),
        content_type="application/json",
    )

    data = {"file": (io.BytesIO(b"not a pdf"), "test.txt")}
    response = client.post(
        "/api/pdfs/", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 400
