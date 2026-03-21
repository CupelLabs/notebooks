# FOIA Response Times Analysis

Analysis behind ["The Federal FOIA Backlog Doubled. The Grant Rate Hit an All-Time Low."](https://cupellabs.veron3.space/foia-backlog-doubled-grant-rate-all-time-low)

## Data source

FOIA.gov annual report CSV files, FY2018-FY2024. Downloaded from https://www.foia.gov/foia-dataset-download.html on 2026-03-21.

Each fiscal year has 32 CSV files covering processing times, backlogs, exemptions, dispositions, staffing, and costs across 118-123 federal agencies.

## Reproduce

```bash
# 1. Download the raw data (or use the copies in data/raw/)
for year in 2018 2019 2020 2021 2022 2023 2024; do
  wget "https://www.foia.gov/downloads/all_agencies_csv_${year}.zip"
  unzip "all_agencies_csv_${year}.zip" -d "csv_${year}"
done

# 2. Run the analysis
python scripts/analyze_foia.py
```

## Directory structure

```
scripts/analyze_foia.py     — main analysis script (produces all findings)
findings.md                 — structured findings with cross-checks
data/raw/                   — original FOIA.gov CSV downloads (FY2018-FY2024)
data/*.csv                  — intermediate computed aggregations (28 files)
```

## Key findings

- Federal FOIA backlog doubled: 130,718 (FY2018) to 267,056 (FY2024)
- Full grant rate hit all-time low: 12.1%, down from 26.9%
- DHS owns 53% of the backlog (141,420 requests)
- Excluding DHS, backlog still grew 64% and grant rate still fell to 23.5%
- $723M/year in FOIA operations ($669M processing + $54M litigation)
- 24 agencies have requests older than 5 years; 4 over 10 years

All data is self-reported by the agencies. No independent audit exists.
