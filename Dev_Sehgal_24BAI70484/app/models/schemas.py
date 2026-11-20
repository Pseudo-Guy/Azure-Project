"""
Pydantic schemas and data models for AzureCloudHub.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

# -------------------------------------------------------------
# ML Inference Schemas
# -------------------------------------------------------------
class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=2, max_length=2000, json_schema_extra={"example": "Our Azure App Service responded quickly without any downtime!"})
    metadata: Optional[Dict[str, Any]] = None

class PredictionResponse(BaseModel):
    text: str
    sentiment: str
    sentiment_confidence: float
    category: str
    category_confidence: float
    latency_ms: float
    probabilities: Dict[str, float]
    timestamp: str

class BatchPredictionRequest(BaseModel):
    items: List[str] = Field(..., min_length=1, max_length=50)

class BatchPredictionResponse(BaseModel):
    results: List[PredictionResponse]
    total_processed: int
    avg_latency_ms: float

# -------------------------------------------------------------
# Cloud Economics & TCO Schemas
# -------------------------------------------------------------
class TCORequest(BaseModel):
    num_servers: int = Field(default=10, ge=1, le=500)
    cpu_cores_per_server: int = Field(default=8, ge=2, le=128)
    ram_gb_per_server: int = Field(default=32, ge=4, le=512)
    storage_tb: float = Field(default=10.0, ge=0.5, le=1000.0)
    years: int = Field(default=3, ge=1, le=5)
    purchase_model: str = Field(default="pay_as_you_go", description="pay_as_you_go | reserved_1yr | reserved_3yr | spot")
    use_azure_hybrid_benefit: bool = Field(default=True)

class TCUBreakdownItem(BaseModel):
    name: str
    cost_usd: float
    description: str

class TCOResponse(BaseModel):
    on_premises_total_usd: float
    azure_total_usd: float
    cost_savings_usd: float
    cost_savings_percentage: float
    capex_vs_opex_summary: str
    on_premises_breakdown: List[TCUBreakdownItem]
    azure_breakdown: List[TCUBreakdownItem]
    applied_discount_rate: float

# -------------------------------------------------------------
# Azure Composite SLA Schemas
# -------------------------------------------------------------
class SLAComponent(BaseModel):
    name: str
    sla_percentage: float = Field(..., ge=90.0, le=100.0)
    tier: str

class SLACalculatorRequest(BaseModel):
    architecture_name: str = "Cloud Microservice Tier"
    components: List[SLAComponent]
    deployment_mode: str = Field(default="single_instance", description="single_instance | availability_zones | multi_region_paired")

class SLACalculatorResponse(BaseModel):
    architecture_name: str
    composite_sla_percentage: float
    max_downtime_per_year_hours: float
    max_downtime_per_month_minutes: float
    max_downtime_per_week_minutes: float
    redundancy_level: str
    high_availability_tier: str
    recommendations: List[str]

# -------------------------------------------------------------
# Storage Redundancy & Lifecycle Schemas
# -------------------------------------------------------------
class StorageSimulatorRequest(BaseModel):
    data_size_gb: float = Field(default=1000.0, ge=1.0)
    redundancy_type: str = Field(default="LRS", description="LRS | ZRS | GRS | GZRS")
    tier: str = Field(default="Hot", description="Hot | Cool | Cold | Archive")
    monthly_read_gb: float = Field(default=200.0, ge=0.0)

class StorageSimulatorResponse(BaseModel):
    data_size_gb: float
    redundancy_type: str
    tier: str
    monthly_storage_cost_usd: float
    monthly_retrieval_cost_usd: float
    total_monthly_cost_usd: float
    durability: str
    replication_scope: str
    availability_sla: str
    rehydration_latency: str
    ideal_use_case: str

# -------------------------------------------------------------
# Governance & Policy Schemas
# -------------------------------------------------------------
class GovernanceCheckRequest(BaseModel):
    resource_name: str
    resource_type: str
    region: str
    tags: Dict[str, str]
    lock_type: str = Field(default="None", description="None | CanNotDelete | ReadOnly")

class PolicyRuleResult(BaseModel):
    rule_name: str
    passed: bool
    details: str

class GovernanceCheckResponse(BaseModel):
    resource_name: str
    is_compliant: bool
    compliance_score: int
    rule_results: List[PolicyRuleResult]
    violations: List[str]
    lock_status: str
    recommendations: List[str]

# -------------------------------------------------------------
# Quiz & Error Log Schemas
# -------------------------------------------------------------
class QuestionItem(BaseModel):
    id: str
    domain: str
    domain_weight: str
    subtopic: str
    question: str
    options: List[str]
    answer_index: int
    explanation: str
    reference: str

class QuizSubmissionRequest(BaseModel):
    answers: Dict[str, int]

class DomainScore(BaseModel):
    domain_name: str
    weight: str
    correct: int
    total: int
    percentage: float

class QuizSubmissionResponse(BaseModel):
    total_questions: int
    correct_count: int
    candidate_score: int
    passing_score: int = 700
    passed: bool
    domain_scores: List[DomainScore]
    candidate_score_benchmark: int = 971
    performance_analysis: str
    incorrect_questions: List[Dict[str, Any]]

# -------------------------------------------------------------
# Health & Status Schemas
# -------------------------------------------------------------
class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    environment: str
    azure_region: str
    uptime_seconds: float
    memory_usage_mb: float
    model_loaded: bool
