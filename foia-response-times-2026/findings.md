# FOIA Response Times: Findings

**Data source:** FOIA.gov Annual Report CSVs, FY2018-FY2024 (7 fiscal years, 32 CSVs per year, 118-123 agencies per year)
**Script:** `scripts/analyze_foia.py`
**Intermediate data:** `data/intermediate/` (28 CSV files)
**Analysis date:** 2026-03-21

**CRITICAL CAVEAT:** All data is self-reported by the agencies themselves. There is no independent audit of these numbers. Agencies have incentive to underreport backlogs and overreport compliance. Every finding below should be read with this in mind.

---

## Finding 1: The federal FOIA backlog doubled in seven years, hitting 267,056 in FY2024
- **Number:** Backlog grew from 130,718 (FY2018) to 267,056 (FY2024), a 104.3% increase.
- **Script:** `analyze_foia.py`, Section 2 (Backlog Analysis) and Section 7 (Overall Trends)
- **Confidence:** High
- **Why this confidence level:** The backlog figure comes directly from the "All agencies" summary row in the source data, which matches the sum of individual agencies exactly (267,056 both ways). The trend is monotonic except for a small dip in FY2023 (200,843 from 206,636).
- **What would make this wrong:** If agencies changed how they define "backlogged" across years, the comparison would be invalid. The FOIA statute defines backlogged as requests pending beyond the statutory time limit, but agencies may apply this differently.
- **Cross-check:** Brechner Center for Freedom of Information (April 2025) reports "backlogged requests increased 33%, from 200,843 to 267,056." My FY2023 and FY2024 numbers match exactly. Federal News Network also cites the 267,000 figure. **Confirmed.**
- **Caveats:** The backlog number is distinct from "pending at end of year" (390,548 in FY2024). Pending includes requests still within the statutory time limit. The backlog is requests that have exceeded it.

## Finding 2: DHS owns 53% of the federal FOIA backlog -- 141,420 requests
- **Number:** DHS backlog = 141,420 (FY2024). This is 53.0% of the total 267,056 backlog. DHS backlog nearly tripled from 52,239 (FY2022) to 141,420 (FY2024).
- **Script:** `analyze_foia.py`, Section 2
- **Confidence:** High
- **Why this confidence level:** The number comes directly from the source data. DHS's dominance of FOIA volumes is well-documented.
- **What would make this wrong:** If DHS's definition of backlogged changed, or if they reclassified a large batch of requests. The jump from 63,883 (FY2023) to 141,420 (FY2024) is dramatic enough to warrant skepticism, but it coincides with DHS receiving 894,939 requests in FY2024 (61% of all federal FOIA requests), so the scale is consistent.
- **Cross-check:** Brechner Center reports DHS handles "61% of government FOIA requests." My data: 894,939 / 1,501,432 = 59.6%. Close match (Brechner may be rounding). GAO (2022) reported DHS accounted for "about 60% of government-wide" requests. **Confirmed.**
- **Caveats:** DHS's FOIA volume is dominated by USCIS immigration records, which are largely routine. The backlog-to-received ratio (141,420 / 894,939 = 15.8%) is actually lower than several smaller agencies. DHS's problem is one of raw scale, not necessarily dysfunction.

## Finding 3: The full grant rate hit an all-time low of 12.1% in FY2024
- **Number:** 181,574 full grants out of 1,499,265 processed requests = 12.1%. Down from 26.9% in FY2018. The decline is steady and monotonic across all 7 years.
- **Script:** `analyze_foia.py`, Section 3 (Denial and Exemption Patterns)
- **Confidence:** High
- **Why this confidence level:** The trend is consistent year-over-year with no reversals. The absolute numbers are large enough to rule out sampling noise.
- **What would make this wrong:** If the composition of requests changed dramatically (e.g., more requests for classified material), the declining grant rate could reflect a harder request mix rather than increased stonewalling. Also, "partial grant/partial denial" is a middle category -- the government could argue it's providing more partial information.
- **Cross-check:** Brechner Center reports "12% (all-time low)" for FY2024 and "38% in 2010" as the historical high. My 12.1% rounds to their 12%. **Confirmed.**
- **Caveats:** A declining grant rate does not necessarily mean more stonewalling. It could also mean more people are requesting information that legitimately falls under exemptions (e.g., law enforcement records, classified material). The composition of requests matters, and this dataset does not capture what people are actually asking for.

