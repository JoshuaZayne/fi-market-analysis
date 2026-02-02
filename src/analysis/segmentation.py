"""
Market Segmentation
===================

Segment the FI market by various dimensions.
"""

from typing import Dict, List, Any
from collections import defaultdict


class MarketSegmentation:
    """
    Segment the financial institution market by various dimensions.

    Segmentation options:
    - Asset tier
    - FI type (bank vs credit union)
    - Region
    - Current vendor
    """

    def __init__(self):
        self.asset_tiers = {
            'tier_1': {'label': '$10B+', 'min': 10_000_000_000},
            'tier_2': {'label': '$1B-$10B', 'min': 1_000_000_000},
            'tier_3': {'label': '$500M-$1B', 'min': 500_000_000},
            'tier_4': {'label': '$100M-$500M', 'min': 100_000_000},
            'tier_5': {'label': '<$100M', 'min': 0}
        }

    def by_asset_tier(self, institutions: List[Dict]) -> Dict[str, Dict]:
        """
        Segment by asset tier.

        Args:
            institutions: List of institutions

        Returns:
            Dictionary with tier labels as keys
        """
        segments = defaultdict(lambda: {'count': 0, 'total_assets': 0, 'institutions': []})

        for fi in institutions:
            assets = fi.get('assets', 0)
            tier = self._get_tier(assets)
            segments[tier]['count'] += 1
            segments[tier]['total_assets'] += assets
            segments[tier]['institutions'].append(fi['name'])

        # Calculate averages
        for tier in segments:
            if segments[tier]['count'] > 0:
                segments[tier]['avg_assets'] = segments[tier]['total_assets'] / segments[tier]['count']
            else:
                segments[tier]['avg_assets'] = 0

        return dict(segments)

    def by_type(self, institutions: List[Dict]) -> Dict[str, Dict]:
        """
        Segment by FI type (bank vs credit union).

        Args:
            institutions: List of institutions

        Returns:
            Dictionary with type as keys
        """
        segments = defaultdict(lambda: {'count': 0, 'total_assets': 0, 'institutions': []})

        for fi in institutions:
            fi_type = fi.get('type', 'unknown')
            label = 'Banks' if fi_type == 'bank' else 'Credit Unions' if fi_type == 'credit_union' else 'Other'
            segments[label]['count'] += 1
            segments[label]['total_assets'] += fi.get('assets', 0)
            segments[label]['institutions'].append(fi['name'])

        for segment in segments:
            if segments[segment]['count'] > 0:
                segments[segment]['avg_assets'] = segments[segment]['total_assets'] / segments[segment]['count']

        return dict(segments)

    def by_region(self, institutions: List[Dict]) -> Dict[str, Dict]:
        """
        Segment by geographic region.

        Args:
            institutions: List of institutions

        Returns:
            Dictionary with region as keys
        """
        segments = defaultdict(lambda: {'count': 0, 'total_assets': 0, 'institutions': []})

        for fi in institutions:
            region = fi.get('region', 'Unknown')
            segments[region]['count'] += 1
            segments[region]['total_assets'] += fi.get('assets', 0)
            segments[region]['institutions'].append(fi['name'])

        for segment in segments:
            if segments[segment]['count'] > 0:
                segments[segment]['avg_assets'] = segments[segment]['total_assets'] / segments[segment]['count']

        return dict(segments)

    def by_vendor(self, institutions: List[Dict]) -> Dict[str, Dict]:
        """
        Segment by current vendor.

        Args:
            institutions: List of institutions

        Returns:
            Dictionary with vendor as keys
        """
        segments = defaultdict(lambda: {'count': 0, 'total_assets': 0, 'institutions': []})

        for fi in institutions:
            vendor = fi.get('current_vendor', 'Unknown')
            segments[vendor]['count'] += 1
            segments[vendor]['total_assets'] += fi.get('assets', 0)
            segments[vendor]['institutions'].append(fi['name'])

        for segment in segments:
            if segments[segment]['count'] > 0:
                segments[segment]['avg_assets'] = segments[segment]['total_assets'] / segments[segment]['count']

        return dict(segments)

    def _get_tier(self, assets: float) -> str:
        """Get tier label for asset amount."""
        if assets >= 10_000_000_000:
            return self.asset_tiers['tier_1']['label']
        elif assets >= 1_000_000_000:
            return self.asset_tiers['tier_2']['label']
        elif assets >= 500_000_000:
            return self.asset_tiers['tier_3']['label']
        elif assets >= 100_000_000:
            return self.asset_tiers['tier_4']['label']
        else:
            return self.asset_tiers['tier_5']['label']

    def calculate_tam_sam_som(
        self,
        institutions: List[Dict],
        target_regions: List[str],
        avg_deal_size: float = 150000
    ) -> Dict[str, Any]:
        """
        Calculate TAM, SAM, SOM estimates.

        Args:
            institutions: List of institutions (represents accessible market)
            target_regions: List of target regions for SOM
            avg_deal_size: Average deal size

        Returns:
            TAM/SAM/SOM estimates
        """
        # TAM: All US FIs (estimated)
        tam_count = 10000
        tam = tam_count * avg_deal_size

        # SAM: Institutions in our data (serviceable)
        sam_count = len(institutions)
        sam = sam_count * avg_deal_size

        # SOM: Target regions we can realistically capture
        som_institutions = [fi for fi in institutions if fi.get('region') in target_regions]
        som_count = len(som_institutions)
        som = som_count * avg_deal_size * 0.10  # 10% realistic capture

        return {
            'tam': {'count': tam_count, 'value': tam},
            'sam': {'count': sam_count, 'value': sam},
            'som': {'count': som_count, 'value': som},
            'avg_deal_size': avg_deal_size
        }
