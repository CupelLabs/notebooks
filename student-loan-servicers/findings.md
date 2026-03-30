# Student Loan Servicer Transition Analysis: Findings

**Date:** 2026-03-30
**Analyst:** Analyzer
**Script:** `scripts/analyze_servicer_transitions.py`
**Data:** 83,680 CFPB student loan complaints (63,111 federal), 2018-01-01 to 2026-03-24

---

## Finding 1: MOHELA went from 63 complaints/year to 7,022 after absorbing FedLoan's portfolio

- **Number:** MOHELA complaints: 63 (2018), 47 (2019), 27 (2020), 30 (2021), 806 (2022), 3,566 (2023), 5,311 (2024), 7,022 (2025). That's an 11,146% increase from 2018 to 2025.
- **Script:** `scripts/analyze_servicer_transitions.py` — yearly totals by servicer
- **Confidence:** HIGH
- **Cross-check:** CFPB Student Loan Ombudsman's 2024 annual report confirms MOHELA received the most complaints of any student loan company. Senate investigation found 43,000 complaints filed against MOHELA in 2023 alone (broader scope than CFPB). Consistent with our data showing MOHELA as #1 complaint target.
- **Caveats:** The growth partly reflects MOHELA absorbing ~8 million accounts from FedLoan. More accounts = more complaints is expected. But the complaint *rate* also increased: MOHELA's complaints grew faster than its account base. It went from near-zero to #1 most-complained-about servicer.

## Finding 2: The FedLoan→MOHELA transfer produced a clear complaint spike in Q4 2022

- **Number:** MOHELA monthly complaints went from 8 (Jun 2022) to 86 (Sep 2022) to 327 (Oct 2022) — a 40x increase in four months. Combined FedLoan+MOHELA portfolio complaints went from 113 (Jun 2022) to 460 (Oct 2022).
- **Script:** `scripts/analyze_servicer_transitions.py` — transition 1 section
- **Confidence:** HIGH
- **Cross-check:** FSA announced FedLoan→MOHELA PSLF transfers beginning July 2022, completing by December 2022 (fsapartners.ed.gov). CNN reported ~2 million borrowers affected. Timeline matches our complaint spike exactly.
- **Caveats:** FedLoan complaints didn't proportionally decrease as MOHELA's increased. The combined portfolio complaints rose from ~110/month pre-transfer to 460 at peak — the transfer created new complaints, not just shifted them.

## Finding 3: The Navient→Aidvantage (Maximus) transfer showed the same pattern but smaller

- **Number:** Maximus (Aidvantage) went from 0 complaints pre-2021 to 193/month in Oct 2022. Combined Navient+Maximus hit 253 in Oct 2022 vs. ~65/month in mid-2021.
- **Script:** `scripts/analyze_servicer_transitions.py` — transition 2 section
- **Cross-check:** Washington Post (March 2022) reported CFPB complaints piling up against Aidvantage. ABC News reported 5.6 million loans transferred. Timeline consistent.
- **Confidence:** HIGH
- **Caveats:** Navient's exit was also driven by a $1.85B settlement for predatory lending, which may have independently driven some complaints.

## Finding 4: Payment restart (Oct 2023) caused a 235% complaint surge

- **Number:** H1 2023 (payments still paused): 2,030 federal student loan complaints. H2 2023 (payments restart Oct): 6,805 complaints. That's a 235% increase. Quarterly: Q2 2023 had 828 complaints; Q4 2023 had 4,576. MOHELA alone went from 117/month (Jun 2023) to 674/month (Oct 2023).
- **Script:** `scripts/analyze_servicer_transitions.py` — payment restart impact
- **Cross-check:** CFPB reported reviewing 9,000+ complaints during the restart period. DOE disclosed MOHELA failed to send bills to 2.5 million borrowers, causing 800,000 missed payments. DOE withheld $7.2M from MOHELA's payment as penalty. NPR, CNN, CNBC all reported the billing failure.
- **Confidence:** HIGH
- **Caveats:** Some of the H2 2023 surge is also attributable to SAVE plan enrollment confusion, not just payment restart. But the timing is unmistakable — the spike begins in September 2023 and peaks in October, exactly when payments restarted.

