"""
Market Data
===========

Industry and market benchmark data.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class IndustryBenchmark:
    """Industry benchmark data."""
    metric: str
    value: float
    percentile_25: float
    percentile_50: float
    percentile_75: float
    source: str


class MarketData:
    """
    Market and industry benchmark data for FI analysis.
    """

    def __init__(self):
        self.benchmarks = self._load_benchmarks()
        self.industry_trends = self._load_trends()

    def _load_benchmarks(self) -> Dict[str, IndustryBenchmark]:
        """Load industry benchmarks."""
        return {
            "digital_adoption": IndustryBenchmark(
                metric="Digital Banking Adoption",
                value=0.72,
                percentile_25=0.55,
                percentile_50=0.72,
                percentile_75=0.85,
                source="Industry Report 2024"
            ),
            "mobile_users": IndustryBenchmark(
                metric="Mobile Banking Users %",
                value=0.65,
                percentile_25=0.45,
                percentile_50=0.65,
                percentile_75=0.78,
                source="Industry Report 2024"
            ),
            "cost_per_transaction": IndustryBenchmark(
                metric="Cost per Transaction",
                value=0.35,
                percentile_25=0.25,
                percentile_50=0.35,
                percentile_75=0.50,
                source="Industry Report 2024"
            ),
            "member_attrition": IndustryBenchmark(
                metric="Annual Member Attrition",
                value=0.08,
                percentile_25=0.05,
                percentile_50=0.08,
                percentile_75=0.12,
                source="Industry Report 2024"
            )
        }

    def _load_trends(self) -> Dict[str, Dict]:
        """Load industry trends."""
        return {
            "digital_transformation": {
                "trend": "increasing",
                "growth_rate": 0.15,
                "description": "FIs investing heavily in digital capabilities"
            },
            "fintech_competition": {
                "trend": "increasing",
                "growth_rate": 0.25,
                "description": "Neobanks capturing market share"
            },
            "data_analytics": {
                "trend": "increasing",
                "growth_rate": 0.20,
                "description": "Growing demand for member insights"
            },
            "open_banking": {
                "trend": "emerging",
                "growth_rate": 0.30,
                "description": "API-first strategies gaining traction"
            }
        }

    def get_benchmark(self, metric: str) -> Optional[IndustryBenchmark]:
        """Get benchmark for a metric."""
        return self.benchmarks.get(metric)

    def get_trend(self, trend_name: str) -> Optional[Dict]:
        """Get trend data."""
        return self.industry_trends.get(trend_name)

    def get_tam_estimate(self, region: Optional[str] = None) -> Dict:
        """
        Get Total Addressable Market estimate.

        Args:
            region: Optional region filter

        Returns:
            TAM estimate dictionary
        """
        # Simplified TAM estimation
        base_tam = {
            "total_fis": 10000,
            "average_deal_size": 150000,
            "tam": 1500000000
        }

        regional_factors = {
            "West": 0.20,
            "Mountain": 0.08,
            "Southwest": 0.12,
            "Midwest": 0.18,
            "Southeast": 0.22,
            "Northeast": 0.15,
            "Mid-Atlantic": 0.05
        }

        if region:
            factor = regional_factors.get(region, 0.10)
            return {
                "region": region,
                "total_fis": int(base_tam["total_fis"] * factor),
                "average_deal_size": base_tam["average_deal_size"],
                "tam": base_tam["tam"] * factor
            }

        return base_tam

    def get_competitive_market_share(self) -> Dict[str, float]:
        """Get estimated market share by competitor."""
        return {
            "FIS": 0.28,
            "Fiserv": 0.24,
            "Jack Henry": 0.18,
            "NCR": 0.08,
            "Q2": 0.06,
            "Alkami": 0.04,
            "Temenos": 0.03,
            "Other": 0.09
        }
