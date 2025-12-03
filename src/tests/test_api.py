from fastapi.testclient import TestClient
from app import app
import os

os.environ["API_KEYS"] = "test-key-12345,test-key-67890"

from auth import get_valid_api_keys
import auth
auth.VALID_API_KEYS = get_valid_api_keys()

client = TestClient(app)

class DummyLLM:
    def invoke(self, prompt):
        class Obj:
            content = "SELECT 1"
        return Obj()


def test_health():
    """Health endpoint should work without API key."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_query_without_api_key():
    """Query endpoint should reject requests without API key."""
    response = client.post("/query", json={"user_query": "hi"})
    assert response.status_code == 401
    assert "Missing API key" in response.json()["detail"]


def test_query_with_invalid_api_key():
    """Query endpoint should reject invalid API keys."""
    response = client.post(
        "/query",
        json={"user_query": "hi"},
        headers={"X-API-Key": "invalid-key"}
    )
    assert response.status_code == 403
    assert "Invalid API key" in response.json()["detail"]


def test_query_with_valid_api_key(monkeypatch):
    """Query endpoint should work with valid API key."""
    from app import llm_loader
    monkeypatch.setattr(llm_loader, "get_model", lambda: DummyLLM())

    response = client.post(
        "/query",
        json={"user_query": "hi"},
        headers={"X-API-Key": "test-key-12345"}
    )
    assert response.status_code == 200
    result = response.json()
    assert "sql" in result
    assert "result" in result
