# R&D vs Capital Expenditure: Big Tech's Spending Inversion

Analysis behind the Cupel Labs article: **"Big Tech Spends More on Buildings Than Research"**

## What this shows

Three of the four largest tech companies (Microsoft, Alphabet, Meta) now spend more on capital expenditure than on R&D. Apple went the opposite direction. The crossover accelerated in 2024-2025, driven by the AI infrastructure buildout.

## Data source

SEC EDGAR XBRL API. No API key required. All data from 10-K annual filings.

- `ResearchAndDevelopmentExpense` (R&D)
- `PaymentsToAcquirePropertyPlantAndEquipment` (CapEx)

Companies: Microsoft (CIK 0000789019), Alphabet (CIK 0001652044), Meta (CIK 0001326801), Apple (CIK 0000320193).

Amazon excluded: does not report R&D as a standard XBRL line item. NVIDIA excluded: fabless semiconductor, capex not material.

## Reproduce

```bash
python3 fetch_edgar.py    # Downloads from SEC EDGAR, saves to data/
python3 analyze.py        # Computes ratios and growth rates, prints findings
```

Requires Python 3.8+. No external dependencies (uses only stdlib).

## Files

- `fetch_edgar.py` — Downloads company facts from SEC EDGAR XBRL API, extracts R&D and capex from 10-K filings
- `analyze.py` — Computes capex/R&D ratios, growth rates, crossover years
- `findings.md` — Full findings with tables and analysis
- `data/rd_vs_capex.csv` — Raw extracted data (company, year, R&D, capex, revenue)
- `data/analysis.csv` — Computed ratios and growth metrics
- `data/chart_data.json` — Chart-ready data by company

## Key findings

| Company   | 2020 CapEx/R&D | 2025 CapEx/R&D | Crossover |
|-----------|---------------|---------------|-----------|
| Microsoft | 0.80          | 1.99          | ~2021     |
| Alphabet  | 0.81          | 1.50          | 2024      |
| Meta      | 0.82          | 1.21          | 2025      |
| Apple     | 0.39          | 0.37          | Never     |
