"""
Chart Generator
===============

Generate interactive Plotly visualizations for FI analysis.
"""

from typing import List, Dict, Any
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict


class ChartGenerator:
    """Generate interactive charts for FI market analysis."""

    def __init__(self):
        self.colors = {
            'primary': '#1F4E79',
            'secondary': '#2E75B6',
            'hot': '#28a745',
            'warm': '#ffc107',
            'cold': '#dc3545',
            'neutral': '#6c757d'
        }

    def competitive_landscape(self, institutions: List[Dict]) -> go.Figure:
        """
        Create competitive landscape bubble chart.

        X-axis: Asset size
        Y-axis: Count by vendor
        Bubble size: Total assets
        Color: Vendor
        """
        vendor_data = defaultdict(lambda: {'count': 0, 'total_assets': 0, 'institutions': []})

        for fi in institutions:
            vendor = fi.get('current_vendor', 'Other')
            vendor_data[vendor]['count'] += 1
            vendor_data[vendor]['total_assets'] += fi.get('assets', 0)
            vendor_data[vendor]['institutions'].append(fi['name'])

        vendors = list(vendor_data.keys())
        counts = [vendor_data[v]['count'] for v in vendors]
        assets = [vendor_data[v]['total_assets'] / 1e9 for v in vendors]  # In billions
        avg_assets = [vendor_data[v]['total_assets'] / vendor_data[v]['count'] / 1e6 for v in vendors]  # In millions

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=avg_assets,
            y=counts,
            mode='markers+text',
            marker=dict(
                size=[max(10, a * 2) for a in assets],  # Size based on total assets
                color=list(range(len(vendors))),
                colorscale='Viridis',
                showscale=False
            ),
            text=vendors,
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>' +
                          'Avg Assets: $%{x:.0f}M<br>' +
                          'Count: %{y}<br>' +
                          '<extra></extra>'
        ))

        fig.update_layout(
            title='Competitive Landscape',
            xaxis_title='Average Assets per FI ($M)',
            yaxis_title='Number of Institutions',
            showlegend=False,
            height=500
        )

        return fig

    def scoring_distribution(self, institutions: List[Dict]) -> go.Figure:
        """
        Create scoring distribution histogram.
        """
        from analysis.scoring import AccountScorer
        scorer = AccountScorer()

        scores = []
        grades = []

        for fi in institutions:
            if 'score' in fi:
                scores.append(fi['score'])
                grades.append(fi.get('grade', 'UNKNOWN'))
            else:
                result = scorer.score_account(fi)
                scores.append(result['total_score'])
                grades.append(result['grade'])

        fig = go.Figure()

        # Create histogram with color by grade
        colors = [self.colors['hot'] if g == 'HOT' else
                  self.colors['warm'] if g == 'WARM' else
                  self.colors['cold'] for g in grades]

        fig.add_trace(go.Histogram(
            x=scores,
            nbinsx=20,
            marker_color=self.colors['primary'],
            opacity=0.7
        ))

        # Add threshold lines
        fig.add_vline(x=80, line_dash="dash", line_color=self.colors['hot'],
                      annotation_text="HOT (80+)")
        fig.add_vline(x=60, line_dash="dash", line_color=self.colors['warm'],
                      annotation_text="WARM (60+)")

        fig.update_layout(
            title='Account Score Distribution',
            xaxis_title='Score',
            yaxis_title='Number of Accounts',
            height=400
        )

        return fig

    def pipeline_by_segment(self, institutions: List[Dict]) -> go.Figure:
        """
        Create pipeline value by segment bar chart.
        """
        from analysis.scoring import AccountScorer
        from targeting.prioritization import AccountPrioritization

        scorer = AccountScorer()
        prioritizer = AccountPrioritization()

        # Score and estimate values
        data_by_region = defaultdict(lambda: {'hot': 0, 'warm': 0, 'other': 0})

        for fi in institutions:
            region = fi.get('region', 'Unknown')
            result = scorer.score_account(fi)
            value = prioritizer._estimate_deal_value(fi.get('assets', 0))

            if result['grade'] == 'HOT':
                data_by_region[region]['hot'] += value
            elif result['grade'] == 'WARM':
                data_by_region[region]['warm'] += value
            else:
                data_by_region[region]['other'] += value

        regions = list(data_by_region.keys())

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='HOT',
            x=regions,
            y=[data_by_region[r]['hot'] / 1000 for r in regions],
            marker_color=self.colors['hot']
        ))

        fig.add_trace(go.Bar(
            name='WARM',
            x=regions,
            y=[data_by_region[r]['warm'] / 1000 for r in regions],
            marker_color=self.colors['warm']
        ))

        fig.add_trace(go.Bar(
            name='OTHER',
            x=regions,
            y=[data_by_region[r]['other'] / 1000 for r in regions],
            marker_color=self.colors['neutral']
        ))

        fig.update_layout(
            title='Pipeline Value by Region ($K)',
            xaxis_title='Region',
            yaxis_title='Pipeline Value ($K)',
            barmode='stack',
            height=450
        )

        return fig

    def market_segments(self, institutions: List[Dict]) -> go.Figure:
        """
        Create market segmentation pie/sunburst chart.
        """
        # Segment by type and region
        segments = []

        for fi in institutions:
            segments.append({
                'type': 'Bank' if fi.get('type') == 'bank' else 'Credit Union',
                'region': fi.get('region', 'Unknown'),
                'assets': fi.get('assets', 0)
            })

        # Create sunburst
        labels = []
        parents = []
        values = []

        # Root
        type_totals = defaultdict(int)
        region_totals = defaultdict(lambda: defaultdict(int))

        for s in segments:
            type_totals[s['type']] += s['assets']
            region_totals[s['type']][s['region']] += s['assets']

        # Add type level
        for fi_type, total in type_totals.items():
            labels.append(fi_type)
            parents.append('')
            values.append(total / 1e9)

            # Add region level
            for region, region_total in region_totals[fi_type].items():
                labels.append(f"{fi_type} - {region}")
                parents.append(fi_type)
                values.append(region_total / 1e9)

        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            branchvalues='total'
        ))

        fig.update_layout(
            title='Market Segments by Type and Region (Assets in $B)',
            height=500
        )

        return fig

    def vendor_market_share(self, institutions: List[Dict]) -> go.Figure:
        """
        Create vendor market share pie chart.
        """
        vendor_counts = defaultdict(int)

        for fi in institutions:
            vendor = fi.get('current_vendor', 'Other')
            vendor_counts[vendor] += 1

        fig = go.Figure(go.Pie(
            labels=list(vendor_counts.keys()),
            values=list(vendor_counts.values()),
            hole=0.3
        ))

        fig.update_layout(
            title='Market Share by Vendor',
            height=450
        )

        return fig
