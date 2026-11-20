# AzureCloudHub: AI Model-Serving Architecture & AZ-900 Cloud Mastery Suite

[![Azure Certification](https://img.shields.io/badge/Microsoft%20Certified-AZ--900%20(942%2F1000)-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/credentials/certifications/resources/study-guides/az-900)
[![Python Version](https://img.shields.io/badge/Python-3.12%20%7C%203.14-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production%20Ready-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade, portfolio-ready cloud engineering project designed and developed from the **Industrial Internship Report** of **Arighna Sadhu** (UID: `24BAI70500`, B.E. Computer Science and Engineering - Artificial Intelligence and Machine Learning, Chandigarh University).

The project brings to life the explicit capstone recommendation documented in **Chapter 3, Section 3.3** of the report:
> *"Build at least one end-to-end mini project, for example a containerised model-serving API on App Service or AKS with monitoring and cost alerts, to turn knowledge of individual services into design experience... and maintain an error log and full-length practice engine."*

---

## 📑 Candidate Profile & Examination Credentials

- **Candidate Name:** Arighna Sadhu
- **University Identifier (UID):** `24BAI70500`
- **Degree:** Bachelor of Engineering in Computer Science & Engineering (Artificial Intelligence and Machine Learning)
- **Institution:** Chandigarh University, Gharuan, Mohali, Punjab
- **Examination Reference:** Certiport Exam Reference `53209596` | Registration `ITS-51811871`
- **AZ-900 Examination Result:** **Passed (942 / 1000)** *(Passing Bar: 700)*
  - **Describe cloud concepts (25–30%):** 90%
  - **Describe Azure architecture and services (35–40%):** 96%
  - **Describe Azure management and governance (30–35%):** 96%

---

## 🏛️ System Architecture

```text
                               +-------------------------------------------------------------+
                               |                    Microsoft Azure (Cloud)                  |
                               |                                                             |
                               |   +-----------------------------------------------------+   |
                               |   |  Resource Group: rg-azurecloudhub-prod (Central IN) |   |
                               |   |  [Lock: CanNotDelete] [Tags: CAF Compliant]         |   |
                               |   |                                                     |   |
                               |   |   +---------------------------------------------+   |   |
  +------------------+         |   |   | Azure App Service Plan (Linux - B1/P1v3)    |   |   |
  |  End User / Web  |  HTTPS  |   |   |                                             |   |   |
  |     Browser      +-------->+------>+   +-------------------------------------+   |   |   |
  +------------------+   :443  |   |   |   | Azure Web App for Containers (PaaS) |   |   |   |
                               |   |   |   | - FastAPI ML Model-Serving Engine   |   |   |   |
                               |   |   |   | - Cloud Economics & TCO Simulators  |   |   |   |
                               |   |   |   | - AZ-900 Exam Engine & Error Log    |   |   |   |
                               |   |   |   +------------------+------------------+   |   |   |
                               |   |   +----------------------|----------------------+   |   |
                               |   |                          | Telemetry Sink           |   |
                               |   |                          v                          |   |
                               |   |   +---------------------------------------------+   |   |
                               |   |   | Observability & Governance Layer            |   |   |
                               |   |   | - Azure Monitor & Application Insights      |   |   |
                               |   |   | - Log Analytics Workspace                   |   |   |
                               |   |   | - Cost Management Budget Alerts (80% / 100%)|   |   |
                               |   |   +---------------------------------------------+   |   |
                               |   |                          ^                          |   |
                               |   |                          | Artifacts                |   |
                               |   |   +----------------------+----------------------+   |   |
                               |   |   | Azure Storage Account (Standard_ZRS)        |   |   |
                               |   |   | - Container: model-artifacts                |   |   |
                               |   |   | - Hot Tier -> Cool (30d) -> Archive (90d)   |   |   |
                               |   |   +---------------------------------------------+   |   |
                               |   +-----------------------------------------------------+   |
                               +-------------------------------------------------------------+
```

---

## 🚀 Key Modules & Capabilities

### 1. 🤖 AI Model-Serving Microservice (`app/services/ml_service.py`)
- Real-time text inference endpoint serving customer feedback and cloud ticket classification.
- Dual-head Scikit-Learn TF-IDF classifier predicting **Sentiment** (`Positive`, `Neutral`, `Negative`) and **Incident Category** (`Reliability`, `Performance`, `Cost`, `Storage`, `Networking`, `Security`, `Governance`).
- Measures sub-20ms inference latency and outputs probability confidence distributions.
- Supports single-request (`/api/ml/predict`) and batch processing (`/api/ml/batch-predict`).

### 2. 🏛️ Azure Architecture & Services Explorer
- **Interactive Shared Responsibility Visualizer:** Toggle between **On-Premises**, **IaaS**, **PaaS**, and **SaaS** to inspect the shifting division of responsibility for data, identities, OS patching, hypervisors, and physical datacenters (*Figure 1.1 in report*).
- **Storage Redundancy & Lifecycle Simulator:** Calculate costs and durability guarantees across **LRS** (11 nines), **ZRS** (12 nines), **GRS** (16 nines), and **GZRS** (16 nines), and simulate access tiers (**Hot**, **Cool**, **Cold**, **Archive** with 1-15 hour rehydration latency) (*Table 2.2 in report*).

### 3. 💰 Cloud Economics & TCO Engine (`app/services/cloud_calculator.py`)
- **CapEx vs OpEx Projection:** Dynamic slider-based model computing total on-premises datacenter costs (rack servers, SAN storage, HVAC cooling, hypervisor licenses, IT labor) vs Azure consumption-based billing.
- **Pricing Optimization Tiers:** Simulates **Pay-As-You-Go**, **1-Year Reserved Instances (38% off)**, **3-Year Reserved Instances (62% off)**, **Spot VMs (85% off)**, and **Azure Hybrid Benefit (up to 40% software assurance discount)** (*Week 1 Day 2 & Week 4 Day 1 in report*).

### 4. 🛡️ Azure Governance & Composite SLA Calculator (`app/services/governance_service.py`)
- **Azure Policy Evaluation Engine:** Validates target deployment regions against approved geographic boundaries (`centralindia`, `eastus`, `westeurope`), enforces mandatory Cloud Adoption Framework (CAF) tags (`Environment`, `Owner`, `Project`, `CostCenter`), and verifies resource naming patterns.
- **Resource Lock Verification:** Assesses `CanNotDelete` and `ReadOnly` locks protecting critical cloud assets.
- **Composite SLA Multiplier:** Computes end-to-end multi-tier availability ($SLA_{total} = \prod SLA_i$) and demonstrates how deploying across **3 Availability Zones** elevates uptime from 99.9% to 99.99%.

### 5. 📝 AZ-900 Exam Simulator & Error Log Revision (`app/services/quiz_service.py`)
- **20-Question Full Mock Examination:** Comprehensive question bank strictly mapped to the official syllabus:
  - Domain 1: Describe cloud concepts (25–30%)
  - Domain 2: Describe Azure architecture and services (35–40%)
  - Domain 3: Describe Azure management and governance (30–35%)
- **Certiport Scoring Algorithm:** Converts raw answers into a 1000-point score, compares performance directly against **Arighna's 942 benchmark**, and isolates weak domains.
- **Curated Error Log:** Interactive revision entries reviewing the exact conceptual traps highlighted in Chapter 2.5 of the internship report:
  - *RBAC vs Azure Policy* (Who can act vs What can be deployed)
  - *VPN Gateway vs ExpressRoute* (Internet transit vs Dedicated private circuit)
  - *Scalability vs Elasticity* (Capability vs Automation)
  - *CanNotDelete vs ReadOnly Locks* (Modification allowed vs Read-only)
  - *LRS vs ZRS vs GRS* (Single datacenter vs 3 zones vs paired region)
  - *Azure Monitor vs Azure Advisor vs Service Health* (Resource telemetry vs Best-practice tips vs Microsoft platform status)

### 6. 📊 Observability Sink & Telemetry Stream (`app/services/telemetry_service.py`)
- Live Application Insights metric simulator tracking request volume, p95/p99 latency, and structured log traces.
- Interactive **Cost Management Budget Spike simulation** that triggers an automated 80% threshold alert ($120 on a $150 budget).

---

## 📁 Repository Structure

```text
C:\Study\AZ-900 Project\
├── README.md                      # Complete system documentation
├── requirements.txt               # Production Python dependencies
├── pytest.ini                     # Pytest configuration
├── Dockerfile                     # Multi-stage production container build
├── docker-compose.yml             # Local container orchestration
├── .gitignore                     # Git ignore rules
├── .dockerignore                  # Container build context filter
│
├── app/
│   ├── main.py                    # FastAPI application & lifespan setup
│   ├── models/
│   │   └── schemas.py             # Pydantic v2 data models & request/response schemas
│   ├── services/
│   │   ├── ml_service.py          # Dual-head ML classifier & batch inference engine
│   │   ├── cloud_calculator.py    # TCO, Composite SLA & Storage simulator
│   │   ├── governance_service.py  # Azure Policy & Resource Lock validator
│   │   ├── telemetry_service.py   # Application Insights & Azure Monitor simulator
│   │   └── quiz_service.py        # AZ-900 mock engine & candidate error log
│   ├── api/
│   │   ├── ml_routes.py           # REST endpoints for model inference
│   │   ├── calculator_routes.py   # REST endpoints for TCO and SLA calculations
│   │   ├── governance_routes.py   # REST endpoints for Policy checks
│   │   ├── telemetry_routes.py    # REST endpoints for metrics and budget alerts
│   │   └── quiz_routes.py         # REST endpoints for exam prep & report metadata
│   └── static/
│       ├── index.html             # Responsive Azure-themed Single Page Application
│       ├── css/style.css          # Glassmorphism dark mode styles
│       └── js/app.js              # Interactive client-side controller
│
├── ml/
│   ├── train_model.py             # Training pipeline for sentiment & category model
│   └── model_artifacts/
│       ├── vectorizer.joblib      # Fitted TF-IDF n-gram vectorizer
│       ├── sentiment_clf.joblib   # Serialized sentiment classification model
│       └── category_clf.joblib    # Serialized ticket category routing model
│
├── infra/
│   ├── bicep/
│   │   ├── main.bicep             # Azure Bicep Infrastructure as Code template
│   │   └── parameters.bicepparam  # Bicep environment parameters
│   ├── arm/
│   │   └── azuredeploy.json       # Exported ARM template equivalent
│   ├── policies/
│   │   ├── allowed-locations-policy.json # Azure Policy restricting allowed regions
│   │   └── require-tag-policy.json       # Azure Policy enforcing mandatory tags
│   └── scripts/
│       ├── deploy.ps1             # One-click deployment script (PowerShell)
│       ├── deploy.sh              # One-click deployment script (Bash)
│       ├── cleanup.ps1            # Teardown script to prevent unwanted charges
│       └── cleanup.sh             # Teardown script (Bash)
│
├── .github/
│   └── workflows/
│       └── azure-deploy.yml       # Production GitHub Actions CI/CD pipeline
│
└── tests/
    ├── test_api_endpoints.py      # End-to-end integration tests
    ├── test_ml_service.py         # AI inference unit tests
    ├── test_calculators.py        # TCO, SLA, and Storage calculation tests
    ├── test_governance.py         # Policy and compliance tests
    └── test_quiz.py               # Exam scoring and error log tests
```

---

## ⚙️ Quickstart Guide

### Option 1: Run Locally (Python 3.12+)

```bash
# 1. Clone or navigate to the project directory
cd "C:\Study\AZ-900 Project"

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Re-train ML model artifacts
python ml/train_model.py

# 4. Launch the application
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser and navigate to:
- **Interactive Web Workbench:** [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check Endpoint:** [http://localhost:8000/health](http://localhost:8000/health)

---

### Option 2: Run with Docker & Docker Compose

```bash
# Build and run the containerized workload
docker-compose up --build -d

# Verify container health
docker ps
```

Access the application at [http://localhost:8000](http://localhost:8000).

---

### Option 3: Automated Testing

Run the full automated test suite with pytest:

```bash
pytest -v
```

All 16 test cases across ML inference, TCO calculators, composite SLA formulas, Azure Policy rules, and exam scoring execute in under 2 seconds.

---

## ☁️ Azure Cloud Deployment (Infrastructure as Code)

### Deploying via Azure CLI and Bicep

```powershell
# Authenticate to your Azure subscription
az login

# Execute the automated deployment script
.\infra\scripts\deploy.ps1 -ResourceGroupName "rg-azurecloudhub-prod" -Location "centralindia"
```

The script automatically:
1. Connects to your active Azure subscription.
2. Creates the target Resource Group with standard Cloud Adoption Framework (CAF) governance tags (`Environment=prod`, `Owner=Arighna Sadhu`, `CostCenter=CC-70500`).
3. Registers the **Allowed Locations Azure Policy definition**.
4. Provisions the Bicep template:
   - App Service Plan (Linux) & Web App for Containers
   - Storage Account with Zone-Redundant Storage (`Standard_ZRS`) & Lifecycle Rules
   - Log Analytics Workspace & Application Insights
   - Network Security Group (NSG) and Subnet
   - `CanNotDelete` Resource Lock
5. Outputs the live HTTPS URL for the deployed workload.

### Cleaning Up Resources (Cost Guard)

As highlighted in **Section 3.3 of the report**, cleaning up resources after testing is critical to avoid accidental consumption charges:

```powershell
.\infra\scripts\cleanup.ps1 -ResourceGroupName "rg-azurecloudhub-prod"
```

---

## 🎯 Syllabus & Internship Report Cross-Reference Matrix

| Syllabus Domain | Report Reference | Project Component |
| :--- | :--- | :--- |
| **Domain 1: Cloud Concepts** (25–30%) | Week 1 (§2.2), Table 1.1 | - CapEx vs OpEx TCO Calculator<br>- Shared Responsibility Interactive Matrix<br>- Scalability vs Elasticity Simulator |
| **Domain 2: Azure Architecture & Services** (35–40%) | Week 2 (§2.3) & Week 3 (§2.4), Tables 2.1 & 2.2 | - FastAPI Model Serving on Azure App Service<br>- Multi-AZ 99.99% Composite SLA Calculator<br>- Storage Redundancy (LRS/ZRS/GRS) & Tiering Simulator |
| **Domain 3: Management & Governance** (30–35%) | Week 4 (§2.5), Fig 2.2 | - Azure Policy & Tagging Evaluator<br>- Bicep (`main.bicep`) & ARM (`azuredeploy.json`) IaC<br>- CanNotDelete Resource Lock Safeguard<br>- Budget Alert Simulator ($150 with 80% threshold) |
| **Candidate Capstone Recommendation** | Section 3.3 (Recommendations) | - Containerized ML Microservice<br>- Live Telemetry & Application Insights Stream<br>- Curated Candidate Error Log Revision Module |

---

## 📜 Acknowledgements & References

1. **Mell, P. and Grance, T.**, *"The NIST Definition of Cloud Computing,"* Special Publication 800-145, National Institute of Standards and Technology, U.S. Department of Commerce.
2. **Microsoft Learn**, *"Study Guide for Exam AZ-900: Microsoft Azure Fundamentals,"* Microsoft Corporation.
3. **Certiport (Pearson VUE)**, *"Exam Score Report: AZ-900 Microsoft Azure Fundamentals,"* Candidate: Arighna Sadhu (Score: 942/1000), 28 October 2026.
4. **Chandigarh University**, Department of Computer Science and Engineering (Artificial Intelligence and Machine Learning), Gharuan, Punjab.
