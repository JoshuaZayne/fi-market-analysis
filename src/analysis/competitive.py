"""
Competitive Analysis
====================

Analyze competitive landscape in the FI market.
"""

from typing import Dict, List, Any
from collections import defaultdict


class CompetitiveAnalysis:
    """
    Analyze competitive positioning in the FI market.

    Tracks:
    - Market share by vendor
    - Competitive strengths/weaknesses
    - Displacement opportunities
    """

    def __init__(self):
        self.competitors = {
            'FIS': {
                'type': 'legacy',
                'strengths': ['Market leader', 'Full suite', 'Enterprise focus'],
                'weaknesses': ['Legacy technology', 'Slow innovation', 'Complex pricing'],
                'displacement_difficulty': 'medium'
            },
            'Fiserv': {
                'type': 'legacy',
                'strengths': ['Large install base', 'Broad product line'],
                'weaknesses': ['Integration challenges', 'User experience'],
                'displacement_difficulty': 'medium'
            },
            'Jack Henry': {
                'type': 'legacy',
                'strengths': ['Community bank focus', 'Service quality'],
                'weaknesses': ['Limited innovation', 'Smaller scale'],
                'displacement_difficulty': 'medium'
            },
            'NCR': {
                'type': 'legacy',
                'strengths': ['ATM integration', 'Hardware bundle'],
                'weaknesses': ['Software focus secondary', 'Aging platform'],
                'displacement_difficulty': 'low'
            },
            'Q2': {
                'type': 'modern',
                'strengths': ['Modern platform', 'Good UX', 'API-first'],
                'weaknesses': ['Smaller market share', 'Enterprise gaps'],
                'displacement_difficulty': 'high'
            },
            'Alkami': {
                'type': 'modern',
                'strengths': ['Cloud-native', 'CU focus', 'Modern UX'],
                'weaknesses': ['Newer entrant', 'Scale limitations'],
                'displacement_difficulty': 'high'
            },
            'Temenos': {
                'type': 'modern',
                'strengths': ['Global presence', 'Core banking'],
                'weaknesses': ['Implementation complexity', 'US market'],
                'displacement_difficulty': 'medium'
            }
        }

    def analyze(self, institutions: List[Dict]) -> Dict[str, Any]:
        """
        Analyze competitive landscape for a set of institutions.

        Args:
            institutions: List of institutions

        Returns:
            Competitive analysis results
        """
        vendor_share = self._calculate_market_share(institutions)
        opportunities = self._identify_opportunities(institutions)
        positioning = self._competitive_positioning(institutions)

        return {
            'market_share': vendor_share,
            'opportunities': opportunities,
            'positioning': positioning,
            'total_institutions': len(institutions)
        }

    def _calculate_market_share(self, institutions: List[Dict]) -> Dict[str, Dict]:
        """Calculate market share by vendor."""
        share = defaultdict(lambda: {'count': 0, 'assets': 0})

        for fi in institutions:
            vendor = fi.get('current_vendor', 'Other')
            share[vendor]['count'] += 1
            share[vendor]['assets'] += fi.get('assets', 0)

        total_count = len(institutions)
        total_assets = sum(fi.get('assets', 0) for fi in institutions)

        for vendor in share:
            share[vendor]['count_share'] = share[vendor]['count'] / total_count if total_count > 0 else 0
            share[vendor]['asset_share'] = share[vendor]['assets'] / total_assets if total_assets > 0 else 0

        return dict(share)

    def _identify_opportunities(self, institutions: List[Dict]) -> Dict[str, List[str]]:
        """Identify displacement opportunities."""
        opportunities = {
            'high': [],
            'medium': [],
            'low': []
        }

        for fi in institutions:
            vendor = fi.get('current_vendor', 'Other')
            competitor = self.competitors.get(vendor, {})
            difficulty = competitor.get('displacement_difficulty', 'medium')

            if difficulty == 'low':
                opportunities['high'].append(fi['name'])
            elif difficulty == 'medium':
                opportunities['medium'].append(fi['name'])
            else:
                opportunities['low'].append(fi['name'])

        return opportunities

    def _competitive_positioning(self, institutions: List[Dict]) -> Dict[str, Dict]:
        """Analyze positioning by competitor."""
        positioning = {}

        for vendor, info in self.competitors.items():
            vendor_fis = [fi for fi in institutions if fi.get('current_vendor') == vendor]

            positioning[vendor] = {
                'type': info['type'],
                'count': len(vendor_fis),
                'total_assets': sum(fi.get('assets', 0) for fi in vendor_fis),
                'strengths': info['strengths'],
                'weaknesses': info['weaknesses'],
                'displacement_difficulty': info['displacement_difficulty']
            }

        return positioning

    def get_competitor_info(self, vendor: str) -> Dict:
        """Get detailed info on a competitor."""
        return self.competitors.get(vendor, {
            'type': 'unknown',
            'strengths': [],
            'weaknesses': [],
            'displacement_difficulty': 'unknown'
        })

    def win_loss_analysis(self, wins: List[Dict], losses: List[Dict]) -> Dict:
        """
        Analyze win/loss patterns by competitor.

        Args:
            wins: List of won deals
            losses: List of lost deals

        Returns:
            Win/loss analysis by competitor
        """
        analysis = defaultdict(lambda: {'wins': 0, 'losses': 0, 'win_rate': 0})

        for deal in wins:
            competitor = deal.get('competitor', 'Unknown')
            analysis[competitor]['wins'] += 1

        for deal in losses:
            competitor = deal.get('competitor', 'Unknown')
            analysis[competitor]['losses'] += 1

        for competitor in analysis:
            total = analysis[competitor]['wins'] + analysis[competitor]['losses']
            if total > 0:
                analysis[competitor]['win_rate'] = analysis[competitor]['wins'] / total

        return dict(analysis)
