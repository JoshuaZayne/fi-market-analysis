"""
Account Prioritization
======================

Prioritize accounts for sales targeting.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class AccountPrioritization:
    """
    Prioritize financial institution accounts for targeting.

    Combines scoring with deal value estimation.
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the prioritizer."""
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "config.json"

        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.deal_sizes = self.config.get('average_deal_size_by_tier', {
            'tier_1': 500000,
            'tier_2': 250000,
            'tier_3': 150000,
            'tier_4': 75000,
            'tier_5': 35000
        })

    def prioritize(self, institutions: List[Dict], top_n: int = 20) -> List[Dict]:
        """
        Prioritize institutions for targeting.

        Args:
            institutions: List of institutions (should include scores)
            top_n: Number of top accounts to return

        Returns:
            List of prioritized accounts with estimated values
        """
        from analysis.scoring import AccountScorer
        scorer = AccountScorer()

        prioritized = []
        for fi in institutions:
            # Get score if not already scored
            if 'score' not in fi:
                result = scorer.score_account(fi)
                score = result['total_score']
                grade = result['grade']
                asset_tier = result['asset_tier']
            else:
                score = fi['score']
                grade = fi.get('grade', 'UNKNOWN')
                asset_tier = fi.get('asset_tier', self._get_tier(fi.get('assets', 0)))

            # Estimate deal value
            estimated_value = self._estimate_deal_value(fi.get('assets', 0))

            # Calculate priority score (combining score and value)
            priority_score = score * 0.6 + (estimated_value / 10000) * 0.4

            prioritized.append({
                'name': fi['name'],
                'type': fi.get('type', 'unknown'),
                'assets': fi.get('assets', 0),
                'region': fi.get('region', 'Unknown'),
                'current_vendor': fi.get('current_vendor', 'Unknown'),
                'score': score,
                'grade': grade,
                'asset_tier': asset_tier,
                'estimated_value': estimated_value,
                'priority_score': priority_score
            })

        # Sort by priority score
        prioritized.sort(key=lambda x: x['priority_score'], reverse=True)

        return prioritized[:top_n]

    def _estimate_deal_value(self, assets: float) -> int:
        """Estimate deal value based on asset size."""
        if assets >= 10_000_000_000:
            return self.deal_sizes.get('tier_1', 500000)
        elif assets >= 1_000_000_000:
            return self.deal_sizes.get('tier_2', 250000)
        elif assets >= 500_000_000:
            return self.deal_sizes.get('tier_3', 150000)
        elif assets >= 100_000_000:
            return self.deal_sizes.get('tier_4', 75000)
        else:
            return self.deal_sizes.get('tier_5', 35000)

    def _get_tier(self, assets: float) -> str:
        """Get tier label for assets."""
        if assets >= 10_000_000_000:
            return '$10B+'
        elif assets >= 1_000_000_000:
            return '$1B-$10B'
        elif assets >= 500_000_000:
            return '$500M-$1B'
        elif assets >= 100_000_000:
            return '$100M-$500M'
        else:
            return '<$100M'

    def estimate_pipeline(self, accounts: List[Dict]) -> Dict[str, Any]:
        """
        Estimate total pipeline value.

        Args:
            accounts: List of prioritized accounts

        Returns:
            Pipeline estimates
        """
        total_value = sum(a.get('estimated_value', 0) for a in accounts)

        by_grade = {}
        for grade in ['HOT', 'WARM', 'DEVELOPING', 'COLD']:
            grade_accounts = [a for a in accounts if a.get('grade') == grade]
            by_grade[grade] = {
                'count': len(grade_accounts),
                'value': sum(a.get('estimated_value', 0) for a in grade_accounts)
            }

        by_region = {}
        for a in accounts:
            region = a.get('region', 'Unknown')
            if region not in by_region:
                by_region[region] = {'count': 0, 'value': 0}
            by_region[region]['count'] += 1
            by_region[region]['value'] += a.get('estimated_value', 0)

        return {
            'total_accounts': len(accounts),
            'total_value': total_value,
            'by_grade': by_grade,
            'by_region': by_region,
            'avg_deal_size': total_value / len(accounts) if accounts else 0
        }

    def assign_territories(
        self,
        accounts: List[Dict],
        territories: Dict[str, List[str]]
    ) -> Dict[str, List[Dict]]:
        """
        Assign accounts to sales territories.

        Args:
            accounts: List of accounts
            territories: Dict mapping territory name to regions

        Returns:
            Accounts grouped by territory
        """
        assignments = {t: [] for t in territories}
        unassigned = []

        for account in accounts:
            region = account.get('region', 'Unknown')
            assigned = False

            for territory, regions in territories.items():
                if region in regions:
                    assignments[territory].append(account)
                    assigned = True
                    break

            if not assigned:
                unassigned.append(account)

        if unassigned:
            assignments['Unassigned'] = unassigned

        return assignments
