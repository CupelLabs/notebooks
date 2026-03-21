# EPA Endangerment Finding Rescission: Analysis Findings

**Source document:** EPA-420-R-26-002 (Regulatory Impact Analysis, 35 pages)
**Supporting documents:** Economic Impact Fact Sheet (EPA-420-F-26-002), Federal Register Final Rule (91 FR 7686), Response to Comments (EPA-420-R-26-003, 335 pages)
**Analysis period:** 2027-2055, all figures in billions of 2024 dollars unless noted
**Script:** `analyzer/experiments/epa-endangerment/scripts/extract_ria_tables.py`
**Intermediate data:** `analyzer/experiments/epa-endangerment/data/intermediate/`

---

## Finding 1: The fact sheet claims $1.3 trillion in "savings" while the RIA's primary scenario shows a $180 billion net cost

- **Number:** The EPA fact sheet states "this action will result in over $1.3 trillion in savings from 2027 through 2055." The RIA's Scenario A1 (AEO 2025 Reference case energy prices, full lifetime fuel costs) shows: gross savings of $1,290B (vehicle technology $1,090B + EVSE $200B) offset by costs of $1,470B (fuel, repair, maintenance, insurance, congestion, noise $1,430B + energy security, refueling time, drive value $40B). Net impact: -$180B. That is a cost, not a savings.
- **Script:** `extract_ria_tables.py` -- see "THE CONTRADICTION" section
- **Confidence:** High
- **Why this confidence level:** The numbers come directly from the EPA's own documents. The fact sheet figure ($1.3T) matches the gross savings in Table A-1 ($1,290B rounds to $1.3T). The net figure (-$180B) is stated explicitly in the RIA text: "the scenario A1 analysis shows an estimated net societal cost associated with rescinding GHG standards...of about $180 billion." The RIA itself confirms: "removing the GHG standards would lead to a reduction in vehicle technology and EVSE costs of approximately $1.3 trillion." Both numbers are correct; the fact sheet simply omits the cost side.
- **What would make this wrong:** If the fact sheet intended to reference a different scenario (A3 or A4) rather than A1. However, the fact sheet does not mention scenarios, discount rates, or fuel cost valuation assumptions. It presents the $1.3T as an unqualified statement about "this action."
- **Cross-check:** FactCheck.org (March 2026) independently identified this same contradiction, calling EPA's claim "misleading." Bloomberg (Feb 19, 2026) reported "costs of EPA's endangerment finding rollback could outweigh savings." Electrek (Feb 18, 2026) reported the $1.47T cost figure and $180B net cost. All three match our numbers exactly.
- **Caveats:** The fact sheet is technically not wrong about the gross savings figure -- $1,290B does round to "over $1.3 trillion." The issue is that reporting gross savings without mentioning net impact is misleading by omission. The EPA's own RIA presents both sides.

---

## Finding 2: Only 1 of 8 scenario/discount-rate combinations shows a net cost; it is the most realistic one

- **Number:** Across 4 scenarios and 2 discount rates (3% and 7%), only Scenario A1 at 3% shows a net cost (-$180B). The other 7 show net savings ranging from $89B to $920B. However, A1 uses the EIA's best-estimate fuel prices (AEO 2025 Reference case) and counts full lifetime fuel costs -- making it the most methodologically standard scenario. The scenarios showing net savings require either (a) assuming fuel prices will be much lower than the EIA projects (A2, A4), or (b) counting only 2.5 years of fuel costs over a vehicle's lifetime (A3, A4), or (c) both.
- **Script:** `extract_ria_tables.py` -- see "SCENARIO OUTCOME MATRIX"
- **Confidence:** High
- **Why this confidence level:** Direct table extraction from the RIA. The scenario descriptions are unambiguous.
- **What would make this wrong:** If the AEO 2025 Reference case fuel prices turn out to be significantly higher than actual prices (making A2/A4 more realistic). Also, if the 2.5-year fuel valuation is actually the correct economic assumption (contested -- see Finding 4).
- **Cross-check:** The Federal Register (91 FR 7686, p. 7755) confirms identical scenario results. The CNBC article (Feb 12, 2026) reported "One of the EPA's key estimates -- using the Energy Information Administration's best guess for future fuel prices -- shows that rescinding the policy will cost Americans $180 billion on net." Match.
- **Caveats:** At the 7% discount rate, even Scenario A1 shows net savings of $89B. The choice of discount rate matters. However, OMB Circular A-4 (revised 2023) recommends 2% as the default, which would push the net cost even higher than -$180B. The 3% rate used in A1 is already more favorable to the repeal than the current OMB guidance.

