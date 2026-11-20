"""
Unit tests for AI/ML Inference Service.
"""

from app.models.schemas import PredictionRequest, BatchPredictionRequest
from app.services.ml_service import ml_service

def test_ml_service_is_ready():
    assert ml_service.is_ready is True

def test_single_prediction_positive():
    req = PredictionRequest(text="Azure App Service deployment was remarkably smooth, fast and stable.")
    res = ml_service.predict(req)
    assert res.sentiment in ["Positive", "Neutral", "Negative"]
    assert 0.0 <= res.sentiment_confidence <= 1.0
    assert res.latency_ms >= 0.0
    assert "Positive" in res.probabilities

def test_batch_prediction():
    req = BatchPredictionRequest(items=[
        "Great performance on Azure Kubernetes Service",
        "How do I configure zone-redundant storage accounts?",
        "Critical VM failure in East US datacenter"
    ])
    res = ml_service.batch_predict(req)
    assert res.total_processed == 3
    assert len(res.results) == 3
    assert res.avg_latency_ms >= 0.0
