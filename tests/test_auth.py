import os
import pytest

@pytest.mark.skipif(not os.getenv("RUN_INTEGRATION_TESTS"), reason="Requires PostgreSQL and RUN_INTEGRATION_TESTS=1")
def test_auth_endpoints():
    from app import app, initialize_database
    initialize_database()
    client = app.test_client()
    response = client.get("/api/auth/me")
    assert response.status_code == 200
    assert response.json["authenticated"] is False
