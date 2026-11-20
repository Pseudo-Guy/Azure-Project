"""
AZ-900 Exam Simulator and Error Log Revision Engine.
Faithfully mirrors the official syllabus, section weights, and candidate error-log methodology
detailed in Dev Sehgal's Industrial Internship Report.
"""

from typing import List, Dict, Any
from app.models.schemas import (
    QuestionItem, QuizSubmissionRequest, QuizSubmissionResponse, DomainScore
)

# Comprehensive AZ-900 Question Bank (Domain 1, Domain 2, Domain 3)
AZ900_QUESTIONS: List[QuestionItem] = [
    # ---------------- Domain 1: Describe Cloud Concepts (25-30%) ----------------
    QuestionItem(
        id="q1",
        domain="Describe cloud concepts",
        domain_weight="25–30%",
        subtopic="Cloud Models & Shared Responsibility",
        question="Under the Azure Shared Responsibility Model, which component is ALWAYS the exclusive responsibility of the customer across all cloud models (IaaS, PaaS, and SaaS)?",
        options=[
            "Operating system patching and updates",
            "Data, information, and identity governance",
            "Physical datacenter security and network cabling",
            "Virtual machine hypervisor configuration"
        ],
        answer_index=1,
        explanation="Data, information, endpoints, and identity accounts always remain 100% the customer's responsibility in on-premises, IaaS, PaaS, and SaaS models.",
        reference="NIST SP 800-145 / AZ-900 Study Guide Domain 1"
    ),
    QuestionItem(
        id="q2",
        domain="Describe cloud concepts",
        domain_weight="25–30%",
        subtopic="Cloud Economics",
        question="Which of the following describes an Operational Expenditure (OpEx) model?",
        options=[
            "Purchasing physical rack servers and amortizing them over 5 years",
            "Paying monthly for only the cloud compute and storage resources actually consumed",
            "Constructing a dedicated disaster recovery datacenter building",
            "Upfront capital procurement of high-speed Fibre Channel SAN switches"
        ],
        answer_index=1,
        explanation="OpEx is an ongoing operational expense with zero up-front capital hardware commitment, where organizations pay for services as they use them (consumption-based pricing).",
        reference="AZ-900 Week 1 Day 2 (CapEx vs OpEx)"
    ),
    QuestionItem(
        id="q3",
        domain="Describe cloud concepts",
        domain_weight="25–30%",
        subtopic="Scalability vs Elasticity",
        question="An online retailer configures an Azure App Service to automatically add three additional VM instances when CPU utilization exceeds 80%, and remove them when traffic subsides. Which cloud benefit does this illustrate?",
        options=[
            "Vertical scalability (scaling up)",
            "Predictability",
            "Elasticity (dynamic scaling out and in)",
            "Disaster Recovery"
        ],
        answer_index=2,
        explanation="Elasticity is the ability to automatically scale computing resources dynamically in real-time to match changing workload demands.",
        reference="AZ-900 Report Section 1.2.1 / Week 1 Day 1"
    ),
    QuestionItem(
        id="q4",
        domain="Describe cloud concepts",
        domain_weight="25–30%",
        subtopic="Cloud Service Models",
        question="A development team wants to deploy a containerized Python ML application without having to manage OS patching, hypervisors, or hardware, but wants full control over the runtime environment and scaling rules. Which service model is this?",
        options=[
            "Infrastructure as a Service (IaaS)",
            "Platform as a Service (PaaS)",
            "Software as a Service (SaaS)",
            "On-Premises Private Cloud"
        ],
        answer_index=1,
        explanation="Platform as a Service (PaaS) provides an environment for building, testing, and deploying software without the complexity of maintaining the underlying infrastructure and OS.",
        reference="AZ-900 Table 2.1 / Week 1 Day 3"
    ),
    QuestionItem(
        id="q5",
        domain="Describe cloud concepts",
        domain_weight="25–30%",
        subtopic="Cloud Deployment Models",
        question="An organization keeps its legacy sensitive database inside its private corporate datacenter while hosting its public-facing web API on Microsoft Azure. What deployment model is being used?",
        options=[
            "Public Cloud",
            "Private Cloud",
            "Hybrid Cloud",
            "Multi-tenant SaaS"
        ],
        answer_index=2,
        explanation="A hybrid cloud combines public and private cloud environments, allowing data and apps to be shared between them.",
        reference="AZ-900 Week 1 Day 4"
    ),

    # ---------------- Domain 2: Describe Azure Architecture and Services (35-40%) ----------------
    QuestionItem(
        id="q6",
        domain="Describe Azure architecture and services",
        domain_weight="35–40%",
        subtopic="Global Infrastructure",
        question="What is an Azure Availability Zone?",
        options=[
            "A logical group of subscriptions managed under a single root group",
            "One or more physically separate datacenters within a region, each with independent power, cooling, and networking",
            "A paired geographic region located at least 300 miles away",
            "A virtual network subnet reserved exclusively for firewall appliances"
        ],
        answer_index=1,
        explanation="Availability zones are physically separated datacenters within an Azure region, each equipped with independent power, cooling, and networking infrastructure to protect against single-datacenter outages.",
        reference="AZ-900 Figure 2.1 / Week 1 Day 5"
    ),
    QuestionItem(
        id="q7",
        domain="Describe Azure architecture and services",
        domain_weight="35–40%",
        subtopic="Resource Hierarchy",
        question="What is the correct hierarchical order of Azure resource management from top to bottom?",
        options=[
            "Subscriptions -> Management Groups -> Resource Groups -> Resources",
            "Management Groups -> Subscriptions -> Resource Groups -> Resources",
            "Resource Groups -> Management Groups -> Subscriptions -> Resources",
            "Subscriptions -> Resource Groups -> Management Groups -> Resources"
        ],
        answer_index=1,
        explanation="The Azure resource organisation hierarchy is: Management Groups (top) -> Subscriptions -> Resource Groups -> Resources (bottom).",
        reference="AZ-900 Figure 2.2 / Week 2 Day 1"
    ),
    QuestionItem(
        id="q8",
        domain="Describe Azure architecture and services",
        domain_weight="35–40%",
        subtopic="Compute Services",
        question="Which Azure compute service is serverless, executes lightweight code triggered by events, and bills strictly for the milliseconds of compute execution time?",
        options=[
            "Azure Virtual Machines",
            "Azure Kubernetes Service (AKS)",
            "Azure Functions",
            "Azure Virtual Desktop"
        ],
        answer_index=2,
        explanation="Azure Functions is an event-driven, serverless compute service where the customer only provides code and pays only when code runs.",
        reference="AZ-900 Table 2.1 / Week 2 Day 3"
    ),
    QuestionItem(
        id="q9",
        domain="Describe Azure architecture and services",
        domain_weight="35–40%",
        subtopic="Networking Services",
        question="What is the primary difference between Azure VPN Gateway and Azure ExpressRoute?",
        options=[
            "VPN Gateway connects to AWS, whereas ExpressRoute connects only to Azure",
            "VPN Gateway routes encrypted traffic across the public internet, whereas ExpressRoute provides a dedicated private connection that bypasses the public internet",
            "VPN Gateway supports up to 100 Gbps, whereas ExpressRoute is limited to 10 Mbps",
            "VPN Gateway requires an Azure Firewall, whereas ExpressRoute does not"
        ],
        answer_index=1,
        explanation="A VPN Gateway sends encrypted traffic between an on-premises network and Azure across the public internet. ExpressRoute creates a private, dedicated physical connection that does not traverse the public internet.",
        reference="AZ-900 Week 2 Day 5 / Error Log"
    ),
    QuestionItem(
        id="q10",
        domain="Describe Azure architecture and services",
        domain_weight="35–40%",
        subtopic="Storage Redundancy",
        question="Which Azure Storage redundancy option replicates data synchronously across three availability zones within the primary region, protecting against a datacenter outage?",
        options=[
            "Locally Redundant Storage (LRS)",
            "Zone-Redundant Storage (ZRS)",
            "Geo-Redundant Storage (GRS)",
            "Read-Access Geo-Redundant Storage (RA-GRS)"
        ],
        answer_index=1,
        explanation="Zone-Redundant Storage (ZRS) replicates data synchronously across three Azure availability zones in the primary region.",
        reference="AZ-900 Table 2.2 / Week 3 Day 2"
    ),
    QuestionItem(
        id="q11",
        domain="Describe Azure architecture and services",
        domain_weight="35–40%",
        subtopic="Storage Access Tiers",
        question="An enterprise needs to store compliance audit logs for 7 years. The logs are rarely accessed, but must be retained. Which Blob Storage tier provides the lowest monthly storage cost?",
        options=[
            "Hot Tier",
            "Cool Tier",
            "Cold Tier",
            "Archive Tier"
        ],
        answer_index=3,
        explanation="The Archive tier offers the lowest storage cost per GB, but has higher retrieval costs and requires several hours to rehydrate before data can be read.",
        reference="AZ-900 Week 3 Day 1"
    ),
    QuestionItem(
        id="q12",
        domain="Describe Azure architecture and services",
        domain_weight="35–40%",
        subtopic="Identity & Access",
        question="What is Microsoft Entra ID (formerly Azure Active Directory)?",
        options=[
            "A relational database service running on Linux VMs",
            "A cloud-based identity and access management service providing authentication, SSO, and MFA",
            "A hardware firewall that inspects incoming HTTP packets",
            "An antivirus scanner for managed disks"
        ],
        answer_index=1,
        explanation="Microsoft Entra ID is Microsoft's multi-tenant cloud-based identity and access management solution that manages users, credentials, SSO, MFA, and Conditional Access.",
        reference="AZ-900 Week 3 Day 4"
    ),
    QuestionItem(
        id="q13",
        domain="Describe Azure architecture and services",
        domain_weight="35–40%",
        subtopic="Security Principles",
        question="The security model based on the core principle 'never trust, always verify' is known as:",
        options=[
            "Defense in Depth",
            "Zero Trust",
            "Shared Responsibility",
            "Role-Based Access Control"
        ],
        answer_index=1,
        explanation="Zero Trust assumes breach and verifies each access request as though it originated from an uncontrolled network, enforcing explicit verification, least privilege, and assumed breach.",
        reference="AZ-900 Week 3 Day 5"
    ),

    # ---------------- Domain 3: Describe Azure Management and Governance (30-35%) ----------------
    QuestionItem(
        id="q14",
        domain="Describe Azure management and governance",
        domain_weight="30–35%",
        subtopic="Governance vs RBAC",
        question="What is the key difference between Azure Role-Based Access Control (RBAC) and Azure Policy?",
        options=[
            "RBAC enforces resource naming conventions; Azure Policy sets user passwords",
            "RBAC focuses on user actions (who has permission to perform what actions); Azure Policy focuses on resource properties (what configurations and rules resources must comply with)",
            "RBAC is only used for billing; Azure Policy is only used for networking",
            "RBAC cannot be assigned at subscription scope; Azure Policy can only be assigned to VMs"
        ],
        answer_index=1,
        explanation="RBAC determines WHAT actions an authorized user/identity can perform (User Authorization). Azure Policy evaluates resource properties and configurations to ensure corporate compliance (e.g. allowed regions, enforced tags).",
        reference="AZ-900 Week 4 Day 2 / Error Log"
    ),
    QuestionItem(
        id="q15",
        domain="Describe Azure management and governance",
        domain_weight="30–35%",
        subtopic="Resource Locks",
        question="An administrator applies a 'CanNotDelete' lock to an Azure Resource Group. What actions are permitted for an authorized user with Contributor role?",
        options=[
            "The user can only read resources, but cannot make any modifications",
            "The user can read and modify existing resources, but cannot delete the resources or the resource group",
            "The user can delete resources but cannot read them",
            "The lock completely revokes all access to the resource group"
        ],
        answer_index=1,
        explanation="A 'CanNotDelete' lock allows authorized users to read and modify resources, but prevents them from deleting them. A 'ReadOnly' lock prevents both modification and deletion.",
        reference="AZ-900 Week 4 Day 2 / Error Log"
    ),
    QuestionItem(
        id="q16",
        domain="Describe Azure management and governance",
        domain_weight="30–35%",
        subtopic="Cost Management & Savings",
        question="Which cost-saving feature allows an enterprise to apply existing on-premises Windows Server or SQL Server licenses with Software Assurance to Azure VMs to save up to 40-50%?",
        options=[
            "Azure Reservations",
            "Azure Hybrid Benefit",
            "Spot Virtual Machines",
            "Pricing Calculator"
        ],
        answer_index=1,
        explanation="Azure Hybrid Benefit allows organizations to use their eligible on-premises Windows Server and SQL Server licenses on Azure, significantly reducing compute costs.",
        reference="AZ-900 Week 4 Day 1"
    ),
    QuestionItem(
        id="q17",
        domain="Describe Azure management and governance",
        domain_weight="30–35%",
        subtopic="Infrastructure as Code",
        question="Which domain-specific language (DSL) developed by Microsoft uses declarative syntax to simplify writing and deploying Infrastructure as Code on Azure instead of complex JSON ARM templates?",
        options=[
            "Bicep",
            "Bash",
            "PowerShell",
            "Ansible Playbooks"
        ],
        answer_index=0,
        explanation="Bicep is a declarative domain-specific language (DSL) for deploying Azure resources that compiles into standard ARM template JSON with cleaner, concise syntax.",
        reference="AZ-900 Week 4 Day 3"
    ),
    QuestionItem(
        id="q18",
        domain="Describe Azure management and governance",
        domain_weight="30–35%",
        subtopic="Monitoring & Observability",
        question="Which Azure service provides personalized, actionable recommendations across five pillars: Reliability, Security, Performance, Cost, and Operational Excellence?",
        options=[
            "Azure Monitor",
            "Azure Advisor",
            "Azure Service Health",
            "Microsoft Purview"
        ],
        answer_index=1,
        explanation="Azure Advisor analyzes resource configuration and usage telemetry to provide proactive recommendations across Cost, Security, Reliability, Performance, and Operational Excellence.",
        reference="AZ-900 Week 4 Day 4"
    ),
    QuestionItem(
        id="q19",
        domain="Describe Azure management and governance",
        domain_weight="30–35%",
        subtopic="Hybrid Management",
        question="Which service enables you to project non-Azure resources—such as physical servers in your on-premises datacenter or Kubernetes clusters in AWS—into Azure Resource Manager for unified governance?",
        options=[
            "Azure ExpressRoute",
            "Azure Arc",
            "Azure Lighthouse",
            "Azure Migrate"
        ],
        answer_index=1,
        explanation="Azure Arc extends Azure ARM management and governance across on-premises, multi-cloud, and edge environments.",
        reference="AZ-900 Week 4 Day 3"
    ),
    QuestionItem(
        id="q20",
        domain="Describe Azure management and governance",
        domain_weight="30–35%",
        subtopic="Incident Notifications",
        question="Where should an Azure administrator go to check official Microsoft notifications about platform-wide service outages, planned maintenance, and health advisories affecting their specific subscriptions?",
        options=[
            "Azure Advisor",
            "Azure Service Health",
            "Cost Management + Billing",
            "Microsoft Entra ID"
        ],
        answer_index=1,
        explanation="Azure Service Health notifies you about Azure service incidents, planned maintenance events, and health advisories affecting your specific subscription and resources.",
        reference="AZ-900 Week 4 Day 4"
    )
]

