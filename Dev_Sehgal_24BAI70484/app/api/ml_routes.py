"""
FastAPI Routes for AI/ML Inference Workload.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import PredictionRequest, PredictionResponse, BatchPredictionRequest, BatchPredictionResponse
from app.services.ml_service import ml_service
from app.services.telemetry_service import telemetry_service

router = APIRouter(prefix="/api/ml", tags=["Machine Learning Inference"])

@router.post("/predict", response_model=PredictionResponse)
def predict_single(req: PredictionRequest):
    try:
        response = ml_service.predict(req)
        telemetry_service.record_request("/api/ml/predict", response.latency_ms, 200)
        return response
    except Exception as e:
        telemetry_service.record_request("/api/ml/predict", 0.0, 500)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch-predict", response_model=BatchPredictionResponse)
def predict_batch(req: BatchPredictionRequest):
    try:
        response = ml_service.batch_predict(req)
        telemetry_service.record_request("/api/ml/batch-predict", response.avg_latency_ms, 200)
        return response
    except Exception as e:
        telemetry_service.record_request("/api/ml/batch-predict", 0.0, 500)
        raise HTTPException(status_code=500, detail=str(e))