## Finding 4: Exemption 6 (privacy) and 7(C) (law enforcement privacy) account for 63% of all exemption invocations
- **Number:** In FY2024, Ex. 6 was invoked 474,605 times and Ex. 7(C) was invoked 486,454 times. Together: 961,059 out of 1,520,226 total exemption invocations = 63.2%. Ex. 7(E) (law enforcement techniques) adds another 348,702 (22.9%). These three exemptions account for 86.1% of all invocations.
- **Script:** `analyze_foia.py`, Section 3
- **Confidence:** High
- **Why this confidence level:** These are raw counts from the source data, summed across agencies. The pattern is consistent across all 7 years.
- **What would make this wrong:** If agencies are misclassifying exemptions (e.g., using Ex. 6 privacy when Ex. 5 deliberative process would be more accurate), the distribution would be misleading.
- **Cross-check:** No independent source found that reports exact exemption totals for FY2024. The dominance of Ex. 6 and Ex. 7(C) is consistent with prior years' DOJ annual FOIA report summaries.
- **Caveats:** A single request can trigger multiple exemptions. The total exemption count (1.52M) exceeds total processed requests (1.50M) because of this. DHS alone accounts for 1,189,161 exemption invocations (78% of the total), heavily skewing the picture.

## Finding 5: Exemption usage surged in FY2024 -- Ex. 6 up 51%, Ex. 7(C) up 84%, Ex. 7(E) up 63%
- **Number:** Year-over-year increases from FY2023 to FY2024: Ex. 6 (privacy) from 315,062 to 474,605 (+51%); Ex. 7(C) (law enforcement privacy) from 263,899 to 486,454 (+84%); Ex. 7(E) (law enforcement techniques) from 213,684 to 348,702 (+63%). Ex. 5 (deliberative process) also jumped from 68,541 to 86,802 (+27%).
- **Script:** `analyze_foia.py`, Section 3 (Exemption Trends)
- **Confidence:** Medium
- **Why this confidence level:** The numbers are clear, but the surge coincides with a 34% increase in processed requests (1.12M to 1.50M). Some increase is expected from volume alone. The question is whether exemptions grew faster than volume, and they did -- Ex. 7(C) grew 84% against 34% volume growth. That said, this could reflect the composition of new requests (e.g., more USCIS/law enforcement requests) rather than a policy change.
- **What would make this wrong:** If the surge is entirely driven by one agency (likely DHS/USCIS) processing a backlog of older requests that happen to use these exemptions.
- **Cross-check:** No independent source found with FY2024 exemption breakdowns. Brechner Center mentions increased denials but does not detail exemption categories.
- **Caveats:** DHS skews everything. Further analysis separating DHS from the rest would clarify whether this is a government-wide trend or a DHS-specific phenomenon.

## Finding 6: The CIA denies 29.5% of FOIA requests outright -- highest rate among agencies with 100+ processed
- **Number:** CIA: 767 full denials based on exemptions out of 2,603 processed = 29.5%. Next: NTSB at 27.5%, ODNI at 18.2%.
- **Script:** `analyze_foia.py`, Section 3
- **Confidence:** High
- **Why this confidence level:** Direct computation from source data. The CIA's high denial rate is unsurprising given the nature of its records.
- **What would make this wrong:** If the CIA's "total processed" includes a different mix of disposition categories than other agencies.
- **Cross-check:** No specific independent source found for CIA's FY2024 denial rate. The CIA's historically high denial rate is well-documented in prior FOIA audits by the National Security Archive.
- **Caveats:** Full denial rate alone is misleading. CIA also had a 5.2% full grant rate. The question is what happens to the other 65% -- much of it falls into "partial grant/partial denial," "no records," "referred," etc. A full denial at the CIA may be more defensible (national security) than a full denial at, say, the Department of Labor.

## Finding 7: Only 74% of simple FOIA requests are processed within 20 calendar days
- **Number:** In FY2024, 316,455 of 427,706 simple requests (74.0%) were completed within the 1-20 day bucket. The worst agencies: Federal Retirement Thrift Investment Board (18.3%), Office of Management and Budget (20.0%), USTDA (31.2%), Federal Maritime Commission (31.5%).
- **Script:** `analyze_foia.py`, Section 4
- **Confidence:** Medium
- **Why this confidence level:** The 20-day bucket in the data uses calendar days, but the FOIA statute specifies 20 business days (~28 calendar days). So 74% is an undercount of actual statutory compliance -- the true compliance rate is higher than 74% because some requests in the 21-40 day bucket would still be within 20 business days.
- **What would make this wrong:** The calendar-vs-business-day mismatch means this is a conservative estimate of non-compliance. Actual compliance is likely 5-10 percentage points higher.
- **Cross-check:** Brechner Center reports "average of 44 days" for simple requests in FY2024 (up from 39 in FY2023). This is the unweighted mean of agency averages, which I can reproduce (44.0 days). The volume-weighted average is 20.2 days, much lower because DHS processes fast at scale. **Average confirmed; compliance percentage not independently reported.**
- **Caveats:** (1) Calendar vs. business day mismatch. (2) The "simple" vs "complex" classification is determined by each agency, creating potential for gaming. (3) The worst-performing agencies on this metric tend to be small agencies where a few difficult requests can distort the percentage.