# Curated Error Log entries based on Dev Sehgal's report revision insights
CURATED_ERROR_LOG: List[Dict[str, Any]] = [
    {
        "id": "err-1",
        "topic": "Governance vs Authorization",
        "distinction": "Azure Policy vs Azure RBAC",
        "error_trap": "Confusing 'who can do what' with 'what can be deployed'.",
        "one_line_rule": "RBAC controls USER ACTIONS (Who can execute API calls); Azure Policy controls RESOURCE PROPERTIES (Enforcing regions, tags, SKUs).",
        "reference": "Report Section 2.5 & Section 3.2"
    },
    {
        "id": "err-2",
        "topic": "Networking Architecture",
        "distinction": "VPN Gateway vs Azure ExpressRoute",
        "error_trap": "Assuming VPN Gateway is faster or private without understanding internet transit.",
        "one_line_rule": "VPN Gateway sends encrypted traffic over the public internet; ExpressRoute provides a dedicated, private, unshared physical link bypassing the internet.",
        "reference": "Report Section 2.3 & Section 2.5"
    },
    {
        "id": "err-3",
        "topic": "Cloud Economics",
        "distinction": "Scalability vs Elasticity",
        "error_trap": "Treating scalability and elasticity as interchangeable synonyms.",
        "one_line_rule": "Scalability is the CAPABILITY of a system to grow (vertically or horizontally); Elasticity is the AUTOMATION of scaling dynamically based on real-time load.",
        "reference": "Report Section 2.2 & Section 3.2"
    },
    {
        "id": "err-4",
        "topic": "Resource Safety",
        "distinction": "CanNotDelete Lock vs ReadOnly Lock",
        "error_trap": "Thinking ReadOnly lock still allows updates from subscription Owners.",
        "one_line_rule": "CanNotDelete prevents deletion but allows modification; ReadOnly prevents both deletion AND modification, even for Owners.",
        "reference": "Report Section 2.5"
    },
    {
        "id": "err-5",
        "topic": "Storage Durability",
        "distinction": "LRS vs ZRS vs GRS",
        "error_trap": "Thinking LRS protects against a datacenter flood or power outage.",
        "one_line_rule": "LRS replicates within 1 datacenter (11 nines); ZRS replicates across 3 Availability Zones in 1 region (12 nines); GRS replicates to a paired region 300+ miles away (16 nines).",
        "reference": "Report Table 2.2 & Section 2.4"
    },
    {
        "id": "err-6",
        "topic": "Observability",
        "distinction": "Azure Monitor vs Azure Advisor vs Service Health",
        "error_trap": "Using Azure Monitor to check global Microsoft datacenter outages.",
        "one_line_rule": "Azure Monitor tracks telemetry and metrics of YOUR resources; Azure Advisor gives optimization advice; Azure Service Health reports MICROSOFT'S platform status.",
        "reference": "Report Section 2.5"
    }
]

