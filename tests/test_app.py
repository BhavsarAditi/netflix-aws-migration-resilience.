import os
import pytest

# These smoke tests require a reachable PostgreSQL service and the same
# DB_* environment variables as the application.
@pytest.mark.skipif(not os.getenv("RUN_INTEGRATION_TESTS"), reason="Set RUN_INTEGRATION_TESTS=1 with PostgreSQL available")
def test_health_endpoint():
    from app import app
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["database"] == "connected"
