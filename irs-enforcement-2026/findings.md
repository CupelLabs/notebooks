# IRS Enforcement Collapse: Findings

**Analyst:** Cupel Labs Analyzer
**Date:** 2026-03-21
**Data source:** IRS Data Book (FY2020-FY2024), Tables 17, 33
**Coverage:** Tax Years 2010-2022 (audit rates), Fiscal Years 1995-2024 (staffing)

---

## Finding 1: The $5M-$10M audit rate fell 98.5% in twelve years

- **Number:** Audit rate for filers earning $5M-$10M dropped from 13.545% (2010) to 0.200% (2022)
- **Script:** `scripts/analyze_audits.py`
- **Chart:** Line chart, audit rates over time
- **Confidence:** High. Direct from IRS Data Book Table 17 (revised). Two independent table versions cross-checked.
- **Caveats:** 2022 is the latest available tax year in the Data Book. Post-2022 changes (IRA funding, then DOGE cuts) are not yet in the published data.

## Finding 2: The $10M+ audit rate fell from 21.5% to 4.0%

- **Number:** Filers earning $10M+ went from a 21.498% audit rate (2010) to 4.000% (2022). An 81.4% decline.
- **Script:** `scripts/analyze_audits.py`
- **Chart:** Line chart, audit rates over time
- **Confidence:** High. Same source.
- **Caveats:** The 2022 figure (4.0%) is higher than the 2020 trough (2.43%), suggesting IRA-funded enforcement was beginning to take effect before DOGE cuts.

## Finding 3: Low-income filers are audited at 4x the rate of upper-middle-income filers

- **Number:** In Tax Year 2022, $1-$25K bracket audited at 0.400% vs $200K-$500K at 0.100%. EITC filers audited at 0.700%, 7x the $200K-$500K rate.
- **Script:** `scripts/analyze_audits.py`
- **Chart:** Bar chart, audit rates by income bracket (2022)
- **Confidence:** High. The IRS has acknowledged this disparity is driven by automated EITC correspondence audits, which are cheap to run. Field audits of wealthy taxpayers are expensive.
- **Caveats:** "Audit" includes correspondence audits (paper reviews), which inflate the low-income rate. These are less intensive than field audits targeting high earners. But that IS the point: the IRS chose cheap audits of poor people over expensive audits of rich people.

## Finding 4: IRS lost 34% of its workforce over 23 years

- **Number:** 112,024 FTEs (1995) to 73,519 FTEs (2018). Partial recovery to 90,516 by 2024, still 19.2% below the 1995 peak.
- **Script:** `scripts/analyze_audits.py`
- **Chart:** Staffing time series
- **Confidence:** High. IRS Data Book Table 33.
- **Caveats:** FTE count includes all IRS employees, not just enforcement. The enforcement-specific staffing decline may be steeper.

## Finding 5: Revenue from high-income audits collapsed

- **Number:** Recommended additional tax from $1M+ audits: $1.43B (2010) to $0.29B (2022). A 79.7% decline.
- **Script:** `scripts/analyze_audits.py`
- **Chart:** Referenced in text
- **Confidence:** Medium. The "recommended additional tax" figure is what auditors flag, not what is ultimately collected. But the directional collapse is clear.
- **Caveats:** Recommended tax is not collected tax. Some is disputed, abated, or settled for less. But the decline from $1.43B to $0.29B is too large to be explained by collection efficiency changes alone.

## Finding 6: Overall individual audit rate fell 80%

- **Number:** 1.006% (2010) to 0.200% (2022). 161.7 million returns filed, roughly 323,000 examined.
- **Script:** `scripts/analyze_audits.py`
- **Confidence:** High.
- **Caveats:** None significant. This is a straightforward count.

## Finding 7: Collections per FTE increased 359% while FTEs declined

- **Number:** $12.3M per FTE (1995) to $56.3M per FTE (2024). The remaining IRS employees are far more productive per capita, but cannot cover the enforcement gap.
- **Script:** `scripts/analyze_audits.py`
- **Confidence:** Medium. This number conflates inflation, tax base growth, and genuine productivity gains. It does NOT mean each auditor is finding more money. It mostly reflects that the economy grew faster than the IRS shrank.
- **Caveats:** Not inflation-adjusted. Do not present as "auditors got more efficient." Present as "the economy grew while the IRS shrank."

---

## Data exported

All intermediate data at `data/intermediate/`:
- `audit_rates_by_bracket_2010_2022.csv` - Full dataset
- `audit_rates_key_brackets_pivot.csv` - Pivot for line chart
- `audit_rates_latest_by_bracket.csv` - 2022 snapshot for bar chart
- `irs_staffing_efficiency.csv` - 30-year staffing time series
- `chart_data.json` - Pre-formatted for React chart components
