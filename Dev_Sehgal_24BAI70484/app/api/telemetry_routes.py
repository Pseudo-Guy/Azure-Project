"""
FastAPI Routes for Azure Monitor & Application Insights Telemetry.
"""

from fastapi import APIRouter
from app.services.telemetry_service import telemetry_service

router = APIRouter(prefix="/api/telemetry", tags=["Observability & Telemetry"])

@router.get("/metrics")
def get_telemetry_metrics():
    return telemetry_service.get_metrics()

@router.post("/reset-budget-alert")
def reset_budget():
    telemetry_service.current_spend_usd = 42.50
    telemetry_service.record_log("INFO", "Azure Cost Management budget simulation reset to $42.50 baseline.")
    return {"status": "Budget reset to normal ($42.50 / $150.00)"}

@router.post("/simulate-spend-spike")
def trigger_spend_spike():
    telemetry_service.current_spend_usd = 135.00
    telemetry_service.record_log("WARN", "Azure Cost Management ALERT triggered: Current spend ($135.00) exceeded 80% threshold ($120.00).")
    return {"status": "Spend spike simulated: 90% budget utilized. Alert triggered!"}
