# CFPB Credit Reporting Relief Rate Analysis: Findings

**Date:** 2026-03-20
**Analyst:** Analyzer
**Script:** `scripts/analyze_relief_rates.py`
**Data:** 10.57M CFPB credit reporting complaints, 2020-01-01 to 2026-03-17

---

## Finding 1: Experian's relief rate collapsed from 21.6% (2024 avg) to 0.49% (2025 avg)

- **Number:** 97.7% decline year-over-year. Q1 2024: 36.1% relief. Q1 2025: 1.6% relief. By Q2 2025 it hits 0.09% and stays below 0.2% for the rest of the year.
- **Script:** `scripts/analyze_relief_rates.py` -- quarterly breakdown section
- **Chart:** `charts/relief_rate_cliff_highlighted.png`
- **Confidence:** HIGH
- **Caveats:** The original claim said "approximately 20% in 2024 to less than 1% in 2025." The actual 2024 average was 21.6%, so "approximately 20%" is fair. The 2025 average of 0.49% is indeed below 1%. However, Q1 2025 was still at 1.6% -- the sub-1% rates only consolidated from Q2 2025 onward. The claim is directionally correct and, if anything, understates the severity of the drop.

## Finding 2: Equifax and TransUnion did NOT show the same cliff -- this is Experian-specific

- **Number:** Equifax: 64.0% (2024) -> 64.1% (2025), essentially flat (+0.1 pp). TransUnion: 87.3% (2024) -> 66.5% (2025), a decline of 20.8 pp but nowhere near Experian's collapse.
- **Script:** `scripts/analyze_relief_rates.py` -- summary section
- **Chart:** `charts/relief_rate_by_bureau.png`
- **Confidence:** HIGH
- **Caveats:** TransUnion did experience a significant decline in H2 2025 (dropping from ~84% to ~49%), which is worth noting separately. But the Experian pattern is unique in both timing and magnitude.

## Finding 3: The drop is NOT a data artifact -- response categories are stable

- **Number:** The same five response categories ("Closed with explanation", "Closed with monetary relief", "Closed with non-monetary relief", "In progress", "Untimely response") appear across all years. No new categories were introduced. No categories were retired.
- **Script:** `scripts/analyze_relief_rates.py` -- stress test 1
- **Confidence:** HIGH
- **Caveats:** The "In progress" category appears in 2025 (19 cases) and 2026 (376,868 cases for Experian). The 2026 "In progress" count is massive -- 73.7% of Experian's 2026 responses are "In progress," which means most 2026 complaints haven't been resolved yet. This does NOT affect the 2025 finding, where only 7 Experian complaints show "In progress."

## Finding 4: Experian shifted almost entirely to "Closed with explanation"

- **Number:** In 2024, "Closed with explanation" was 84% of Experian responses and "Closed with non-monetary relief" was 16%. In 2025, "Closed with explanation" jumped to 99.55% and "Closed with non-monetary relief" fell to 0.44%. Experian didn't stop closing complaints -- it stopped granting relief.
- **Script:** `scripts/analyze_relief_rates.py` -- stress test 2, Experian response distribution
- **Chart:** N/A (tabular data)
- **Confidence:** HIGH
- **Caveats:** None. This is the clearest indicator that Experian made a deliberate policy change.

## Finding 5: Complaint volumes exploded for all three bureaus

- **Number:** Experian: Q1 2024 had ~104K closed complaints; Q1 2025 had ~262K. Equifax and TransUnion show similar volume surges. Total Big Three rows: 9.9 million out of 10.6 million in the dataset.
- **Script:** `scripts/analyze_relief_rates.py` -- volume section
- **Chart:** `charts/complaint_volume_by_bureau.png`
- **Confidence:** HIGH
- **Caveats:** The volume surge started in mid-2023 and accelerated through 2024-2025. It's possible (though not testable from this dataset alone) that the volume surge influenced Experian's decision to stop granting relief. More complaints + same staff = less individual review = blanket "explanation" responses.

## Finding 6: The decline is consistent across all sub-products

- **Number:** Experian's relief rate for "Credit reporting" (the dominant sub-product) went from 16.0% (2024) to 0.44% (2025). "Other personal consumer report" went from 15.2% to 1.1%. The pattern is not isolated to one complaint type.
- **Script:** `scripts/analyze_relief_rates.py` -- stress test 4
- **Confidence:** HIGH
- **Caveats:** Cannot test against non-credit-reporting products from this dataset. A complete CFPB download would be needed to check if Experian shows the same pattern in mortgage, debt collection, etc.

## Finding 7: TransUnion's relief rate is also declining, but on a different timeline

- **Number:** TransUnion held steady at ~87% through Q2 2024, then dropped to ~49% by Q3 2025, where it has roughly stabilized. This is a ~38 pp decline over 12 months.
- **Script:** `scripts/analyze_relief_rates.py` -- quarterly breakdown
- **Confidence:** HIGH
- **Caveats:** TransUnion's decline is real but slower, later, and less extreme than Experian's. It may represent a different phenomenon (gradual policy shift vs. Experian's apparent cliff).

---

## Overall Assessment

**The claim is confirmed and, if anything, understated.**

Experian's relief rate didn't just drop from ~20% to <1%. It collapsed from a 2024 average of 21.6% to a 2025 average of 0.49%, a 97.7% relative decline. The transition was rapid -- by February 2025 Experian was granting relief on fewer than 0.1% of closed complaints. This has persisted through Q1 2026.

The control groups prove this isn't a CFPB data issue or an industry-wide shift: Equifax maintained its ~64% relief rate through the same period. TransUnion declined but on a completely different curve.

The mechanism is clear in the data: Experian shifted from "Closed with non-monetary relief" to "Closed with explanation" at massive scale. This is a company-level policy change, not a data artifact.

**What the data does NOT tell us:** Why Experian made this change, whether it's related to the complaint volume surge, and whether consumers are actually worse off (it's possible Experian changed how it categorizes the same underlying actions). Those are editorial/investigative questions, not data questions.