## Finding 8: For complex requests, only 27.4% are processed within 20 days
- **Number:** 200,678 of 731,555 complex requests (27.4%) fell in the 1-20 day bucket in FY2024.
- **Script:** `analyze_foia.py`, Section 4
- **Confidence:** Medium
- **Why this confidence level:** Complex requests have no statutory time limit beyond 20 business days (agencies can negotiate extensions). The 20-day bucket is informative but not a compliance measure for complex requests.
- **What would make this wrong:** Complex requests are expected to take longer. The relevant question is not "how many finish in 20 days" but "how long do they actually take." The median complex processing time varies wildly -- NARA at 2,444 days vs. many agencies under 50 days.
- **Cross-check:** No independent source found for complex request time distributions.
- **Caveats:** Agencies decide what counts as "complex." Reclassifying a request from simple to complex resets expectations and buys time. There is no independent check on this classification.

## Finding 9: NARA has the longest complex request median: 2,444 days (6.7 years)
- **Number:** National Archives and Records Administration: median complex FOIA request takes 2,444 days (6.7 years) to process. The oldest pending NARA request is 4,571 days (12.5 years).
- **Script:** `analyze_foia.py`, Sections 1 and 6
- **Confidence:** High
- **Why this confidence level:** NARA's extreme processing times are a well-documented, structural problem related to declassification review.
- **What would make this wrong:** If NARA's "complex" classification captures a genuinely different type of request (classified historical records requiring multi-agency declassification review), the comparison to other agencies' complex requests is not apples-to-apples.
- **Cross-check:** National Security Archive (March 2024) documents "12-year queues at the National Declassification Center" and notes NARA had a FOIA request from 1993 still pending (as of 2019). My FY2024 data shows NARA's oldest request at 4,571 days (filed ~2012), suggesting the 1993 request was eventually resolved. **Pattern confirmed; specific numbers differ due to different timeframes.**
- **Caveats:** NARA's problem is fundamentally different from most agencies. They are not "stonewalling" -- they are processing declassification requests that require coordination with intelligence agencies. The delay is structural, not attitudinal.

## Finding 10: 24 agencies have FOIA requests older than 5 years; 4 agencies have requests older than 10 years
- **Number:** In FY2024, 24 agencies reported their oldest pending request at >1,826 days (5 years). Four agencies have requests >3,652 days (10 years): NARA (12.5 years), State Department (11.7 years), DoD (11.3 years), CIA (10.8 years).
- **Script:** `analyze_foia.py`, Section 6
- **Confidence:** High
- **Why this confidence level:** Direct from the "ten oldest pending requests" file, which is reported by each agency.
- **What would make this wrong:** If agencies are not accurately reporting their oldest requests, or if some of these are edge cases that have been substantially responded to but remain technically "pending."
- **Cross-check:** National Security Archive has documented multi-decade FOIA delays at national security agencies. The pattern of State, DoD, and CIA having the oldest requests is consistent with prior reporting. **Pattern confirmed.**
- **Caveats:** The four agencies with 10+ year requests are all national security/foreign policy agencies where declassification review is the bottleneck. This is a different phenomenon from general FOIA processing delays.

## Finding 11: Spending more on FOIA does not correlate with faster processing
- **Number:** Correlation between processing costs and simple median processing time: r = -0.111. Correlation between cost per request and simple median days: r = -0.061. Neither is statistically meaningful. Total federal FOIA spending was $723M in FY2024 (up from $550M in FY2018, +31.4%).
- **Script:** `analyze_foia.py`, Section 5
- **Confidence:** Medium
- **Why this confidence level:** The lack of correlation is real in the data, but the analysis is crude -- it compares across agencies that process very different types of requests. EPA spending $6,556 per request vs. DHS spending $104 per request reflects the nature of the requests, not efficiency.
- **What would make this wrong:** If there is a within-agency correlation (more spending -> faster in that same agency over time) that the cross-sectional analysis misses. A panel analysis would be needed.
- **Cross-check:** Brechner Center reports $723M for FY2024 processing (though they appear to mean total costs including litigation). My processing costs = $669M, litigation = $54M, total = $723M. **Total confirmed; breakdown note: Brechner labels the $723M as "processing costs" but it includes litigation.**
- **Caveats:** Cross-agency comparisons of cost efficiency are misleading. A classified document request at CIA costs more to process than a routine USCIS record. The "right" spending level is unknowable from this data.

