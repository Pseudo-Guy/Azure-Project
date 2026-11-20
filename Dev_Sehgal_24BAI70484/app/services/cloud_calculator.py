"""
Cloud Economics, TCO, Composite SLA, and Storage Redundancy Simulators.
Directly implements the AZ-900 concepts from Dev Sehgal's internship report.
"""

from typing import List, Dict
from app.models.schemas import (
    TCORequest, TCOResponse, TCUBreakdownItem,
    SLACalculatorRequest, SLACalculatorResponse,
    StorageSimulatorRequest, StorageSimulatorResponse
)

class CloudCalculatorService:

    @staticmethod
    def calculate_tco(req: TCORequest) -> TCOResponse:
        years = req.years
        num_servers = req.num_servers
        storage_tb = req.storage_tb

        # --- 1. On-Premises Costs (CapEx + Datacenter OpEx) ---
        # Hardware server cost (CapEx): ~$4,200 per 8-core/32GB server
        server_hw_unit = 1500.0 + (req.cpu_cores_per_server * 150.0) + (req.ram_gb_per_server * 35.0)
        total_server_capex = server_hw_unit * num_servers
        
        # Hardware maintenance / warranty (OpEx): 15% per year
        hw_maintenance_annual = total_server_capex * 0.15 * years
        
        # Datacenter facility, power, cooling, floor space: ~$1,800 per server/year
        datacenter_power_facility = num_servers * 1800.0 * years
        
        # On-prem SAN/NAS Storage hardware + drive replacements
        storage_capex_opex = (storage_tb * 250.0) + (storage_tb * 50.0 * years)
        
        # IT administration and virtualization licensing (VMware / Windows Server)
        it_admin_and_licensing = (num_servers * 2200.0 * years) + (storage_tb * 30.0 * years)
        
        on_prem_total = total_server_capex + hw_maintenance_annual + datacenter_power_facility + storage_capex_opex + it_admin_and_licensing

        # --- 2. Azure Cloud Costs (100% OpEx) ---
        # Base hourly compute rate for equivalent Azure VM (e.g. D-series v5)
        # Approximate: $0.048 per core/hr + $0.004 per GB RAM/hr
        base_hourly_per_vm = (req.cpu_cores_per_server * 0.035) + (req.ram_gb_per_server * 0.004)
        base_annual_vm_cost = base_hourly_per_vm * 730 * 12 * num_servers
        
        # Pricing model discount multipliers (from AZ-900 syllabus)
        discounts = {
            "pay_as_you_go": 1.0,
            "reserved_1yr": 0.62,   # ~38% discount
            "reserved_3yr": 0.38,   # ~62% discount
            "spot": 0.15            # ~85% discount
        }
        discount_rate = discounts.get(req.purchase_model.lower(), 1.0)
        
        # Azure Hybrid Benefit applies up to 40% additional discount on Windows/SQL licenses
        ahb_factor = 0.60 if req.use_azure_hybrid_benefit else 1.0
        
        effective_azure_compute = base_annual_vm_cost * discount_rate * ahb_factor * years
        
        # Managed Disks & Blob storage in Azure (~$0.045 / GB / month)
        azure_storage_cost = (storage_tb * 1024 * 0.045 * 12) * years
        
        # Networking egress & Azure Monitor logging
        azure_network_monitoring = (num_servers * 25.0 * 12) * years
        
        azure_total = effective_azure_compute + azure_storage_cost + azure_network_monitoring
        
        savings_usd = round(max(0.0, on_prem_total - azure_total), 2)
        savings_pct = round((savings_usd / on_prem_total) * 100.0, 1) if on_prem_total > 0 else 0.0

        on_prem_breakdown = [
            TCUBreakdownItem(name="Server Hardware (CapEx)", cost_usd=round(total_server_capex, 2), description="Physical rack servers, CPUs, RAM, and motherboard chassis"),
            TCUBreakdownItem(name="Hardware Maintenance (OpEx)", cost_usd=round(hw_maintenance_annual, 2), description="OEM vendor support, parts replacement, and hardware warranties"),
            TCUBreakdownItem(name="Datacenter Facilities & Power", cost_usd=round(datacenter_power_facility, 2), description="Electricity, HVAC precision cooling, floor space leasing, UPS batteries"),
            TCUBreakdownItem(name="SAN/NAS Storage Hardware", cost_usd=round(storage_capex_opex, 2), description="Storage controllers, SAS drives, Fibre Channel SAN switches"),
            TCUBreakdownItem(name="IT Staffing & OS Licensing", cost_usd=round(it_admin_and_licensing, 2), description="System admin labor, hypervisor licenses, datacenter security staff")
        ]

        azure_breakdown = [
            TCUBreakdownItem(name=f"Azure Compute ({req.purchase_model})", cost_usd=round(effective_azure_compute, 2), description=f"Elastic virtual machines with {req.purchase_model.replace('_', ' ')} discount and AHB={req.use_azure_hybrid_benefit}"),
            TCUBreakdownItem(name="Azure Managed Disks & Blob", cost_usd=round(azure_storage_cost, 2), description=f"{storage_tb} TB resilient managed cloud storage with SLA-backed durability"),
            TCUBreakdownItem(name="Azure Monitor & Data Egress", cost_usd=round(azure_network_monitoring, 2), description="Full observability metrics, Log Analytics ingestion, and outbound bandwidth")
        ]

        capex_summary = (
            f"Over {years} years, migrating {num_servers} servers to Azure eliminates ${round(total_server_capex, 2):,} "
            f"in up-front Capital Expenditure (CapEx). Under the {req.purchase_model.replace('_', ' ')} model, "
            f"your organisation saves approximately ${savings_usd:,} ({savings_pct}% reduction) through operational efficiency."
        )

        return TCOResponse(
            on_premises_total_usd=round(on_prem_total, 2),
            azure_total_usd=round(azure_total, 2),
            cost_savings_usd=savings_usd,
            cost_savings_percentage=savings_pct,
            capex_vs_opex_summary=capex_summary,
            on_premises_breakdown=on_prem_breakdown,
            azure_breakdown=azure_breakdown,
            applied_discount_rate=round(1.0 - (discount_rate * ahb_factor), 2)
        )

    @staticmethod
    def calculate_sla(req: SLACalculatorRequest) -> SLACalculatorResponse:
        """
        Calculates composite SLA for multi-tier Azure architectures.
        Serial formula: SLA_total = SLA_1 * SLA_2 * ... * SLA_n
        Zone/Region redundancy provides enhanced parallel availability.
        """
        if not req.components:
            return SLACalculatorResponse(
                architecture_name=req.architecture_name,
                composite_sla_percentage=99.9,
                max_downtime_per_year_hours=8.76,
                max_downtime_per_month_minutes=43.8,
                max_downtime_per_week_minutes=10.08,
                redundancy_level="Baseline",
                high_availability_tier="Standard",
                recommendations=["Add at least one service component to calculate composite SLA."]
            )

        # Baseline serial calculation
        serial_factor = 1.0
        for c in req.components:
            serial_factor *= (c.sla_percentage / 100.0)

        composite_sla = serial_factor * 100.0
        
        # Redundancy mode impact (AZ-900 syllabus Section 2.2 / Table 2.1)
        mode = req.deployment_mode.lower()
        recommendations = []

        if mode == "availability_zones":
            # Multi-AZ deployment mitigates single datacenter failures
            # E.g., single VM (99.9%) -> Multi-AZ deployment (99.99%)
            boost = (100.0 - composite_sla) * 0.75
            composite_sla = min(99.99, composite_sla + boost)
            redundancy_level = "Zone Redundant (3 Availability Zones in 1 Region)"
            recommendations.append("Workload is protected against single-datacenter power, cooling, or network failure.")
            recommendations.append("Ensure application uses zone-redundant storage (ZRS) or geo-zone-redundant storage (GZRS).")
        elif mode == "multi_region_paired":
            # Active-passive or active-active failover across paired regions
            boost = (100.0 - composite_sla) * 0.95
            composite_sla = min(99.999, composite_sla + boost)
            redundancy_level = "Multi-Region Paired (Azure Region Pair with Traffic Manager/Front Door)"
            recommendations.append("Workload is protected against regional catastrophic disasters.")
            recommendations.append("Use Azure Front Door or Traffic Manager for global DNS load balancing and auto-failover.")
        else:
            redundancy_level = "Single Region / Single Datacenter"
            recommendations.append("Notice that combining services in series reduces the overall composite SLA.")
            recommendations.append("Consider deploying across Availability Zones to achieve up to 99.99% SLA.")
            recommendations.append("Single VM with Premium SSD guarantees 99.9%, whereas spreading across Availability Zones increases SLA to 99.99%.")

        composite_sla = round(composite_sla, 4)
        unavailability_fraction = (100.0 - composite_sla) / 100.0

        # Downtime estimations:
        # 1 year = 8760 hours
        # 1 month = 43800 minutes (~30.4 days)
        # 1 week = 10080 minutes
        downtime_year_hrs = round(unavailability_fraction * 8760.0, 2)
        downtime_month_mins = round(unavailability_fraction * 43800.0, 2)
        downtime_week_mins = round(unavailability_fraction * 10080.0, 2)

        if composite_sla >= 99.99:
            ha_tier = "Mission-Critical (99.99%+)"
        elif composite_sla >= 99.9:
            ha_tier = "High Availability (99.9% - 99.99%)"
        else:
            ha_tier = "Standard / Non-Critical (<99.9%)"

        return SLACalculatorResponse(
            architecture_name=req.architecture_name,
            composite_sla_percentage=composite_sla,
            max_downtime_per_year_hours=downtime_year_hrs,
            max_downtime_per_month_minutes=downtime_month_mins,
            max_downtime_per_week_minutes=downtime_week_mins,
            redundancy_level=redundancy_level,
            high_availability_tier=ha_tier,
            recommendations=recommendations
        )

    @staticmethod
    def simulate_storage(req: StorageSimulatorRequest) -> StorageSimulatorResponse:
        """
        Simulates Azure Storage costs, durability nines, replication scopes,
        and access tier rehydration characteristics (Table 2.2 in internship report).
        """
        # Redundancy multipliers
        redundancy_multipliers = {
            "LRS": 1.0,
            "ZRS": 1.25,
            "GRS": 2.0,
            "GZRS": 2.5
        }
        
        # Access tier base monthly storage rate per GB
        tier_storage_rates = {
            "Hot": 0.018,
            "Cool": 0.010,
            "Cold": 0.0036,
            "Archive": 0.00099
        }

        # Data retrieval cost per GB
        tier_retrieval_rates = {
            "Hot": 0.0,
            "Cool": 0.01,
            "Cold": 0.03,
            "Archive": 0.02
        }

        red_key = req.redundancy_type.upper()
        if red_key not in redundancy_multipliers:
            red_key = "LRS"

        tier_key = req.tier.capitalize()
        if tier_key not in tier_storage_rates:
            tier_key = "Hot"

        base_rate = tier_storage_rates[tier_key]
        red_mult = redundancy_multipliers[red_key]
        
        storage_cost = req.data_size_gb * (base_rate * red_mult)
        retrieval_cost = req.monthly_read_gb * tier_retrieval_rates[tier_key]
        total_cost = storage_cost + retrieval_cost

        metadata = {
            "LRS": {
                "durability": "99.999999999% (11 nines)",
                "scope": "3 copies replicated synchronously within a single datacenter in primary region",
                "availability": "99.9% (Hot/Cool)",
                "use_case": "Dev/test workloads or non-critical data with external backup"
            },
            "ZRS": {
                "durability": "99.9999999999% (12 nines)",
                "scope": "Replicated across 3 Availability Zones within the primary region",
                "availability": "99.9% (Hot/Cool)",
                "use_case": "High availability applications requiring zone-level fault isolation"
            },
            "GRS": {
                "durability": "99.99999999999999% (16 nines)",
                "scope": "LRS (3 copies) in primary region + async copy to secondary paired region (hundreds of miles away)",
                "availability": "99.9% (RA-GRS allows read access from secondary)",
                "use_case": "Enterprise disaster recovery protection against regional catastrophes"
            },
            "GZRS": {
                "durability": "99.99999999999999% (16 nines)",
                "scope": "ZRS across 3 zones in primary region + async copy to secondary paired region",
                "availability": "99.9% (RA-GZRS allows read access from secondary)",
                "use_case": "Maximum durability and availability for mission-critical production data"
            }
        }

        rehydration_info = {
            "Hot": "Instant (sub-second)",
            "Cool": "Instant (sub-second)",
            "Cold": "Instant (sub-second)",
            "Archive": "High Priority: ~1 hour; Standard: 3 to 15 hours"
        }

        meta = metadata.get(red_key, metadata["LRS"])

        return StorageSimulatorResponse(
            data_size_gb=req.data_size_gb,
            redundancy_type=red_key,
            tier=tier_key,
            monthly_storage_cost_usd=round(storage_cost, 2),
            monthly_retrieval_cost_usd=round(retrieval_cost, 2),
            total_monthly_cost_usd=round(total_cost, 2),
            durability=meta["durability"],
            replication_scope=meta["scope"],
            availability_sla=meta["availability"],
            rehydration_latency=rehydration_info.get(tier_key, "Instant"),
            ideal_use_case=meta["use_case"]
        )

cloud_calculator = CloudCalculatorService()
