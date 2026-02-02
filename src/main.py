"""
Financial Institution Market Analysis - CLI Interface
=====================================================

Command-line interface for FI market analysis tools.
"""

import click
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from data.fi_loader import FILoader
from analysis.scoring import AccountScorer
from analysis.segmentation import MarketSegmentation
from analysis.competitive import CompetitiveAnalysis
from targeting.prioritization import AccountPrioritization
from visualization.charts import ChartGenerator


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Financial Institution Market Analysis - Account targeting and competitive analysis."""
    pass


@cli.command()
@click.option('--file', '-f', type=str, help='Path to CSV file with FI data')
@click.option('--from-config', is_flag=True, help='Load from config/fi_database.json')
def load(file: str, from_config: bool):
    """Load financial institution data."""
    loader = FILoader()

    if from_config:
        institutions = loader.load_from_config()
        source = "config/fi_database.json"
    elif file:
        institutions = loader.load_from_csv(file)
        source = file
    else:
        click.echo("Error: Specify --file or --from-config")
        return

    click.echo(f"\nLoaded {len(institutions)} financial institutions from {source}")
    click.echo(f"\nSummary:")
    click.echo(f"  Banks: {sum(1 for fi in institutions if fi.get('type') == 'bank')}")
    click.echo(f"  Credit Unions: {sum(1 for fi in institutions if fi.get('type') == 'credit_union')}")

    total_assets = sum(fi.get('assets', 0) for fi in institutions)
    click.echo(f"  Total Assets: ${total_assets/1e9:.1f}B")


@cli.command()
@click.option('--all', 'score_all', is_flag=True, help='Score all accounts')
@click.option('--name', '-n', type=str, help='Score specific institution by name')
def score(score_all: bool, name: str):
    """Score accounts based on targeting criteria."""
    loader = FILoader()
    institutions = loader.load_from_config()
    scorer = AccountScorer()

    if name:
        fi = next((f for f in institutions if name.lower() in f['name'].lower()), None)
        if fi:
            result = scorer.score_account(fi)
            _print_score_result(fi['name'], result)
        else:
            click.echo(f"Institution not found: {name}")
        return

    if score_all:
        click.echo(f"\n{'='*70}")
        click.echo("ACCOUNT SCORING RESULTS")
        click.echo(f"{'='*70}\n")

        results = []
        for fi in institutions:
            result = scorer.score_account(fi)
            results.append((fi['name'], result))

        # Sort by score descending
        results.sort(key=lambda x: x[1]['total_score'], reverse=True)

        click.echo(f"{'Institution':<35} {'Score':>8} {'Grade':>12} {'Tier':>10}")
        click.echo("-" * 70)

        for name, result in results:
            click.echo(f"{name:<35} {result['total_score']:>8.1f} {result['grade']:>12} {result['asset_tier']:>10}")

        # Summary
        hot = sum(1 for _, r in results if r['grade'] == 'HOT')
        warm = sum(1 for _, r in results if r['grade'] == 'WARM')
        click.echo(f"\nSummary: {hot} HOT, {warm} WARM, {len(results) - hot - warm} OTHER")


def _print_score_result(name: str, result: dict):
    """Print detailed score result."""
    click.echo(f"\n{'='*50}")
    click.echo(f"SCORE: {name}")
    click.echo(f"{'='*50}\n")
    click.echo(f"Total Score: {result['total_score']:.1f}/100")
    click.echo(f"Grade: {result['grade']}")
    click.echo(f"\nBreakdown:")
    for factor, score in result['breakdown'].items():
        click.echo(f"  {factor}: {score:.1f}")


@cli.command()
@click.option('--by', '-b', type=click.Choice(['asset_tier', 'type', 'region', 'vendor']),
              required=True, help='Segmentation dimension')
def segment(by: str):
    """Segment the market by a dimension."""
    loader = FILoader()
    institutions = loader.load_from_config()
    segmentation = MarketSegmentation()

    if by == 'asset_tier':
        results = segmentation.by_asset_tier(institutions)
    elif by == 'type':
        results = segmentation.by_type(institutions)
    elif by == 'region':
        results = segmentation.by_region(institutions)
    elif by == 'vendor':
        results = segmentation.by_vendor(institutions)

    click.echo(f"\n{'='*60}")
    click.echo(f"MARKET SEGMENTATION BY {by.upper()}")
    click.echo(f"{'='*60}\n")

    click.echo(f"{'Segment':<25} {'Count':>8} {'Assets ($B)':>15} {'Avg Assets ($M)':>15}")
    click.echo("-" * 65)

    for segment, data in sorted(results.items(), key=lambda x: x[1]['total_assets'], reverse=True):
        click.echo(f"{segment:<25} {data['count']:>8} {data['total_assets']/1e9:>15.1f} {data['avg_assets']/1e6:>15.1f}")


@cli.command()
@click.option('--top', '-t', type=int, default=20, help='Number of accounts to show')
@click.option('--region', '-r', type=str, help='Filter by region')
def prioritize(top: int, region: str):
    """Prioritize accounts for targeting."""
    loader = FILoader()
    institutions = loader.load_from_config()

    if region:
        institutions = [fi for fi in institutions if fi.get('region', '').lower() == region.lower()]

    prioritizer = AccountPrioritization()
    ranked = prioritizer.prioritize(institutions, top_n=top)

    click.echo(f"\n{'='*80}")
    click.echo(f"TOP {top} PRIORITIZED ACCOUNTS" + (f" - {region.upper()}" if region else ""))
    click.echo(f"{'='*80}\n")

    click.echo(f"{'Rank':<6} {'Institution':<30} {'Score':>8} {'Est. Value':>12} {'Region':>12}")
    click.echo("-" * 80)

    for i, account in enumerate(ranked, 1):
        click.echo(f"{i:<6} {account['name']:<30} {account['score']:>8.1f} ${account['estimated_value']:>10,} {account['region']:>12}")

    total_value = sum(a['estimated_value'] for a in ranked)
    click.echo(f"\nTotal Pipeline Value: ${total_value:,}")


@cli.command()
@click.option('--chart', '-c', type=click.Choice(['competitive', 'scoring', 'pipeline', 'segments']),
              required=True, help='Chart type')
@click.option('--output', '-o', type=str, default=None, help='Output file path')
def visualize(chart: str, output: str):
    """Generate visualization charts."""
    loader = FILoader()
    institutions = loader.load_from_config()
    chart_gen = ChartGenerator()

    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    if output is None:
        output = str(output_dir / f"{chart}_chart.html")

    if chart == 'competitive':
        fig = chart_gen.competitive_landscape(institutions)
    elif chart == 'scoring':
        fig = chart_gen.scoring_distribution(institutions)
    elif chart == 'pipeline':
        fig = chart_gen.pipeline_by_segment(institutions)
    elif chart == 'segments':
        fig = chart_gen.market_segments(institutions)

    fig.write_html(output)
    click.echo(f"\nChart saved to: {output}")


@cli.command()
@click.option('--format', '-f', 'fmt', type=click.Choice(['html', 'json']), default='html', help='Export format')
@click.option('--output', '-o', type=str, default=None, help='Output file path')
def export(fmt: str, output: str):
    """Export analysis to file."""
    loader = FILoader()
    institutions = loader.load_from_config()
    scorer = AccountScorer()

    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    if output is None:
        output = str(output_dir / f"fi_analysis.{fmt}")

    # Score all accounts
    scored = []
    for fi in institutions:
        result = scorer.score_account(fi)
        fi_data = fi.copy()
        fi_data['score'] = result['total_score']
        fi_data['grade'] = result['grade']
        scored.append(fi_data)

    if fmt == 'json':
        with open(output, 'w') as f:
            json.dump(scored, f, indent=2)
    else:
        # Generate HTML report
        html = _generate_html_report(scored)
        with open(output, 'w') as f:
            f.write(html)

    click.echo(f"\nExport saved to: {output}")


def _generate_html_report(data: list) -> str:
    """Generate HTML report."""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>FI Market Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #1F4E79; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #1F4E79; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .hot { background-color: #d4edda; }
        .warm { background-color: #fff3cd; }
    </style>
</head>
<body>
    <h1>Financial Institution Market Analysis</h1>
    <table>
        <tr>
            <th>Institution</th>
            <th>Type</th>
            <th>Assets</th>
            <th>Region</th>
            <th>Current Vendor</th>
            <th>Score</th>
            <th>Grade</th>
        </tr>
"""
    for fi in sorted(data, key=lambda x: x['score'], reverse=True):
        grade_class = 'hot' if fi['grade'] == 'HOT' else ('warm' if fi['grade'] == 'WARM' else '')
        html += f"""        <tr class="{grade_class}">
            <td>{fi['name']}</td>
            <td>{fi['type']}</td>
            <td>${fi['assets']/1e6:.0f}M</td>
            <td>{fi['region']}</td>
            <td>{fi.get('current_vendor', 'Unknown')}</td>
            <td>{fi['score']:.1f}</td>
            <td>{fi['grade']}</td>
        </tr>
"""
    html += """    </table>
</body>
</html>"""
    return html


if __name__ == '__main__':
    cli()
