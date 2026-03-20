# CFPB Credit Reporting Relief Rate Analysis

Data and analysis behind [Experian Stopped Fixing Credit Errors](https://cupellabs.veron3.space/experian-stopped-fixing-credit-errors).

## The Finding

Experian's consumer relief rate on CFPB complaints dropped from 21.6% (2024) to 0.49% (2025). A 97.7% decline. Equifax, under a consent order, held steady at ~65%. TransUnion declined from ~87% to ~66% on a different timeline.

## Data

**Source:** [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/) (bulk download)

**Coverage:** 10.57 million credit reporting complaints, January 2020 through March 2026.

**How to get the data:**
1. Download the full database: `https://files.consumerfinance.gov/ccdb/complaints.csv.zip` (~1.7GB)
2. Unzip it (~7.8GB)
3. Filter to credit reporting products (see script)

The raw data is too large for GitHub. Download it yourself and verify.

## How to Run

```bash
# Download the data
curl -L -o complaints.csv.zip https://files.consumerfinance.gov/ccdb/complaints.csv.zip
unzip complaints.csv.zip

# Filter to credit reporting (outputs cfpb-credit-reporting-2020-2026.csv)
# Then run the analysis
python3 analyze_relief_rates.py
```

Requirements: Python 3, pandas, matplotlib. No other dependencies.

## Files

- `analyze_relief_rates.py` — full analysis script, produces all charts and summary statistics
- `findings.md` — structured findings with confidence levels and caveats
- `relief_rate_cliff_highlighted.png` — the key chart showing Experian's collapse
- `relief_rate_by_bureau.png` — all three bureaus compared
- `complaint_volume_by_bureau.png` — complaint volume context

## Verify Our Work

The entire analysis is reproducible. Download the CFPB database, run the script, compare your output to ours. If you get different numbers, open an issue.
