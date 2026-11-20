"""
FastAPI Routes for Azure Governance, Policy Validation, and Resource Locks.
"""

from fastapi import APIRouter
from app.models.schemas import GovernanceCheckRequest, GovernanceCheckResponse
from app.services.governance_service import governance_service, ALLOWED_REGIONS, MANDATORY_TAGS
from app.services.telemetry_service import telemetry_service
import time

router = APIRouter(prefix="/api/governance", tags=["Azure Governance & Policy"])

@router.post("/check", response_model=GovernanceCheckResponse)
def evaluate_resource_governance(req: GovernanceCheckRequest):
    t0 = time.perf_counter()
    res = governance_service.evaluate_compliance(req)
    lat = (time.perf_counter() - t0) * 1000.0
    telemetry_service.record_request("/api/governance/check", lat, 200)
    return res

@router.get("/rules")
def get_governance_rules():
    return {
        "allowed_regions": ALLOWED_REGIONS,
        "mandatory_tags": MANDATORY_TAGS,
        "supported_locks": ["None", "CanNotDelete", "ReadOnly"],
        "cloud_adoption_framework": "Microsoft Azure CAF Enterprise Landing Zone standard"
    }