## Finding 5: MOHELA's timely response rate collapsed from ~100% to 35% in 2025

- **Number:** MOHELA timely response rate: 100% (2020-2021), 97% (2022), 99.9% (2023), 100% (2024), 35.0% (2025). Two-thirds of 2025 MOHELA complaints received untimely responses.
- **Script:** `scripts/analyze_servicer_transitions.py` — timeliness section
- **Cross-check:** BBB downgraded MOHELA to F rating in 2025. DOE stopped awarding MOHELA new accounts in Oct 2024 and threatened contract termination. AFT sued MOHELA in July 2024 for "call deflection" scheme. MOHELA's Q4 2024 call wait times were 7x the second-worst servicer.
- **Confidence:** HIGH
- **Caveats:** The 2024 rate (100%) vs 2025 (35%) is a striking cliff. It's possible MOHELA's 2024 "timeliness" was gamed (auto-responding to meet deadlines). The 2025 collapse may reflect either genuine deterioration or a change in how CFPB categorizes timeliness.

## Finding 6: EdFinancial also collapsed on timeliness in 2023-2024 (33%)

- **Number:** EdFinancial timely response rate: 100% (2018-2022), 32.8% (2023), 32.6% (2024), 91.2% (2025). EdFinancial recovered in 2025; MOHELA went the opposite direction.
- **Script:** `scripts/analyze_servicer_transitions.py` — timeliness section
- **Confidence:** HIGH
- **Caveats:** EdFinancial also received transferred accounts (from Granite State/GSMR). The pattern holds: servicers who absorb transferred portfolios see timeliness degrade.

## Finding 7: Complaint volumes are at all-time highs and accelerating

- **Number:** Federal student loan complaints by year: 5,633 (2018), 4,937 (2019), 2,929 (2020), 2,652 (2021), 5,832 (2022), 8,835 (2023), 10,781 (2024). 2025 is on track for ~21,500 (extrapolating from 17,825 through ~Q3). Q1 2025 alone (6,605) exceeds all of 2020 or 2021.
- **Script:** `scripts/analyze_servicer_transitions.py` — quarterly totals
- **Cross-check:** CFPB's 2024 Student Loan Ombudsman report documented complaint volumes higher than previous years. GAO report confirmed repayment restart challenges.
- **Confidence:** HIGH
- **Caveats:** 2020-2021 were artificially low due to COVID forbearance (no payments = fewer complaints). The fair baseline is 2018-2019, when complaints were ~5,000-5,600/year. Current levels are 2-4x that baseline.

## Finding 8: "Dealing with your lender or servicer" dominates complaints — and the share grew

- **Number:** In 2020, "Dealing with your lender or servicer" was 68.2% of issues. In 2022, it was 84.4%. MOHELA-specific complaints 2022-2023: 88.6% were "Dealing with your lender or servicer."
- **Script:** `scripts/analyze_servicer_transitions.py` — issue breakdown
- **Confidence:** HIGH
- **Caveats:** This is a broad CFPB category. It covers billing errors, payment processing, account access, and general servicing. The concentration in this category is consistent with transition-related problems (lost records, wrong balances, access issues).

## Synthesis

Every major administrative event — servicer transfers, payment restart, SAVE plan confusion — produced measurable complaint spikes in CFPB data. The pattern is consistent:

1. **Pre-event baseline** (stable, low complaints)
2. **Event occurs** (transfer, restart, policy change)
3. **Spike** within 1-3 months
4. **Partial recovery** but to a new, higher baseline
5. **Next event** hits before recovery completes, ratcheting complaints higher

MOHELA is the case study. It absorbed the nation's largest public service loan portfolio, then immediately faced the payment restart, then the SAVE plan rollout. Each shock stacked on the last. By 2025, it's the most-complained-about student loan servicer in America, with a 35% timely response rate and an F from the BBB.

The thesis is supported: servicer transitions produce measurable, quantifiable harm visible in complaint data. But the finding is bigger than transitions alone. The federal student loan system is running every major servicer at or past capacity, and administrative churn makes it worse.
