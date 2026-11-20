"""
Azure Policy, Governance, Resource Locks, and RBAC Validation Service.
Implements the compliance rules and distinctions detailed in Week 4 of Arighna's report.
"""

import re
from typing import List, Dict
from app.models.schemas import GovernanceCheckRequest, GovernanceCheckResponse, PolicyRuleResult

ALLOWED_REGIONS = [
    "centralindia",
    "southindia",
    "eastus",
    "eastus2",
    "westeurope",
    "northeurope",
    "southeastasia"
]

MANDATORY_TAGS = ["Environment", "Owner", "Project", "CostCenter"]

class GovernanceService:

    @staticmethod
    def evaluate_compliance(req: GovernanceCheckRequest) -> GovernanceCheckResponse:
        violations: List[str] = []
        rule_results: List[PolicyRuleResult] = []
        score = 100

        # Rule 1: Allowed Locations Policy
        region_clean = req.region.lower().replace(" ", "")
        if region_clean in ALLOWED_REGIONS:
            rule_results.append(PolicyRuleResult(
                rule_name="Allowed Locations Policy",
                passed=True,
                details=f"Region '{req.region}' is compliant with enterprise sovereign boundary rules."
            ))
        else:
            violations.append(f"Region '{req.region}' violates Allowed Locations Policy. Must be deployed to approved regions: {', '.join(ALLOWED_REGIONS)}.")
            rule_results.append(PolicyRuleResult(
                rule_name="Allowed Locations Policy",
                passed=False,
                details=f"Region '{req.region}' is outside compliant cloud geographies."
            ))
            score -= 30

        # Rule 2: Mandatory Tags Policy
        missing_tags = [t for t in MANDATORY_TAGS if t not in req.tags or not str(req.tags[t]).strip()]
        if not missing_tags:
            rule_results.append(PolicyRuleResult(
                rule_name="Mandatory Tagging Policy",
                passed=True,
                details=f"All required enterprise tags ({', '.join(MANDATORY_TAGS)}) are present for cost tracking and governance."
            ))
        else:
            violations.append(f"Missing mandatory governance tags: {', '.join(missing_tags)}. Cost management and chargeback require complete tagging.")
            rule_results.append(PolicyRuleResult(
                rule_name="Mandatory Tagging Policy",
                passed=False,
                details=f"Missing tags: {', '.join(missing_tags)}"
            ))
            score -= (10 * len(missing_tags))

        # Rule 3: Naming Convention Standard
        name_patterns = {
            "resourcegroup": r"^rg-[a-z0-9\-]+$",
            "appservice": r"^app-[a-z0-9\-]+$",
            "storageaccount": r"^st[a-z0-9]{3,21}$",
            "virtualnetwork": r"^vnet-[a-z0-9\-]+$",
            "keyvault": r"^kv-[a-z0-9\-]+$"
        }
        res_type_clean = req.resource_type.lower().replace(" ", "").replace("_", "")
        pattern = name_patterns.get(res_type_clean, r"^[a-z0-9\-]+$")

        if re.match(pattern, req.resource_name.lower()):
            rule_results.append(PolicyRuleResult(
                rule_name="Resource Naming Convention Standard",
                passed=True,
                details=f"Resource name '{req.resource_name}' complies with cloud naming standard pattern '{pattern}'."
            ))
        else:
            violations.append(f"Resource name '{req.resource_name}' does not follow Azure CAF naming conventions for type '{req.resource_type}' (expected pattern: {pattern}).")
            rule_results.append(PolicyRuleResult(
                rule_name="Resource Naming Convention Standard",
                passed=False,
                details=f"Name does not conform to pattern '{pattern}'"
            ))
            score -= 15

        # Lock evaluation
        lock = req.lock_type
        if lock == "ReadOnly":
            lock_status = "Protected with ReadOnly lock. Authorized users can read resources, but cannot delete or modify them."
        elif lock == "CanNotDelete":
            lock_status = "Protected with CanNotDelete lock. Authorized users can read and modify resources, but cannot delete them."
        else:
            lock_status = "No Resource Lock applied. Resource is vulnerable to accidental deletion."
            violations.append("Recommended: Apply 'CanNotDelete' lock to production resources to prevent accidental catastrophic deletion.")
            score -= 10

        recommendations = []
        if violations:
            recommendations.append("Remediate non-compliant settings before initiating ARM/Bicep template provisioning.")
            recommendations.append("Configure Azure Policy Remediation Tasks to automatically append missing tags on deployment.")
        else:
            recommendations.append("Resource meets 100% of enterprise Azure Governance standards and CAF best practices.")
            recommendations.append("Proceed with automated Infrastructure as Code deployment.")

        score = max(0, score)
        is_compliant = len([v for v in violations if "Recommended:" not in v]) == 0

        return GovernanceCheckResponse(
            resource_name=req.resource_name,
            is_compliant=is_compliant,
            compliance_score=score,
            rule_results=rule_results,
            violations=violations,
            lock_status=lock_status,
            recommendations=recommendations
        )

governance_service = GovernanceService()
