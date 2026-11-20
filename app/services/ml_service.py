"""
ML Inference Service for AzureCloudHub.
Simulates an AI model-serving microservice deployed on Azure App Service / ACI.
"""

import os
import time
from datetime import datetime, timezone
import joblib
from app.models.schemas import PredictionRequest, PredictionResponse, BatchPredictionRequest, BatchPredictionResponse

ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ml", "model_artifacts")
VECTORIZER_PATH = os.path.join(ARTIFACTS_DIR, "vectorizer.joblib")
SENTIMENT_PATH = os.path.join(ARTIFACTS_DIR, "sentiment_clf.joblib")
CATEGORY_PATH = os.path.join(ARTIFACTS_DIR, "category_clf.joblib")

class MLService:
    def __init__(self):
        self.vectorizer = None
        self.sentiment_model = None
        self.category_model = None
        self.load_artifacts()

    def load_artifacts(self):
        try:
            if os.path.exists(VECTORIZER_PATH) and os.path.exists(SENTIMENT_PATH) and os.path.exists(CATEGORY_PATH):
                self.vectorizer = joblib.load(VECTORIZER_PATH)
                self.sentiment_model = joblib.load(SENTIMENT_PATH)
                self.category_model = joblib.load(CATEGORY_PATH)
                print("[OK] ML Service: Artifacts loaded successfully.")
            else:
                print("[WARN] ML Service: Artifacts not found. Will trigger fallback or re-train.")
        except Exception as e:
            print(f"[ERR] Failed to load model artifacts: {e}")

    @property
    def is_ready(self) -> bool:
        return self.vectorizer is not None and self.sentiment_model is not None and self.category_model is not None

    def predict(self, req: PredictionRequest) -> PredictionResponse:
        start_time = time.perf_counter()
        
        if not self.is_ready:
            # Fallback heuristic if models are not loaded
            text_lower = req.text.lower()
            if any(w in text_lower for w in ["great", "smooth", "flawlessly", "amazing", "reliable", "satisfied", "good"]):
                sentiment = "Positive"
                sentiment_conf = 0.92
            elif any(w in text_lower for w in ["failed", "error", "spike", "crash", "denied", "broken", "issue"]):
                sentiment = "Negative"
                sentiment_conf = 0.88
            else:
                sentiment = "Neutral"
                sentiment_conf = 0.80
            
            category = "General"
            category_conf = 0.75
            probabilities = {"Positive": 0.33, "Neutral": 0.33, "Negative": 0.34}
        else:
            X = self.vectorizer.transform([req.text])
            
            # Sentiment prediction
            sentiment_pred = self.sentiment_model.predict(X)[0]
            sentiment_probs = self.sentiment_model.predict_proba(X)[0]
            sentiment_classes = self.sentiment_model.classes_
            
            sentiment_conf = float(max(sentiment_probs))
            probabilities = {cls: round(float(prob), 4) for cls, prob in zip(sentiment_classes, sentiment_probs)}
            sentiment = sentiment_pred
            
            # Category prediction
            category_pred = self.category_model.predict(X)[0]
            category_probs = self.category_model.predict_proba(X)[0]
            category_conf = float(max(category_probs))
            category = category_pred

        latency = (time.perf_counter() - start_time) * 1000.0

        return PredictionResponse(
            text=req.text,
            sentiment=sentiment,
            sentiment_confidence=round(sentiment_conf, 4),
            category=category,
            category_confidence=round(category_conf, 4),
            latency_ms=round(latency, 2),
            probabilities=probabilities,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

    def batch_predict(self, req: BatchPredictionRequest) -> BatchPredictionResponse:
        results = []
        start_batch = time.perf_counter()
        for text in req.items:
            res = self.predict(PredictionRequest(text=text))
            results.append(res)
        total_time = (time.perf_counter() - start_batch) * 1000.0
        avg_latency = total_time / len(req.items) if req.items else 0.0

        return BatchPredictionResponse(
            results=results,
            total_processed=len(results),
            avg_latency_ms=round(avg_latency, 2)
        )

ml_service = MLService()
