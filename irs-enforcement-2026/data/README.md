# IRS Enforcement Data — Raw Files

Downloaded 2026-03-21 from IRS Statistics of Income (SOI) Data Book publications.

## Primary Source

IRS Data Book: https://www.irs.gov/statistics/soi-tax-stats-irs-data-book

All files are official IRS Excel tables from the FY2020–FY2024 Data Books.

## Files

### Examination / Audit Coverage (core dataset)

| File | Source | Coverage | Description |
|------|--------|----------|-------------|
| `table17_exam_coverage_all_years_2010_2021_revised.xlsx` | FY2023 Data Book (revised) | Tax Years 2010–2021 | **Primary file.** Examination coverage and recommended additional tax, by type and size of return. Includes individual returns broken down by total positive income brackets ($1–$25K, $25K–$50K, ... $10M+). Has returns filed, returns examined (closed + in process), percentage covered, no-change count, and recommended additional tax. 12 tax years in one file. |
| `table17_exam_coverage_2024db.xlsx` | FY2024 Data Book | Tax Years 2014–2022 | Same structure. Adds Tax Year 2022 data not in the revised file above. |
| `table17_exam_coverage_22db.xlsx` | FY2022 Data Book | Tax Years 2012–2020 | Earlier Data Book version of Table 17. |
| `table17_exam_coverage_21db.xlsx` | FY2021 Data Book | Tax Years 2011–2019 | Earlier Data Book version of Table 17. |
| `table17_exam_coverage_20db.xlsx` | FY2020 Data Book | Tax Years 2010–2018 | Earlier Data Book version of Table 17. |
| `table18_exam_results_2024db.xlsx` | FY2024 Data Book | FY 2024 | Examination coverage with unagreed additional tax, by type and size of return. |
| `table19_revenue_protection_2024db.xlsx` | FY2024 Data Book | FY 2024 | Returns examined involving protection of revenue base. |

### Income Brackets in Table 17 (individual returns)

- No total positive income
- $1 under $25,000
- $25,000 under $50,000
- $50,000 under $75,000
- $75,000 under $100,000
- $100,000 under $200,000
- $200,000 under $500,000
- $500,000 under $1,000,000
- $1,000,000 under $5,000,000
- $5,000,000 under $10,000,000
- $10,000,000 or more

Also includes: EITC returns, international returns, corporate returns by balance sheet size, partnership/S-corp returns, estate/gift tax returns.

### Workforce and Budget

| File | Source | Coverage | Description |
|------|--------|----------|-------------|
| `table33_collections_costs_personnel_1995_2024.xlsx` | FY2024 Data Book | FY 1995–2024 | **Key workforce file.** Gross collections, operating costs, cost per $100 collected, U.S. population, per-capita tax, and full-time equivalent positions. Shows IRS went from 112,024 FTEs in 1995 to 73,519 in 2018 (low point), recovering to 90,516 by 2024. |
| `table32_costs_by_budget_activity.xlsx` | FY2024 Data Book | FY 2023–2024 | Costs broken down by IRS budget activity (enforcement, operations support, taxpayer services, etc.) |
| `table34_personnel_summary.xlsx` | FY2024 Data Book | FY 2023–2024 | Personnel by employment status and budget activity. |

### Collections and Enforcement

| File | Source | Coverage | Description |
|------|--------|----------|-------------|
| `table06_gross_collections_1960_2024.xlsx` | FY2024 Data Book | FY 1960–2024 | Historical gross collections by type of tax. Long time series. |
| `table26_criminal_investigation.xlsx` | FY2024 Data Book | FY 2024 | Criminal investigation program data. |
| `table27_delinquent_collections.xlsx` | FY2024 Data Book | FY 2023–2024 | Delinquent collection activities, assessments, offer-in-compromise. |
| `table28_civil_penalties.xlsx` | FY2024 Data Book | FY 2024 | Civil penalties assessed and abated by type. |

## Key Observations from Initial Inspection

**Audit rates by income (Tax Year 2021, from Table 17):**
- $1–$25K: 0.40% (driven heavily by EITC correspondence audits)
- $25K–$50K: 0.18%
- $50K–$75K: 0.11%
- $200K–$500K: 0.10%  ← the trough
- $500K–$1M: 0.28%
- $1M–$5M: 0.50%
- $5M–$10M: 1.41%
- $10M+: 2.91%

The lowest-income bracket ($1–$25K) is audited at 4x the rate of the $200K–$500K bracket. This is the EITC audit effect.

**IRS staffing collapse:**
- 1995: 112,024 FTEs
- 2018: 73,519 FTEs (low point, -34%)
- 2024: 90,516 FTEs (partial recovery)
- Cost per $100 collected went from $0.54 (1995) to $0.36 (2024)

## Enforcement ROI Context (not in these files)

Treasury Department estimates (https://home.treasury.gov/news/featured-stories/the-case-for-a-robust-attack-on-the-tax-gap):
- Annual tax gap: ~$600 billion
- Top 1% responsible for $160B+ in unpaid taxes annually
- Wage/salary noncompliance: 1%; partnership/proprietorship noncompliance: up to 55%
- $80B IRS investment projected to generate $320B in enforcement revenue over 10 years (4:1 ROI)

## Notes

- Table 17's "all years" revised file is the cleanest source for the time-series analysis. The per-year Data Book files have the same data but cover fewer years each.
- The 2024 Data Book's Table 17 adds Tax Year 2022 data not in the revised file.
- Between the two primary Table 17 files, we have audit rates by income bracket for Tax Years 2010–2022.
- TRAC Syracuse (tracreports.org) has IRS audit data but it's locked behind interactive tools with SVG-only output — not easily downloadable as structured data.
- The `[6]` values in percentage-covered columns indicate suppressed data (small cell counts).
- `d` values indicate data withheld to avoid disclosure of information about specific taxpayers.
