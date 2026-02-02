"""
Account Scoring
===============

Score accounts based on targeting criteria.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional


class AccountScorer:
    """
    Score financial institution accounts for targeting prioritization.

    Scoring factors:
    - Asset size (25%): Larger FIs = higher potential deal value
    - Technology fit (30%): Modern stack = easier integration
    - Competitive opportunity (25%): Legacy vendors = displacement opportunity
    - Regional presence (20%): Target regions = higher priority
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the scorer with configuration."""
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "config.json"

        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.weights = self.config.get('scoring_weights', {
            'asset_size': 0.25,
            'technology_fit': 0.30,
            'competitive_opportunity': 0.25,
            'regional_presence': 0.20
        })

        self.thresholds = self.config.get('score_thresholds', {
            'hot': 80,
            'warm': 60,
            'developing': 40
        })

        self.target_regions = self.config.get('target_regions', ['Mountain', 'West', 'Southwest'])

        # Vendors with displacement opportunity (legacy systems)
        self.displacement_targets = ['FIS', 'Fiserv', 'NCR', 'Jack Henry']

    def score_account(self, institution: Dict) -> Dict[str, Any]:
        """
        Score a single financial institution.

        Args:
            institution: Institution dictionary with name, assets, region, etc.

        Returns:
            Scoring result with total_score, grade, and breakdown
        """
        breakdown = {}

        # Asset size score (0-100)
        assets = institution.get('assets', 0)
        breakdown['asset_size'] = self._score_assets(assets) * self.weights['asset_size'] * 100

        # Technology fit score (0-100)
        tech_stack = institution.get('tech_stack', 'unknown')
        breakdown['technology_fit'] = self._score_tech_fit(tech_stack) * self.weights['technology_fit'] * 100

        # Competitive opportunity score (0-100)
        vendor = institution.get('current_vendor', 'Unknown')
        breakdown['competitive_opportunity'] = self._score_competitive(vendor) * self.weights['competitive_opportunity'] * 100

        # Regional presence score (0-100)
        region = institution.get('region', 'Unknown')
        breakdown['regional_presence'] = self._score_region(region) * self.weights['regional_presence'] * 100

        # Total score
        total_score = sum(breakdown.values())

        # Determine grade
        if total_score >= self.thresholds['hot']:
            grade = 'HOT'
        elif total_score >= self.thresholds['warm']:
            grade = 'WARM'
        elif total_score >= self.thresholds['developing']:
            grade = 'DEVELOPING'
        else:
            grade = 'COLD'

        # Determine asset tier
        asset_tier = self._get_asset_tier(assets)

        return {
            'total_score': round(total_score, 1),
            'grade': grade,
            'breakdown': {k: round(v, 1) for k, v in breakdown.items()},
            'asset_tier': asset_tier
        }

    def _score_assets(self, assets: float) -> float:
        """Score based on asset size (0-1)."""
        if assets >= 10_000_000_000:  # $10B+
            return 1.0
        elif assets >= 5_000_000_000:  # $5B-$10B
            return 0.9
        elif assets >= 1_000_000_000:  # $1B-$5B
            return 0.8
        elif assets >= 500_000_000:   # $500M-$1B
            return 0.6
        elif assets >= 100_000_000:   # $100M-$500M
            return 0.4
        else:
            return 0.2

    def _score_tech_fit(self, tech_stack: str) -> float:
        """Score based on technology compatibility (0-1)."""
        tech_scores = {
            'modern': 1.0,
            'mixed': 0.7,
            'legacy': 0.4,
            'unknown': 0.5
        }
        return tech_scores.get(tech_stack.lower(), 0.5)

    def _score_competitive(self, vendor: str) -> float:
        """Score based on competitive displacement opportunity (0-1)."""
        if vendor in self.displacement_targets:
            return 0.9  # High opportunity
        elif vendor in ['Q2', 'Alkami']:
            return 0.4  # Modern competitor, harder to displace
        elif vendor == 'Temenos':
            return 0.5
        else:
            return 0.6  # Unknown or other

    def _score_region(self, region: str) -> float:
        """Score based on regional presence (0-1)."""
        if region in self.target_regions:
            return 1.0
        else:
            return 0.5

    def _get_asset_tier(self, assets: float) -> str:
        """Get asset tier label."""
        tiers = self.config.get('asset_tiers', {})

        if assets >= 10_000_000_000:
            return tiers.get('tier_1', {}).get('label', '$10B+')
        elif assets >= 1_000_000_000:
            return tiers.get('tier_2', {}).get('label', '$1B-$10B')
        elif assets >= 500_000_000:
            return tiers.get('tier_3', {}).get('label', '$500M-$1B')
        elif assets >= 100_000_000:
            return tiers.get('tier_4', {}).get('label', '$100M-$500M')
        else:
            return tiers.get('tier_5', {}).get('label', '<$100M')

    def score_all(self, institutions: List[Dict]) -> List[Dict]:
        """
        Score all institutions and return sorted list.

        Args:
            institutions: List of institution dictionaries

        Returns:
            List of scored institutions, sorted by score descending
        """
        scored = []
        for fi in institutions:
            result = self.score_account(fi)
            scored.append({
                **fi,
                'score': result['total_score'],
                'grade': result['grade'],
                'breakdown': result['breakdown'],
                'asset_tier': result['asset_tier']
            })

        return sorted(scored, key=lambda x: x['score'], reverse=True)
