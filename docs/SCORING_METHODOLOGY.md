# Account Scoring Methodology

## Overview

The account scoring system evaluates financial institutions on a 0-100 scale to prioritize sales targeting efforts. The methodology combines multiple factors weighted by their importance to deal success.

## Scoring Factors

### 1. Asset Size (25% weight)

Larger institutions typically represent higher deal values and strategic importance.

| Asset Range | Score | Rationale |
|-------------|-------|-----------|
| $10B+ | 100 | Enterprise accounts, highest ACV |
| $5B-$10B | 90 | Large regional, significant value |
| $1B-$5B | 80 | Mid-size regional, good fit |
| $500M-$1B | 60 | Community banks, solid opportunities |
| $100M-$500M | 40 | Smaller community, lower ACV |
| <$100M | 20 | Small FIs, limited potential |

### 2. Technology Fit (30% weight)

Modern technology stacks indicate easier integration and higher likelihood of adoption.

| Tech Stack | Score | Rationale |
|------------|-------|-----------|
| Modern | 100 | Cloud-native, API-ready |
| Mixed | 70 | Partially modernized |
| Legacy | 40 | Requires more work |
| Unknown | 50 | Default assumption |

### 3. Competitive Opportunity (25% weight)

Legacy vendors present displacement opportunities.

| Current Vendor | Score | Rationale |
|----------------|-------|-----------|
| FIS, Fiserv, NCR, Jack Henry | 90 | Legacy systems, displacement opportunity |
| Temenos | 50 | Moderate difficulty |
| Q2, Alkami | 40 | Modern competitors, harder to displace |
| Other/Unknown | 60 | Varies |

### 4. Regional Presence (20% weight)

Target regions where we have strong go-to-market presence.

| Region | Score | Rationale |
|--------|-------|-----------|
| Mountain, West, Southwest | 100 | Core target markets |
| Other | 50 | Secondary markets |

## Score Calculation

```
Total Score = (Asset Score × 0.25) +
              (Tech Score × 0.30) +
              (Competitive Score × 0.25) +
              (Regional Score × 0.20)
```

## Grade Classification

| Score Range | Grade | Action |
|-------------|-------|--------|
| 80-100 | HOT | Prioritize for immediate outreach |
| 60-79 | WARM | Include in active pipeline |
| 40-59 | DEVELOPING | Nurture with content |
| 0-39 | COLD | Long-term opportunity |

## Deal Value Estimation

Estimated deal value by asset tier:

| Tier | Asset Range | Est. Annual Value |
|------|-------------|-------------------|
| 1 | $10B+ | $500,000 |
| 2 | $1B-$10B | $250,000 |
| 3 | $500M-$1B | $150,000 |
| 4 | $100M-$500M | $75,000 |
| 5 | <$100M | $35,000 |

## Priority Score

The final prioritization combines account score with estimated deal value:

```
Priority Score = (Account Score × 0.6) + (Deal Value / 10000 × 0.4)
```

This ensures we balance quality (score) with potential revenue (deal value).

## Usage in Sales Process

1. **Territory Planning**: Use scores to allocate accounts across territories
2. **Campaign Targeting**: Target HOT and WARM accounts for outbound campaigns
3. **Pipeline Management**: Track progression of scored accounts
4. **Forecasting**: Use deal value estimates for pipeline forecasting

## Customization

Weights and thresholds can be adjusted in `config/config.json`:

```json
{
    "scoring_weights": {
        "asset_size": 0.25,
        "technology_fit": 0.30,
        "competitive_opportunity": 0.25,
        "regional_presence": 0.20
    },
    "score_thresholds": {
        "hot": 80,
        "warm": 60,
        "developing": 40
    }
}
```
