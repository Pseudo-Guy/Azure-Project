"""
Unit tests for Azure Governance and Policy evaluation.
"""

from app.models.schemas import GovernanceCheckRequest
from app.services.governance_service import governance_service

def test_governance_compliant_resource():
    req = GovernanceCheckRequest(
        resource_name="app-cloudhub-prod-01",
        resource_type="appservice",
        region="centralindia",
        tags={
            "Environment": "Production",
            "Owner": "Dev Sehgal",
            "Project": "AZ-900 AIML",
            "CostCenter": "CC-70484"
        },
        lock_type="CanNotDelete"
    )
    res = governance_service.evaluate_compliance(req)
    assert res.is_compliant is True
    assert res.compliance_score == 100
    assert len(res.violations) == 0

def test_governance_non_compliant_region_and_tags():
    req = GovernanceCheckRequest(
        resource_name="INVALID_NAME",
        resource_type="appservice",
        region="brazilsouth", # Not in allowed locations
        tags={},              # Missing mandatory tags
        lock_type="None"      # Missing lock
    )
    res = governance_service.evaluate_compliance(req)
    assert res.is_compliant is False
    assert res.compliance_score < 100
    assert len(res.violations) >= 2
