# AzureCloudHub: AI Model-Serving Architecture & AZ-900 Cloud Mastery Suite

[![Azure Certification](https://img.shields.io/badge/Microsoft%20Certified-AZ--900%20(971%2F1000)-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/credentials/certifications/resources/study-guides/az-900)
[![Python Version](https://img.shields.io/badge/Python-3.12%20%7C%203.14-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production%20Ready-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade, portfolio-ready cloud engineering project designed and developed from the **Industrial Internship Report** of **Dev Sehgal** (UID: `24BAI70484`, B.E. Computer Science and Engineering - Artificial Intelligence & Machine Learning, Chandigarh University).

The project brings to life the explicit capstone recommendations documented in **Chapter 3, Section 3.3** of the report:
> *"Build a small end-to-end project, such as hosting a web application with a managed database and monitoring, to apply the fundamentals in a realistic design... begin each lab by creating a budget alert and tagging convention... and practise infrastructure as code with Bicep or ARM templates."*

---

## 📑 Candidate Profile & Examination Credentials

- **Candidate Name:** Dev Sehgal
- **University Identifier (UID):** `24BAI70484`
- **Degree:** Bachelor of Engineering in Computer Science and Engineering (Artificial Intelligence & Machine Learning)
- **Institution:** Chandigarh University, Gharuan, Mohali, Punjab
- **Report Title:** *Cloud Fundamentals with Microsoft Azure: A Hands-On Study of Cloud Concepts, Azure Architecture and Governance (AZ-900)*
- **Internship Duration:** 01 June 2026 to 30 June 2026 (5 Weeks)
- **Examination Date:** 28 October 2026
- **AZ-900 Examination Result:** **Passed (971 / 1000)** *(Passing Bar: 700)*
  - **Describe cloud concepts (25–30%):** **95%**
  - **Describe Azure architecture and services (35–40%):** **100% (Perfect Score)**
  - **Describe Azure management and governance (30–35%):** **96%**

---

## 📅 5-Week Internship Curriculum Mapping

| Week | Dates | Domain / Topic | Hands-On Focus & Project Mapping |
| :--- | :--- | :--- | :--- |
| **Week 1** | 01/06/2026 – 05/06/2026 | **Describe cloud concepts** | CapEx vs OpEx, consumption pricing, Shared Responsibility Model, IaaS/PaaS/SaaS/Serverless. |
| **Week 2** | 08/06/2026 – 12/06/2026 | **Azure architecture – core services** | Regions, Availability Zones, Resource Hierarchy, VMs, App Service, VNets, Subnets, NSGs. |
| **Week 3** | 15/06/2026 – 19/06/2026 | **Storage, migration, identity and security** | Storage accounts (LRS/ZRS/GRS/GZRS), Blob Tiers (Hot/Cool/Cold/Archive), Entra ID, RBAC, Zero Trust. |
| **Week 4** | 22/06/2026 – 26/06/2026 | **Management and governance** | Cost Management, Pricing & TCO calculators, Azure Policy, CanNotDelete locks, Azure Monitor & Bicep IaC. |
| **Week 5** | 29/06/2026 – 30/06/2026 | **Revision and consolidation** | Full mock exam practice, error log synthesis, final internship report consolidation. |

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
- Sub-20ms inference latency with probability distributions and telemetry logging.

### 2. 🏛️ Azure Architecture & Services Explorer
- **Interactive Shared Responsibility Visualizer:** Toggle between **On-Premises**, **IaaS**, **PaaS**, and **SaaS** to inspect the shifting division of responsibility for data, identities, OS patching, hypervisors, and physical datacenters.
- **Storage Redundancy & Lifecycle Simulator:** Calculate costs and durability guarantees across **LRS** (11 nines), **ZRS** (12 nines), **GRS** (16 nines), and **GZRS** (16 nines), and simulate access tiers (**Hot**, **Cool**, **Cold**, **Archive** with 1-15 hour rehydration latency).

### 3. 💰 Cloud Economics & TCO Engine (`app/services/cloud_calculator.py`)
- **CapEx vs OpEx Projection:** Dynamic slider-based model computing total on-premises datacenter costs vs Azure consumption-based billing.
- **Pricing Optimization Tiers:** Simulates **Pay-As-You-Go**, **1-Year Reserved Instances (38% off)**, **3-Year Reserved Instances (62% off)**, **Spot VMs (85% off)**, and **Azure Hybrid Benefit (up to 40% software assurance discount)**.

### 4. 🛡️ Azure Governance & Composite SLA Calculator (`app/services/governance_service.py`)
- **Azure Policy Evaluation Engine:** Validates target deployment regions against approved geographic boundaries (`centralindia`, `eastus`, `westeurope`), enforces mandatory Cloud Adoption Framework (CAF) tags (`Environment`, `Owner`, `Project`, `CostCenter`), and verifies resource naming patterns.
- **Resource Lock Verification:** Assesses `CanNotDelete` and `ReadOnly` locks protecting critical cloud assets.
- **Composite SLA Multiplier:** Computes end-to-end multi-tier availability and demonstrates how deploying across **3 Availability Zones** elevates uptime to **99.99%**.

### 5. 📝 AZ-900 Exam Simulator & Error Log Revision (`app/services/quiz_service.py`)
- **20-Question Full Mock Examination:** Mapped strictly to the three examination domain weights with Certiport 1000-point scoring benchmarked against **Dev Sehgal's 971 score**.
- **Curated Error Log:** Interactive revision entries reviewing conceptual traps:
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
Dev_Sehgal_24BAI70484/
├── README.md                      # Complete system documentation & syllabus mapping
├── requirements.txt               # Production Python dependencies
├── pytest.ini                     # Pytest configuration
├── Dockerfile                     # Multi-stage production container build
├── docker-compose.yml             # Local container orchestration
│
├── app/
│   ├── main.py                    # FastAPI application & lifespan setup
│   ├── models/schemas.py          # Pydantic v2 data models & request/response schemas
│   ├── services/
│   │   ├── ml_service.py          # Dual-head ML classifier & batch inference engine
│   │   ├── cloud_calculator.py    # TCO, Composite SLA & Storage simulator
│   │   ├── governance_service.py  # Azure Policy & CanNotDelete lock validator
│   │   ├── telemetry_service.py   # Application Insights & Azure Monitor simulator
│   │   └── quiz_service.py        # AZ-900 mock engine & candidate error log
│   ├── api/                       # REST routers (/api/ml, /api/calculator, /api/governance, ...)
│   └── static/                    # Modern Azure-themed glassmorphism Single Page App
│       ├── index.html             # 6-tab interactive web workbench
│       ├── css/style.css          # Custom styling & dark-mode theme
│       └── js/app.js              # Interactive client-side controller
│
├── ml/
│   ├── train_model.py             # Training pipeline for sentiment & category model
│   └── model_artifacts/           # Serialized classifier, vectorizer, and category models
│
├── infra/
│   ├── bicep/
│   │   ├── main.bicep             # Azure Bicep Infrastructure as Code template
│   │   └── parameters.bicepparam  # Bicep environment parameters
│   ├── arm/azuredeploy.json       # Exported ARM template equivalent
│   ├── policies/
│   │   ├── allowed-locations-policy.json # Azure Policy restricting allowed regions
│   │   └── require-tag-policy.json       # Azure Policy enforcing mandatory tags
│   └── scripts/
│       ├── deploy.ps1 / deploy.sh # One-click deployment scripts (PowerShell & Bash)
│       └── cleanup.ps1 / cleanup.sh # Teardown scripts to prevent unwanted charges
│
├── .github/workflows/azure-deploy.yml # Production GitHub Actions CI/CD pipeline
└── tests/                         # 16 unit and integration tests (100% passing)
```

---

## ⚙️ Quickstart Guide

### Option 1: Run Locally (Python 3.12+)

```bash
# 1. Navigate to the project directory
cd "C:\Study\AZ-900 Project\Dev_Sehgal_24BAI70484"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the application
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser and navigate to:
- **Interactive Web Workbench:** [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check Endpoint:** [http://localhost:8000/health](http://localhost:8000/health)

---

### Option 2: Run with Docker & Docker Compose

```bash
docker-compose up --build -d
```

---

### Option 3: Automated Testing

Run the full automated test suite with pytest:

```bash
pytest -v
```

All 16 test cases execute and validate cleanly in under 2 seconds.

---

## ☁️ Azure Cloud Deployment (Infrastructure as Code)

### Deploying via Azure CLI and Bicep

```powershell
az login

.\infra\scripts\deploy.ps1 -ResourceGroupName "rg-azurecloudhub-prod" -Location "centralindia"
```

The script automatically:
1. Connects to your active Azure subscription.
2. Creates the target Resource Group with standard Cloud Adoption Framework (CAF) governance tags (`Environment=prod`, `Owner=Dev Sehgal`, `CostCenter=CC-70484`).
3. Registers the **Allowed Locations Azure Policy definition**.
4. Provisions the Bicep template:
   - App Service Plan (Linux) & Web App for Containers
   - Storage Account with Zone-Redundant Storage (`Standard_ZRS`) & Lifecycle Rules
   - Log Analytics Workspace & Application Insights
   - Network Security Group (NSG) and Subnet
   - `CanNotDelete` Resource Lock
5. Outputs the live HTTPS URL for the deployed workload.

### Cleaning Up Resources (Cost Guard)

As highlighted in **Section 3.3 of Dev Sehgal's report**, cleaning up resources after testing is critical to avoid accidental consumption charges:

```powershell
.\infra\scripts\cleanup.ps1 -ResourceGroupName "rg-azurecloudhub-prod"
```

---

## 📜 Acknowledgements & References

1. **Mell, P. and Grance, T.**, *"The NIST Definition of Cloud Computing,"* NIST Special Publication 800-145, National Institute of Standards and Technology, Gaithersburg, MD, 2011.
2. **Armbrust, M., et al.**, *"A View of Cloud Computing,"* Communications of the ACM, Vol. 53, No. 4, 2010, pp. 50-58.
3. **Microsoft Learn**, *"Study Guide for Exam AZ-900: Microsoft Azure Fundamentals,"* Microsoft Corporation.
4. **Microsoft Exam Score Report**, *"AZ-900: Microsoft Azure Fundamentals,"* Candidate: Dev Sehgal (Score: 971/1000), 28 October 2026.
5. **Chandigarh University**, Department of Computer Science and Engineering (Artificial Intelligence & Machine Learning), Gharuan, Punjab.