class QuizService:
    @staticmethod
    def get_all_questions() -> List[QuestionItem]:
        return AZ900_QUESTIONS

    @staticmethod
    def get_error_log() -> List[Dict[str, Any]]:
        return CURATED_ERROR_LOG

    @staticmethod
    def submit_quiz(submission: QuizSubmissionRequest) -> QuizSubmissionResponse:
        total = len(AZ900_QUESTIONS)
        correct_count = 0
        incorrect_questions = []

        domain_stats = {
            "Describe cloud concepts": {"weight": "25–30%", "correct": 0, "total": 0},
            "Describe Azure architecture and services": {"weight": "35–40%", "correct": 0, "total": 0},
            "Describe Azure management and governance": {"weight": "30–35%", "correct": 0, "total": 0}
        }

        for q in AZ900_QUESTIONS:
            domain = q.domain
            if domain in domain_stats:
                domain_stats[domain]["total"] += 1

            user_ans = submission.answers.get(q.id)
            if user_ans == q.answer_index:
                correct_count += 1
                if domain in domain_stats:
                    domain_stats[domain]["correct"] += 1
            else:
                incorrect_questions.append({
                    "id": q.id,
                    "subtopic": q.subtopic,
                    "question": q.question,
                    "user_answer": q.options[user_ans] if (user_ans is not None and 0 <= user_ans < len(q.options)) else "Not Answered",
                    "correct_answer": q.options[q.answer_index],
                    "explanation": q.explanation,
                    "reference": q.reference
                })

        # Calculate scaled score out of 1000 (Pass threshold 700)
        percentage = (correct_count / total) if total > 0 else 0
        scaled_score = int(round(percentage * 1000))
        passed = scaled_score >= 700

        domain_scores = []
        for dname, stats in domain_stats.items():
            tot = stats["total"]
            cor = stats["correct"]
            pct = round((cor / tot * 100.0), 1) if tot > 0 else 0.0
            domain_scores.append(DomainScore(
                domain_name=dname,
                weight=stats["weight"],
                correct=cor,
                total=tot,
                percentage=pct
            ))

        if scaled_score >= 971:
            perf_text = f"Outstanding! You matched or exceeded Dev Sehgal's top score of 971/1000! You possess mastery across all 3 domains."
        elif scaled_score >= 850:
            perf_text = f"Excellent performance ({scaled_score}/1000). You are well above the 700 passing bar and close to Dev Sehgal's 971 benchmark."
        elif passed:
            perf_text = f"Congratulations! You passed with {scaled_score}/1000 (Passing: 700). Focus on the Error Log to boost to 950+."
        else:
            perf_text = f"Score: {scaled_score}/1000. Review the detailed Error Log explanations below and re-test."

        return QuizSubmissionResponse(
            total_questions=total,
            correct_count=correct_count,
            candidate_score=scaled_score,
            passing_score=700,
            passed=passed,
            domain_scores=domain_scores,
            candidate_score_benchmark=971,
            performance_analysis=perf_text,
            incorrect_questions=incorrect_questions
        )

quiz_service = QuizService()