---

## Finding 3: The $1.3 trillion headline counts vehicle sticker price reductions but ignores that consumers pay more at the pump

- **Number:** Under Scenario A1, rescinding the standards reduces vehicle technology costs by $1,090B ($2,330 per vehicle across 469 million vehicles). But it increases lifetime fuel, repair, maintenance, insurance, congestion, and noise costs by $1,430B. Per vehicle: $2,330 cheaper to buy, but $3,050 more expensive to own. The fact sheet highlights "$2,400/vehicle" in savings (which rounds up from $2,330); it does not mention the $3,050 in increased ownership costs.
- **Script:** `extract_ria_tables.py` -- see per-vehicle calculations
- **Confidence:** High
- **Why this confidence level:** The $2,330 per-vehicle figure is explicitly stated in the RIA (line 1623) and matches our independent calculation ($1,090B / 469M vehicles = $2,324, rounds to $2,330). The per-vehicle ownership cost increase is computed from the same table ($1,430B / 469M = $3,049).
- **What would make this wrong:** If fuel prices fall significantly below EIA projections. Under the low oil price scenario (A2), fuel/maintenance costs drop to $1,040B, making the per-vehicle ownership cost increase $2,203 -- still nearly matching the per-vehicle technology savings.
- **Cross-check:** The EPA's RIA text itself states "$2,330 per vehicle" (confirmed). The fact sheet rounds this to "$2,400/vehicle" -- likely using a slightly different denominator or rounding. Electrek (Feb 18, 2026) reported "76 cents per gallon" fuel price increase per DOE calculations, which is consistent with the aggregate fuel cost increase.
- **Caveats:** The per-vehicle ownership cost increase assumes full lifetime fuel costs. Under the 2.5-year assumption, it would be much lower. The comparison also aggregates across light-duty, medium-duty, and heavy-duty vehicles, which have very different usage profiles.

---

## Finding 4: A single assumption -- counting only 2.5 years of fuel costs -- swings the result by $970 billion

- **Number:** Under reference fuel prices: Scenario A1 (full fuel costs) shows -$180B net cost. Scenario A3 (identical except 2.5 years of fuel costs) shows +$790B net savings. The swing is $970B from one assumption. Under low oil prices: the swing from A2 to A4 is $670B. The 2.5-year assumption discards 68% of lifetime fuel costs ($1,430B becomes $460B). This single methodological choice determines whether the repeal is a $180B cost or a $790B savings.
- **Script:** `extract_ria_tables.py` -- see "IMPACT OF 2.5-YEAR FUEL COST VALUATION ASSUMPTION"
- **Confidence:** High (that the assumption produces this swing); Medium (on whether the assumption is correct)
- **Why this confidence level:** The numerical swing is directly calculable from the RIA tables. Whether the 2.5-year assumption is appropriate is a contested empirical question. The RIA itself presents a literature review (Chapter 5) showing estimates ranging from 16% to 142% of future fuel costs internalized by consumers, with no consensus.
- **What would make this wrong:** If the 2.5-year assumption is actually the correct representation of consumer behavior. Some manufacturers have told EPA that consumers consider ~2-3 years of fuel savings. However, the EPA's own Table 1 in the RIA shows most recent panel studies find consumers internalize 50-100% of future fuel costs at moderate discount rates (4-7%), not the ~32% implied by 2.5 years.
- **Cross-check:** Jason Schwartz (NYU Institute for Policy Integrity) called the 2.5-year assumption "not supported by the economics literature." FactCheck.org reported an expert consensus that "this makes a gigantic difference to the costs and benefits." The EPA's own RIA acknowledges that "the 2.5-year assumption is on the lower end of the estimates" in the literature (RIA line 1130). Leard et al. (2023), cited in the RIA, finds results consistent with a 7-year payback period.
- **Caveats:** The RIA frames scenarios A1/A3 as a "bounding exercise" representing two different interpretations of consumer behavior. This is methodologically defensible as sensitivity analysis. The issue is not that the 2.5-year scenario exists, but that the fact sheet's headline figure appears to cherry-pick from the gross savings of the scenarios without disclosing the net impact under either assumption.