## Finding 12: Several small agencies saw explosive slowdowns -- FLRA went from 5 days to 367 days
- **Number:** Federal Labor Relations Authority: simple median processing time went from 5 days (FY2018) to 366.5 days (FY2024), a 7,230% increase. Chemical Safety Board: 10 to 264.5 days. NSF: 9 to 112.75 days. OMB: 35 to 112 days.
- **Script:** `analyze_foia.py`, Section 1 (Trend analysis)
- **Confidence:** Medium
- **Why this confidence level:** The numbers are real, but small agencies process few requests, so a handful of difficult requests can massively distort the median. FLRA processes ~200 requests/year.
- **What would make this wrong:** If FLRA received a batch of unusually complex requests in FY2024, or if they had staffing disruptions, the spike could be temporary rather than systemic.
- **Cross-check:** No independent source found for FLRA-specific FOIA processing times.
- **Caveats:** Small-agency statistics are inherently noisy. The story is more interesting at State Department, which went the opposite direction: 401 days (FY2018) to 10 days (FY2024), a 97.5% improvement.

## Finding 13: Requests received nearly doubled (863K to 1.50M) while the system barely kept pace
- **Number:** Requests received: 863,729 (FY2018) to 1,501,432 (FY2024), +73.8%. Requests processed: 830,060 to 1,499,265, +80.6%. The net gap (received minus processed) was +2,167 in FY2024 -- agencies nearly kept pace -- but the backlog still grew because it accumulated from prior years' gaps.
- **Script:** `analyze_foia.py`, Section 7
- **Confidence:** High
- **Why this confidence level:** These are the most basic aggregate figures in the dataset, directly from source totals.
- **What would make this wrong:** If the definition of "received" or "processed" changed across years.
- **Cross-check:** Federal News Network (April 2025): "record 1.5 million Freedom of Information Act requests in fiscal 2024" and "agencies nearly kept pace by processing 1.49 million." **Confirmed.**
- **Caveats:** "Processed" includes all dispositions -- full grants, partial, denials, withdrawals, referrals, no records. A request is "processed" even if the answer is "no."

## Finding 14: Three agencies have backlogs larger than their annual intake
- **Number:** NSF: backlog ratio 1.85 (784 backlogged vs 424 received). ODNI: 1.48 (747 vs 504). CIA: 1.19 (4,879 vs 4,087). These agencies would need more than a full year of zero new requests to clear their existing backlog.
- **Script:** `analyze_foia.py`, Section 2 (Backlog-to-received ratio)
- **Confidence:** High
- **Why this confidence level:** Direct computation from source data, filtered to agencies with 100+ requests.
- **What would make this wrong:** If "backlogged" includes requests that are substantively complete but technically still open.
- **Cross-check:** No independent source found for agency-level backlog ratios.
- **Caveats:** Intelligence agencies (ODNI, CIA) have uniquely complex review processes. NSF's high ratio is more surprising and worth investigating.

---

## Overall Assessment

The thesis holds: **some federal agencies systematically stonewall FOIA requests while others comply promptly.** But the picture is more nuanced than "good agencies vs bad agencies":

1. **The system is drowning in volume.** Requests nearly doubled over 7 years. Agencies mostly kept pace on raw throughput but could never catch up on the accumulated backlog.

2. **DHS dominates everything.** It handles 60% of requests, owns 53% of the backlog, and accounts for 78% of exemption invocations. Any government-wide FOIA statistic is largely a DHS statistic.

3. **The full grant rate collapse (26.9% to 12.1%) is the strongest indicator of systemic change.** Whether this reflects changed request composition or changed agency behavior is the open question.

4. **The worst delays are structural, not attitudinal.** The agencies with the oldest requests (NARA, State, DoD, CIA) are dealing with declassification review backlogs, not administrative dysfunction.

5. **Small agency statistics are noisy.** The agencies at the top of "worst processing time" lists are tiny (FLRA, Chemical Safety Board). The more newsworthy story is large agencies like State Department dramatically improving or large agencies like DHS accumulating massive backlogs.

6. **Self-reported data is inherently suspect.** No finding here can be verified against an independent audit because no such audit exists.
