from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

class DummyLLM:
    def invoke(self, prompt):
        class Obj:
            content = "SELECT 1"
        return Obj()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_query_endpoint(monkeypatch):
    # patch LLM loader
    from app import llm_loader
    monkeypatch.setattr(llm_loader, "get_model", lambda: DummyLLM())

    response = client.post("/query", json={"user_query": "hi"})
    assert response.status_code == 200

    result = response.json()
    assert "sql" in result
    assert "result" in result
