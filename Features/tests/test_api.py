import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_analyze_python():
    response = client.post("/api/analyze/python", json={"code": "for i in range(10):\n    print(i)"})
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "python"
    assert "features" in data
    assert data["features"]["loop_count"] == 1

def test_analyze_java():
    response = client.post("/api/analyze/java", json={"code": "for(int i=0; i<10; i++) { System.out.println(i); }"})
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "java"
    assert "features" in data
    assert data["features"]["loop_count"] == 1

def test_empty_code():
    response = client.post("/api/analyze/python", json={"code": "   "})
    assert response.status_code == 400
