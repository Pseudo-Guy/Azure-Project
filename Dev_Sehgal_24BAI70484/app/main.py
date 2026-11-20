"""
AzureCloudHub - AI Model-Serving Microservice & AZ-900 Cloud Mastery Suite
Main FastAPI application entry point.
"""

import os
import time
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import HealthResponse
from app.services.ml_service import ml_service
from app.api.ml_routes import router as ml_router
from app.api.calculator_routes import router as calculator_router
from app.api.governance_routes import router as governance_router
from app.api.telemetry_routes import router as telemetry_router
from app.api.quiz_routes import router as quiz_router

app = FastAPI(
    title="AzureCloudHub: AI Model-Serving & AZ-900 Cloud Suite",
    description="Enterprise-grade cloud microservice and interactive AZ-900 cloud workbench built on Dev Sehgal's Industrial Internship Report.",
    version="1.0.0"
)

# Enable CORS for local and cloud environments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

APP_START_TIME = time.time()

# Include API Routers
app.include_router(ml_router)
app.include_router(calculator_router)
app.include_router(governance_router)
app.include_router(telemetry_router)
app.include_router(quiz_router)

# Mount Static directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "AzureCloudHub API is running. Access /docs for interactive Swagger API documentation."}

@app.get("/health", response_model=HealthResponse, tags=["System Health"])
def health_check():
    uptime = time.time() - APP_START_TIME
    # Memory estimation
    try:
        import resource
        mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    except Exception:
        mem = 48.2  # default fallback in MB

    return HealthResponse(
        status="Healthy",
        app_name="AzureCloudHub-AIML-Workload",
        version="1.0.0",
        environment=os.getenv("AZURE_ENVIRONMENT", "Production (Azure App Service)"),
        azure_region=os.getenv("AZURE_REGION", "Central India"),
        uptime_seconds=round(uptime, 1),
        memory_usage_mb=round(mem, 1),
        model_loaded=ml_service.is_ready
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
