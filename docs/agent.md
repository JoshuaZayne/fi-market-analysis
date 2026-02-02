# FI Market Analysis Agent Documentation

## Overview

The FI Market Analysis Agent (`src/agent.py`) provides a reusable interface for automating market analysis operations. It can be integrated with AI assistants, automation tools, or custom applications.

## Quick Start

```python
from agent import FIMarketAgent, create_agent

# Create an agent
agent = create_agent()

# Load data
institutions = agent.load_data("config")

# Score all accounts
scored = agent.score_accounts()

# Get top 20 accounts
top_accounts = agent.get_top_accounts(20)

# Segment the market
segments = agent.segment_market("region")

# Analyze competition
competitive = agent.analyze_competitive_landscape()

# Generate visualization
chart_path = agent.generate_chart("competitive")
```

## Capabilities

| Capability | Method | Description |
|------------|--------|-------------|
| Load Data | `load_data()` | Load FI data from config or CSV |
| Score Accounts | `score_accounts()` | Score all institutions |
| Get Top Accounts | `get_top_accounts(n)` | Get top N scored accounts |
| Segment Market | `segment_market(by)` | Segment by dimension |
| Competitive Analysis | `analyze_competitive_landscape()` | Analyze competitors |
| Pipeline Estimation | `estimate_pipeline_value()` | Estimate total pipeline |
| Visualization | `generate_chart(type)` | Generate Plotly charts |

## Filtering

Apply filters when scoring:

```python
scored = agent.score_accounts(filters={
    "region": "Mountain",
    "type": "credit_union",
    "min_assets": 500000000
})
```

## Segmentation Options

```python
# By asset tier
agent.segment_market("asset_tier")

# By FI type
agent.segment_market("type")

# By region
agent.segment_market("region")

# By current vendor
agent.segment_market("vendor")
```

## Chart Types

```python
# Competitive landscape bubble chart
agent.generate_chart("competitive")

# Score distribution histogram
agent.generate_chart("scoring")

# Pipeline by segment
agent.generate_chart("pipeline")

# Market segments sunburst
agent.generate_chart("segments")
```

## Context Management

```python
# Get current context
context = agent.get_context()
# Returns: {"data_loaded": True, "scored": True, "filters": {}, ...}

# Reset for new analysis
agent.reset()
```

## Agent Metadata

```python
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
    ]
}
```

## Integration Example

```python
# Automated weekly report
agent = create_agent()
agent.load_data("config")

# Score and prioritize
agent.score_accounts(filters={"region": "Mountain"})
top_accounts = agent.get_top_accounts(50)

# Generate pipeline estimate
pipeline = agent.estimate_pipeline_value(top_accounts)
print(f"Total Pipeline: ${pipeline['total_value']:,}")

# Generate charts
agent.generate_chart("competitive", "output/competitive.html")
agent.generate_chart("scoring", "output/scoring.html")
```
