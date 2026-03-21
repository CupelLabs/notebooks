# IRS Enforcement Collapse Analysis

Analysis behind the Cupel Labs article: "The IRS Audits the Poor More Than the Upper Middle Class"

## What this shows

IRS audit rates by income bracket collapsed between 2010 and 2022. The wealthiest brackets lost 80-98% of their audit risk. Low-income EITC filers are now audited at 7x the rate of upper-middle-income filers ($200K-$500K).

## Key findings

- $10M+ audit rate: 21.5% (2010) to 4.0% (2022), down 81%
- $200K-$500K audit rate: 2.3% to 0.1%, down 95.6%
- EITC filers: 0.7% audit rate vs 0.1% for $200K-$500K (7x ratio)
- IRS FTEs: 112,024 (1995) to 73,519 (2018), partial recovery to 90,516 (2024)
- Recommended additional tax from $1M+ audits: $1.43B (2010) to $0.29B (2022)

## Data source

IRS Data Book, published annually by the IRS Statistics of Income division.
https://www.irs.gov/statistics/soi-tax-stats-irs-data-book

- **Table 17:** Examination coverage by type and size of return (Tax Years 2010-2022)
- **Table 33:** Collections, costs, personnel, and U.S. population (FY 1995-2024)

All data downloaded 2026-03-21.

## How to reproduce

```bash
pip install openpyxl pandas
python scripts/analyze_audits.py
```

The script reads Excel files from `data/` and outputs:
- `data/audit_rates_by_bracket_2010_2022.csv` - Full audit rate dataset
- `data/audit_rates_key_brackets_pivot.csv` - Pivot table for charting
- `data/audit_rates_latest_by_bracket.csv` - 2022 snapshot
- `data/irs_staffing_efficiency.csv` - 30-year staffing time series
- `data/chart_data.json` - Pre-formatted for interactive charts

## File structure

```
scripts/analyze_audits.py          - Analysis script (Python 3, pandas, openpyxl)
findings.md                        - Structured findings with confidence levels
data/README.md                     - Data dictionary and source documentation
data/*.xlsx                        - Raw IRS Data Book Excel tables
data/*.csv                         - Computed intermediate data
data/chart_data.json               - Chart-ready JSON
```
