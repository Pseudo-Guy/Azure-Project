"""
FastAPI Routes for Cloud Economics, Composite SLA, and Storage Simulation.
"""

from fastapi import APIRouter
from app.models.schemas import (
    TCORequest, TCOResponse,
    SLACalculatorRequest, SLACalculatorResponse,
    StorageSimulatorRequest, StorageSimulatorResponse
)
from app.services.cloud_calculator import cloud_calculator
from app.services.telemetry_service import telemetry_service
import time

router = APIRouter(prefix="/api/calculator", tags=["Cloud Calculators"])

@router.post("/tco", response_model=TCOResponse)
def calculate_tco(req: TCORequest):
    t0 = time.perf_counter()
    res = cloud_calculator.calculate_tco(req)
    lat = (time.perf_counter() - t0) * 1000.0
    telemetry_service.record_request("/api/calculator/tco", lat, 200)
    return res

@router.post("/sla", response_model=SLACalculatorResponse)
def calculate_sla(req: SLACalculatorRequest):
    t0 = time.perf_counter()
    res = cloud_calculator.calculate_sla(req)
    lat = (time.perf_counter() - t0) * 1000.0
    telemetry_service.record_request("/api/calculator/sla", lat, 200)
    return res

@router.post("/storage", response_model=StorageSimulatorResponse)
def simulate_storage(req: StorageSimulatorRequest):
    t0 = time.perf_counter()
    res = cloud_calculator.simulate_storage(req)
    lat = (time.perf_counter() - t0) * 1000.0
    telemetry_service.record_request("/api/calculator/storage", lat, 200)
    return res
