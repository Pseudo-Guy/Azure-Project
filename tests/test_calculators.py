"""
Unit tests for Cloud Economics, Composite SLA, and Storage Simulation.
"""

from app.models.schemas import TCORequest, SLACalculatorRequest, SLAComponent, StorageSimulatorRequest
from app.services.cloud_calculator import cloud_calculator

def test_tco_calculation_savings():
    req = TCORequest(
        num_servers=10,
        cpu_cores_per_server=8,
        ram_gb_per_server=32,
        storage_tb=10.0,
        years=3,
        purchase_model="reserved_3yr",
        use_azure_hybrid_benefit=True
    )
    res = cloud_calculator.calculate_tco(req)
    assert res.on_premises_total_usd > 0
    assert res.azure_total_usd > 0
    assert res.cost_savings_usd > 0
    assert res.cost_savings_percentage > 0
    assert len(res.on_premises_breakdown) == 5
    assert len(res.azure_breakdown) == 3

def test_composite_sla_serial_and_zones():
    # Serial components without zones
    req_serial = SLACalculatorRequest(
        architecture_name="Serial App + DB",
        components=[
            SLAComponent(name="App Service", sla_percentage=99.95, tier="Premium"),
            SLAComponent(name="SQL Database", sla_percentage=99.99, tier="General Purpose")
        ],
        deployment_mode="single_instance"
    )
    res_serial = cloud_calculator.calculate_sla(req_serial)
    # 0.9995 * 0.9999 = 0.9994 -> 99.94%
    assert res_serial.composite_sla_percentage < 99.95
    assert res_serial.max_downtime_per_year_hours > 0

    # Availability zones deployment boosts SLA
    req_az = SLACalculatorRequest(
        architecture_name="Zone Resilient Architecture",
        components=[
            SLAComponent(name="App Service", sla_percentage=99.95, tier="Premium"),
            SLAComponent(name="SQL Database", sla_percentage=99.99, tier="General Purpose")
        ],
        deployment_mode="availability_zones"
    )
    res_az = cloud_calculator.calculate_sla(req_az)
    assert res_az.composite_sla_percentage >= 99.98
    assert res_az.high_availability_tier.startswith("Mission-Critical") or res_az.high_availability_tier.startswith("High Availability")

def test_storage_simulator_tiers_and_durability():
    # LRS Hot
    req_lrs = StorageSimulatorRequest(data_size_gb=1000, redundancy_type="LRS", tier="Hot", monthly_read_gb=100)
    res_lrs = cloud_calculator.simulate_storage(req_lrs)
    assert "11 nines" in res_lrs.durability
    assert res_lrs.total_monthly_cost_usd > 0

    # GRS Archive
    req_grs = StorageSimulatorRequest(data_size_gb=1000, redundancy_type="GRS", tier="Archive", monthly_read_gb=100)
    res_grs = cloud_calculator.simulate_storage(req_grs)
    assert "16 nines" in res_grs.durability
    assert "hours" in res_grs.rehydration_latency.lower()
