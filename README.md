# Financial Institution Market Analysis

A Python-based competitive landscape analysis and account targeting framework for regional FI prospects.

## Features

- **FI Data Management**: Load and manage financial institution data
- **Competitive Analysis**: Map competitive landscape and positioning
- **Account Scoring**: Score accounts 1-100 based on multiple criteria
- **Market Segmentation**: Segment by asset tier, FI type, and region
- **Account Prioritization**: Rank accounts by score and deal value
- **Visualization**: Interactive Plotly charts for analysis

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Load FI data from CSV
python src/main.py load --file data/sample_fi_list.csv

# Score all accounts
python src/main.py score --all

# Segment by asset tier
python src/main.py segment --by asset_tier

# Get top 20 prioritized accounts
python src/main.py prioritize --top 20

# Generate competitive landscape chart
python src/main.py visualize --chart competitive

# Export analysis to HTML
python src/main.py export --format html
```

## Project Structure

```
fi-market-analysis/
├── README.md
├── requirements.txt
├── config/
│   ├── config.json
│   └── fi_database.json
├── src/
│   ├── main.py
│   ├── agent.py                   # Reusable agent configuration
│   ├── data/
│   │   ├── fi_loader.py
│   │   └── market_data.py
│   ├── analysis/
│   │   ├── competitive.py
│   │   ├── scoring.py
│   │   └── segmentation.py
│   ├── targeting/
│   │   └── prioritization.py
│   └── visualization/
│       └── charts.py
├── data/
│   └── sample_fi_list.csv
├── docs/
│   ├── SCORING_METHODOLOGY.md
│   └── agent.md
└── output/
```

## Account Scoring Algorithm

Accounts are scored 1-100 based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| Asset Size | 25% | Larger FIs = higher score |
| Technology Fit | 30% | Compatibility with current tech |
| Competitive Opportunity | 25% | Displacement potential |
| Regional Presence | 20% | Geographic alignment |

### Score Classification

| Score Range | Classification | Action |
|-------------|---------------|--------|
| 80-100 | HOT | Prioritize for immediate outreach |
| 60-79 | WARM | Include in active pipeline |
| 40-59 | DEVELOPING | Nurture with content |
| 0-39 | COLD | Long-term opportunity |

## Competitive Landscape

Tracks major competitors:
- FIS
- Fiserv
- Jack Henry
- NCR
- Temenos
- Q2
- Alkami

## Requirements

- Python 3.8+
- pandas
- plotly
- click

## License

MIT License
