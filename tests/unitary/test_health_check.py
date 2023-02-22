from fastapi.testclient import TestClient

from project.main import app

client = TestClient(app)


def test_health_check():
    response = client.head("/health")
    assert response.status_code == 200
