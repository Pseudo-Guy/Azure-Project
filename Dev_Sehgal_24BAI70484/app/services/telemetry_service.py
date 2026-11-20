"""
Azure Monitor & Application Insights Telemetry Service.
Provides live observability, metrics aggregation, log streaming, and alert simulations.
"""

import time
from collections import deque
from datetime import datetime, timezone
from typing import Dict, List, Any

class TelemetryService:
    def __init__(self, max_logs: int = 100):
        self.start_time = time.time()
        self.total_requests = 0
        self.error_count = 0
        self.latencies = deque(maxlen=200)
        self.logs = deque(maxlen=max_logs)
        self.budget_limit_usd = 150.0
        self.current_spend_usd = 42.50

        # Prepopulate initial startup logs
        self.record_log("INFO", "Azure App Service container initialized successfully in Central India.")
        self.record_log("INFO", "Azure Application Insights telemetry sink connected (InstrumentationKey: active).")
        self.record_log("INFO", "Azure Storage account 'stcloudhubaiml' mounted in Hot access tier.")
        self.record_log("INFO", "Azure Cost Management budget set to $150.00/month with alerts at 80% and 100%.")

    def record_request(self, endpoint: str, latency_ms: float, status_code: int = 200):
        self.total_requests += 1
        self.latencies.append(latency_ms)
        if status_code >= 400:
            self.error_count += 1
            self.record_log("ERROR", f"HTTP {status_code} on {endpoint} (latency: {latency_ms:.1f}ms)")
        else:
            self.record_log("INFO", f"HTTP {status_code} on {endpoint} (latency: {latency_ms:.1f}ms)")

    def record_log(self, level: str, message: str, properties: Dict[str, Any] = None):
        entry = {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            "level": level,
            "message": message,
            "properties": properties or {}
        }
        self.logs.append(entry)

    def get_metrics(self) -> Dict[str, Any]:
        uptime_sec = time.time() - self.start_time
        avg_latency = (sum(self.latencies) / len(self.latencies)) if self.latencies else 0.0
        
        # P95 calculation
        sorted_lat = sorted(self.latencies) if self.latencies else [0.0]
        p95_idx = int(len(sorted_lat) * 0.95)
        p95_latency = sorted_lat[min(p95_idx, len(sorted_lat) - 1)]

        failure_rate = (self.error_count / self.total_requests * 100.0) if self.total_requests > 0 else 0.0

        # Cost Management Budget Calculation
        spend_percentage = round((self.current_spend_usd / self.budget_limit_usd) * 100.0, 1)
        budget_alert_active = spend_percentage >= 80.0

        return {
            "uptime_seconds": round(uptime_sec, 1),
            "uptime_human": f"{int(uptime_sec // 3600)}h {int((uptime_sec % 3600) // 60)}m {int(uptime_sec % 60)}s",
            "total_requests": self.total_requests,
            "error_count": self.error_count,
            "failure_rate_pct": round(failure_rate, 2),
            "avg_latency_ms": round(avg_latency, 2),
            "p95_latency_ms": round(p95_latency, 2),
            "cloud_provider": "Microsoft Azure",
            "service_model": "PaaS (App Service Linux Container)",
            "app_insights_status": "Healthy / Ingesting",
            "cost_management": {
                "budget_limit_usd": self.budget_limit_usd,
                "current_spend_usd": self.current_spend_usd,
                "spend_percentage": spend_percentage,
                "budget_alert_active": budget_alert_active,
                "alert_thresholds": ["80% ($120.00)", "100% ($150.00)"]
            },
            "recent_logs": list(reversed(self.logs))[:25]
        }

telemetry_service = TelemetryService()