---

## Finding 5: The RIA excludes all climate and health costs -- categories the Biden-era RIA valued at ~$85 billion per year

- **Number:** The current 35-page RIA contains zero monetized climate benefits or health costs. It does not use the Social Cost of Carbon or Social Cost of Greenhouse Gases. The Biden-era 2024 LMDV final rule RIA (89 FR 27842) estimated approximately $72 billion per year in annualized climate benefits and $13 billion per year in annualized health benefits from the vehicle standards being rescinded. These categories total ~$85 billion annually, or roughly $1.6 trillion at a 2% discount rate over the analysis period. None of this appears in the current RIA.
- **Script:** `extract_ria_tables.py` -- see "WHAT IS NOT MONETIZED" section
- **Confidence:** Medium
- **Why this confidence level:** The omission from the current RIA is verifiable fact -- the document contains no SC-GHG calculations. The $72B and $13B annual figures come from EPA's own 2024 rule analysis. However, (a) the Biden-era figures used different baseline assumptions, so direct comparison is imperfect; (b) the current EPA takes the legal position that the Clean Air Act does not authorize GHG regulation, making climate benefit monetization arguably outside scope; (c) the social cost of carbon methodology itself is contested.
- **What would make this wrong:** If the legal framework genuinely precludes consideration of climate costs in the RIA (a legal question, not an analytical one). Also, the $85B/year is the Biden-era estimate using 2022-era models and assumptions; actual values depend on discount rate, modeling choices, and SC-GHG methodology.
- **Cross-check:** EPA's own landing page for the 2024 LMDV rule states the standards would deliver "nearly $100 billion of annual net benefits." FactCheck.org (March 2026) reported "EPA's 2024 rule estimated $200 billion from reduced particle pollution" and "$1.6 trillion in climate benefits (2022 dollars, 3% discount)." Kenneth Gillingham (Yale) told FactCheck.org: "I honestly can't recall another rulemaking where the focus was ONLY about the costs."
- **Caveats:** The Biden-era figures are not a direct counterfactual because the modeling assumptions, baselines, and dollar years differ. The comparison is directionally valid (the exclusion is massive) but the precise dollar amounts should be treated as indicative, not exact.

---

## Finding 6: The RIA is 35 pages vs. ~1,800 pages for the rules it rescinds, with no new economic modeling

