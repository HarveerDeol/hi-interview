from fastapi.testclient import TestClient


def test_ping(test_client: TestClient) -> None:
    response = test_client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"healthy": "true"}
