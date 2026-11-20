"""
Integration tests for FastAPI endpoints.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Healthy"
    assert data["model_loaded"] is True

def test_api_predict():
    response = client.post("/api/ml/predict", json={
        "text": "Azure App Service delivers amazing scalability and reliability for our team."
    })
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert "latency_ms" in data

def test_api_tco_calculator():
    response = client.post("/api/calculator/tco", json={
        "num_servers": 5,
        "cpu_cores_per_server": 8,
        "ram_gb_per_server": 32,
        "storage_tb": 5.0,
        "years": 3,
        "purchase_model": "reserved_3yr",
        "use_azure_hybrid_benefit": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["cost_savings_usd"] > 0

def test_api_governance_check():
    response = client.post("/api/governance/check", json={
        "resource_name": "app-test-prod",
        "resource_type": "appservice",
        "region": "centralindia",
        "tags": {
            "Environment": "Production",
            "Owner": "Dev Sehgal",
            "Project": "AZ-900 AIML",
            "CostCenter": "CC-70484"
        },
        "lock_type": "CanNotDelete"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["is_compliant"] is True

def test_api_quiz_and_report_summary():
    res_q = client.get("/api/quiz/questions")
    assert res_q.status_code == 200
    assert res_q.json()["total"] >= 20

    res_rep = client.get("/api/quiz/report-summary")
    assert res_rep.status_code == 200
    data = res_rep.json()
    assert data["candidate"] == "Dev Sehgal"
    assert data["exam_result"]["score"] == 971