- **Number:** The RIA (EPA-420-R-26-002) is 35 pages. The Biden-era LMDV RIA and HD GHG Phase 3 RIA it replaces were approximately 1,800 pages combined. The current RIA reuses the 2024 OMEGA and HD TRUCS compliance models with updated assumptions (IRA tax credit changes via OBBB, removal of California ACT rule, reduced BEV acceptance levels, updated fuel prices). No new independent economic modeling was performed.
- **Script:** Page count is a physical property of the PDF. Modeling reuse is documented in the RIA text at lines 152-157 and the Federal Register.
- **Confidence:** High
- **Why this confidence level:** Page count is directly measurable (the PDF is 35 pages). The RIA explicitly states it uses "updated versions of the models and tools used in the 2024 LMDV and HDP3 rulemakings."
- **What would make this wrong:** If "updated versions" constitutes sufficiently new modeling. The EPA would argue that updating assumptions within existing models is standard practice. The question is whether the magnitude of the regulatory change (rescinding all GHG vehicle standards) warrants a proportionally more thorough analysis.
- **Cross-check:** Joshua Linn (University of Maryland) and Jason Schwartz (NYU) have both noted publicly that no new modeling was performed. Multiple legal challenges have been filed citing the inadequacy of the analysis. Harvard's Salata Institute analysis noted the analysis "bears no resemblance to the careful, deliberate, and evidence-based approach EPA has historically used."
- **Caveats:** Page count alone does not determine analytical quality. A focused 35-page analysis could theoretically be superior to an unfocused 1,800-page one. The substantive critique is about what is absent (climate/health costs, alternative regulatory scenarios, independent technology assessment), not the page count per se.

---

## Finding 7: 572,000 public comments were received; the response document is 335 pages

- **Number:** EPA received approximately 572,000 public comments during the comment period. The Response to Comments document (EPA-420-R-26-003) is 335 pages. Multiple commenters raised the cost-benefit contradiction and the exclusion of climate/health costs. The Federal Register notes commenters suggested longer payback periods (e.g., 7 years per Leard et al. 2023) and inclusion of SCC methodology.
- **Script:** Comment count from the README and Federal Register. RTC document properties confirm 335 pages.
- **Confidence:** High (on the numbers); Medium (on whether the comments substantively addressed the cost-benefit contradiction)
- **Why this confidence level:** The 572,000 figure and 335-page RTC are documented. Without a full parse of the RTC, I cannot enumerate every comment addressing the specific cost-benefit contradiction, but the Federal Register text confirms comments on SCC methodology and payback period assumptions were received and responded to.
- **What would make this wrong:** If the 572,000 figure includes form letters or mass-campaign submissions (likely), the number of unique substantive comments would be much smaller.
- **Cross-check:** The Environmental Protection Network submitted detailed oral comments during the August 2025 hearings. Holland & Knight's analysis confirmed the public comment period opened in August 2025. No independent source contradicts the 572,000 figure.
- **Caveats:** Volume of comments does not correlate with quality. Mass-campaign comments are common in EPA rulemakings. The substantive question is whether the EPA adequately responded to the cost-benefit objections, not how many people raised them.

---

## Summary Assessment

The thesis holds. The EPA's fact sheet claims "$1.3 trillion in savings." The EPA's own RIA, under its primary scenario (A1, AEO 2025 Reference case, full lifetime fuel costs, 3% discount rate), shows a net societal cost of $180 billion, not a net savings. The $1.3 trillion figure is the gross savings from reduced vehicle technology and EVSE costs; it omits $1.47 trillion in increased fuel, maintenance, insurance, congestion, and noise costs.

The only scenarios showing net savings require either assuming fuel prices well below EIA projections or counting only 2.5 years of fuel costs over a vehicle's 10-15 year lifetime. Both are methodologically contestable.

Additionally, the RIA excludes climate and health costs entirely -- categories the Biden-era analysis valued at approximately $85 billion per year.

**Honest assessment of strength:** The core contradiction (fact sheet vs. RIA net impact) is rock-solid. The numbers are from the same agency, the same rule, published the same month. Multiple independent sources have confirmed the same discrepancy. The analytical exclusions (climate/health costs, SCC) and the 2.5-year assumption are legitimate editorial targets but involve more judgment about methodology. The article should lead with Finding 1 and treat the methodological critiques as supporting evidence, not the headline.

**What could undermine the article:** If the EPA explicitly stated somewhere that the $1.3T refers to gross savings and the net impact is different, the "contradiction" framing weakens. However, the fact sheet contains no such qualification. It presents "$1.3 trillion in savings" as the headline impact with no mention of costs or net impact.
