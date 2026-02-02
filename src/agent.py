"""
Agent Configuration for FI Market Analysis
==========================================

Reusable agent for automating market analysis operations.
"""

import json
from typing import Dict, List, Optional, Any
from pathlib import Path


class FIMarketAgent:
    """
    Reusable agent for FI market analysis automation.

    Capabilities:
    - Load and manage FI data
    - Score and prioritize accounts
    - Segment markets
    - Analyze competitive landscape
    - Generate visualizations
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the agent with configuration."""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "config.json"

        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.institutions = []
        self.scored_accounts = []
        self.context = {
            "data_loaded": False,
            "scored": False,
            "filters": {}
        }

    def load_data(self, source: str = "config") -> List[Dict]:
        """
        Load FI data from source.

        Args:
            source: 'config' for fi_database.json or path to CSV

        Returns:
            List of institution dictionaries
        """
        from data.fi_loader import FILoader
        loader = FILoader()

        if source == "config":
            self.institutions = loader.load_from_config()
        else:
            self.institutions = loader.load_from_csv(source)

        self.context["data_loaded"] = True
        return self.institutions

    def score_accounts(self, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Score all loaded accounts.

        Args:
            filters: Optional filters (region, type, min_assets, max_assets)

        Returns:
            List of scored account dictionaries
        """
        from analysis.scoring import AccountScorer

        if not self.context["data_loaded"]:
            self.load_data()

        scorer = AccountScorer()
        institutions = self.institutions

        # Apply filters
        if filters:
            if 'region' in filters:
                institutions = [fi for fi in institutions if fi.get('region') == filters['region']]
            if 'type' in filters:
                institutions = [fi for fi in institutions if fi.get('type') == filters['type']]
            if 'min_assets' in filters:
                institutions = [fi for fi in institutions if fi.get('assets', 0) >= filters['min_assets']]
            if 'max_assets' in filters:
                institutions = [fi for fi in institutions if fi.get('assets', 0) <= filters['max_assets']]

        self.scored_accounts = []
        for fi in institutions:
            result = scorer.score_account(fi)
            account = fi.copy()
            account['score'] = result['total_score']
            account['grade'] = result['grade']
            account['breakdown'] = result['breakdown']
            self.scored_accounts.append(account)

        self.scored_accounts.sort(key=lambda x: x['score'], reverse=True)
        self.context["scored"] = True
        self.context["filters"] = filters or {}

        return self.scored_accounts

    def get_top_accounts(self, n: int = 20) -> List[Dict]:
        """
        Get top N accounts by score.

        Args:
            n: Number of accounts to return

        Returns:
            List of top scored accounts
        """
        if not self.context["scored"]:
            self.score_accounts()

        return self.scored_accounts[:n]

    def segment_market(self, by: str) -> Dict[str, Dict]:
        """
        Segment the market by a dimension.

        Args:
            by: 'asset_tier', 'type', 'region', or 'vendor'

        Returns:
            Dictionary of segments with counts and totals
        """
        from analysis.segmentation import MarketSegmentation

        if not self.context["data_loaded"]:
            self.load_data()

        segmentation = MarketSegmentation()

        if by == 'asset_tier':
            return segmentation.by_asset_tier(self.institutions)
        elif by == 'type':
            return segmentation.by_type(self.institutions)
        elif by == 'region':
            return segmentation.by_region(self.institutions)
        elif by == 'vendor':
            return segmentation.by_vendor(self.institutions)
        else:
            raise ValueError(f"Unknown segmentation: {by}")

    def analyze_competitive_landscape(self) -> Dict[str, Any]:
        """
        Analyze the competitive landscape.

        Returns:
            Competitive analysis results
        """
        from analysis.competitive import CompetitiveAnalysis

        if not self.context["data_loaded"]:
            self.load_data()

        analysis = CompetitiveAnalysis()
        return analysis.analyze(self.institutions)

    def estimate_pipeline_value(self, accounts: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Estimate total pipeline value.

        Args:
            accounts: Optional list of accounts (uses scored_accounts if not provided)

        Returns:
            Pipeline value estimates
        """
        from targeting.prioritization import AccountPrioritization

        if accounts is None:
            if not self.context["scored"]:
                self.score_accounts()
            accounts = self.scored_accounts

        prioritizer = AccountPrioritization()
        return prioritizer.estimate_pipeline(accounts)

    def generate_chart(self, chart_type: str, output_path: Optional[str] = None) -> str:
        """
        Generate a visualization chart.

        Args:
            chart_type: 'competitive', 'scoring', 'pipeline', 'segments'
            output_path: Optional output file path

        Returns:
            Path to generated chart
        """
        from visualization.charts import ChartGenerator

        if not self.context["data_loaded"]:
            self.load_data()

        chart_gen = ChartGenerator()
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)

        if output_path is None:
            output_path = str(output_dir / f"{chart_type}_chart.html")

        if chart_type == 'competitive':
            fig = chart_gen.competitive_landscape(self.institutions)
        elif chart_type == 'scoring':
            if not self.context["scored"]:
                self.score_accounts()
            fig = chart_gen.scoring_distribution(self.institutions)
        elif chart_type == 'pipeline':
            fig = chart_gen.pipeline_by_segment(self.institutions)
        elif chart_type == 'segments':
            fig = chart_gen.market_segments(self.institutions)
        else:
            raise ValueError(f"Unknown chart type: {chart_type}")

        fig.write_html(output_path)
        return output_path

    def get_context(self) -> Dict[str, Any]:
        """Return current agent context."""
        return {
            **self.context,
            "institution_count": len(self.institutions),
            "scored_count": len(self.scored_accounts)
        }

    def reset(self) -> None:
        """Reset agent state."""
        self.institutions = []
        self.scored_accounts = []
        self.context = {
            "data_loaded": False,
            "scored": False,
            "filters": {}
        }


def create_agent(config_path: Optional[str] = None) -> FIMarketAgent:
    """Factory function to create a configured agent."""
    return FIMarketAgent(config_path)


AGENT_METADATA = {
    "name": "fi-market-analysis-agent",
    "version": "1.0.0",
    "description": "Analyzes financial institution market for account targeting",
    "capabilities": [
        "load_fi_data",
        "score_accounts",
        "segment_market",
        "competitive_analysis",
        "pipeline_estimation",
        "visualization"
    ],
    "config_schema": {
        "type": "object",
        "properties": {
            "config_path": {"type": "string", "description": "Path to config.json"}
        }
    }
}
