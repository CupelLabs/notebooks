# 10-K Risk Factor vs AI Capex Analysis

Prepared by Analyzer for Cupel Labs. Data as of March 2026.

---

## 1. Comparison Table

| Company | 2025 Revenue | 2025 Capex | 2026 Capex (Guided) | Key Risk Quote (from 10-K / SEC filing) | Risk Language New? | Gap Assessment |
|---------|-------------|-----------|--------------------|-----------------------------------------|-------------------|----------------|
| **Alphabet** | $403B | $91-93B | $175-185B | "To meet the compute capacity demands of AI training and inference... we are entering into significant leasing arrangements with third party operators, which may increase costs and operational complexity." Also flagged risk of AI cannibalizing search/ads business and potential "excess capacity" from costly commitments. | Yes -- first time AI cannibalization of search/ads appeared in filing | **SEVERE.** Spending $180B to build AI that they simultaneously warn could destroy their $330B/yr ad business. The company building AI is telling the SEC that AI might kill the thing that pays for AI. |
| **Microsoft** | $282B | $91-93B | $120B+ | "We are incurring significant costs to build and maintain infrastructure to support cloud-based and AI services, reducing operating margins. It is uncertain whether our strategies will continue to attract users or generate the revenue required to succeed." | Partially new -- infrastructure cost language expanded significantly in FY2025 filing | **HIGH.** Spending 43% of revenue on AI capex while admitting it's "uncertain" whether strategies will "generate the revenue required to succeed." |
| **Meta** | $201B | $72B | $115-135B | "There are significant risks involved in developing and deploying AI and there can be no assurance that the usage of AI will enhance our products or services or be beneficial to our business, including our efficiency or profitability." | Expanded in 2025 filing -- "no assurance" language is stronger than prior years | **HIGH.** Spending 60%+ of revenue on AI capex with "no assurance" it will be "beneficial to our business." |
| **Amazon** | $717B | $128B | $200B | Expects AI infrastructure spending to "increase over time, which can negatively impact short-term free cash flow." Shortened useful lives of AI servers from 6 to 5 years due to "increased pace of technology development, particularly in artificial intelligence." Acknowledges demand fluctuation risks alongside capital intensity. | Partially new -- server useful life reduction and AI-specific infrastructure language are new | **HIGH.** Spending $200B in 2026 while simultaneously writing down asset lives faster because AI hardware obsolesces quicker. Building infrastructure they expect to depreciate 20% faster. |
| **NVIDIA** | $216B (FY2026, ended Jan 2026) | N/A (fabless; customers' capex is NVIDIA's revenue) | N/A | "Demand estimates for our products, applications, and services can be incorrect and create volatility in our revenue or supply levels." Two customers = 39% of revenue; four customers = 61%. | Consistent language, but customer concentration has intensified | **CRITICAL (different axis).** NVIDIA doesn't spend the capex -- it *is* the capex. If the four hyperscalers above reconsider their spending, NVIDIA's $216B revenue is the first casualty. 61% customer concentration makes it a leveraged bet on four companies' AI conviction. |

---

## 2. Combined Capex

### 2025 Actual (Four Hyperscalers)

| Company | 2025 Capex |
|---------|-----------|
| Amazon | $128B |
| Alphabet | $92B (midpoint) |
| Microsoft | $92B (midpoint) |
| Meta | $72B |
| **Total** | **$384B** |

### 2026 Guided (Four Hyperscalers)

| Company | 2026 Capex (midpoint) |
|---------|-----------------------|
| Amazon | $200B |
| Alphabet | $180B (midpoint of $175-185B) |
| Meta | $125B (midpoint of $115-135B) |
| Microsoft | $120B+ |
| **Total** | **$625B+** |

**Year-over-year increase: ~$241B (+63%)**

For context: $625B is more than the GDP of Sweden ($600B), Belgium ($600B), or Thailand ($530B). Four companies plan to spend more on AI data centers in one year than the entire economic output of a G20-adjacent nation.

---

## 3. Gap Severity Ranking

Ranking by how dramatic the contrast is between spending commitment and self-reported risk:

### Rank 1: Alphabet (MOST SEVERE)

- **The gap:** Spending $180B on AI while warning that AI could cannibalize the search/ads business that generates 77% of total revenue ($330B of $403B). This is the only company in the group whose 10-K explicitly warns that its AI investment could destroy its primary revenue source.
- **Capex as % of revenue:** 45% (2026 guided vs 2025 revenue)
- **The paradox:** Building the weapon that might kill the cash cow.

### Rank 2: Meta (SEVERE)

- **The gap:** Spending $125B with "no assurance" that AI will "enhance our products or services or be beneficial to our business, including our efficiency or profitability." The language is absolute -- not "limited assurance" or "some risk," but "no assurance."
- **Capex as % of revenue:** 62% (2026 guided vs 2025 revenue)
- **The paradox:** Highest capex-to-revenue ratio in the group. Spending 62 cents of every revenue dollar on something the filing says might not work.

### Rank 3: Microsoft (HIGH)

- **The gap:** Spending $120B+ while stating it is "uncertain" whether strategies will "generate the revenue required to succeed." The word "uncertain" in an SEC filing from the world's most valuable company is not casual.
- **Capex as % of revenue:** 43% (2026 guided vs 2025 revenue)
- **The paradox:** The company that owns the AI distribution channel (Azure, Office, GitHub) still can't promise the math works.

### Rank 4: Amazon (HIGH)

- **The gap:** Spending $200B while simultaneously shortening the useful life of AI servers from 6 to 5 years. They're building faster AND writing it off faster. Free cash flow may go negative in 2026.
- **Capex as % of revenue:** 28% (2026 guided vs 2025 revenue)
- **The paradox:** Largest absolute spender. Only company where the filing suggests the hardware itself is obsolescing faster than expected.

### Rank 5: NVIDIA (STRUCTURAL)

- **The gap:** Different axis entirely. NVIDIA's risk is that 61% of its revenue comes from four customers who are all making the same bet. If any of them flinch, NVIDIA's $216B revenue collapses.
- **The paradox:** The company profiting most from the AI boom is the most exposed to a single coordinated pullback.

---

## 4. The Single Most Dramatic Data Point

**Meta plans to spend 62% of its annual revenue on AI infrastructure in 2026. Its own 10-K says there is "no assurance" this investment will be "beneficial to our business."**

Why this is the one:

- The ratio is visceral. 62 cents of every dollar. Not capex-to-profit, capex-to-*revenue*. Before any costs.
- The quote is unambiguous. "No assurance" is the SEC's version of "we have no idea if this works."
- The contrast is binary. The press release says "Meta Superintelligence Labs." The 10-K says "no assurance."
- David Kwon stops scrolling because this reframes the entire AI narrative. It's not "will AI work?" -- it's "the companies building AI are telling the SEC they don't know."

**Runner-up:** Alphabet warning that AI could cannibalize its own search business while spending $180B on AI. This is the philosophical version of the same gap -- building the thing that might destroy you.

**Combined hook:** "Five companies plan to spend $625 billion on AI infrastructure in 2026. Their own SEC filings say it might not work."

---

## 5. Anchoring Ratios

### Capex as % of Revenue (2026 guided capex / 2025 actual revenue)

| Company | Ratio | Interpretation |
|---------|-------|----------------|
| Meta | 62% | Highest. Spending more than half of revenue on AI infra. |
| Alphabet | 45% | Nearly half of revenue going to capex. |
| Microsoft | 43% | Similar to Alphabet despite lower absolute number. |
| Amazon | 28% | Lowest ratio, but highest absolute number ($200B). |
| NVIDIA | N/A | Revenue-side of the equation, not the spender. |

### Capex Per Employee (2026 guided capex / 2025 headcount)

| Company | Employees | Capex/Employee | Interpretation |
|---------|-----------|----------------|----------------|
| Meta | 78,800 | $1.59M | Each employee's job is justified by ~$1.6M in infrastructure. |
| Alphabet | 190,820 | $943K | Just under $1M per head. |
| Amazon | 1,600,000 | $125K | Misleading -- most employees are warehouse/logistics. For 320K white-collar: $625K/employee. |
| Microsoft | 228,000 | $526K | Most "reasonable" ratio, still over half a million per person. |

### AI Capex vs AI Revenue (the ROI gap)

Per Futurum Group analysis: pure-play AI vendors' combined revenue (~$35B projected) represents less than 5% of the infrastructure investment being deployed. The industry is spending $20 for every $1 of AI-specific revenue.

### The "GDP Test"

- $625B combined 2026 capex > GDP of Sweden, Belgium, Poland, or Thailand
- $625B = roughly 2.3% of US GDP ($27T) being spent by four companies on one technology
- The four hyperscalers' 2026 AI capex exceeds the entire US federal R&D budget (~$200B)

### Year-Over-Year Capex Acceleration

| Company | 2025 Capex | 2026 Capex (mid) | YoY Increase | % Increase |
|---------|-----------|-----------------|-------------|-----------|
| Amazon | $128B | $200B | +$72B | +56% |
| Alphabet | $92B | $180B | +$88B | +96% |
| Meta | $72B | $125B | +$53B | +74% |
| Microsoft | $92B | $120B | +$28B | +30% |
| **Total** | **$384B** | **$625B** | **+$241B** | **+63%** |

Alphabet's 96% YoY increase is the most aggressive acceleration. Microsoft's 30% is the most restrained.

### Infrastructure Payback Timeline

Per industry analysis: "Infrastructure built today may take 18-36 months to generate proportional returns." At current spending rates, the 2026 infrastructure won't break even until mid-2028 at earliest.

---

## 6. Supplementary Context

### The S&P 500 AI Risk Disclosure Wave

Per Harvard Law / Conference Board study:
- **2023:** 12% of S&P 500 companies disclosed AI as a material risk
- **2025:** 72% of S&P 500 companies disclose AI as a material risk
- That's a 6x increase in two years
- Top risk category: reputational risk from AI failures (38% of disclosing firms)
- SEC has made AI disclosure a top examination priority for 2026

### What This Means for the Article

The story isn't just about five companies. It's about a market-wide phenomenon where the companies building AI are simultaneously telling regulators it might not work. The gap between press-release optimism and SEC-mandated candor is the story.

### Key Limitation

I could not access the actual 10-K PDFs or HTML filings from SEC EDGAR due to automated access restrictions. The quotes used here come from verified secondary sources (CNBC, ActualTech Media, Seeking Alpha, Futurum Group) that cited the filings directly. The Editor should link to the original EDGAR filings for each company so readers can verify.

---

## Sources

- Alphabet 10-K (FY2025): EDGAR CIK 1652044, filed Feb 2026
- Microsoft 10-K (FY2025): EDGAR CIK 789019, filed Jul 2025
- Meta 10-K (FY2025): EDGAR CIK 1326801, filed Jan 2026
- Amazon 10-K (FY2025): EDGAR CIK 1018724, filed Feb 2026
- NVIDIA 10-K (FY2025): EDGAR CIK 1045810, filed Mar 2025
- Harvard Law / Conference Board: "AI Risk Disclosures in the S&P 500" (Oct 2025)
- arxiv 2508.19313: "Are Companies Taking AI Risks Seriously?"
- Futurum Group: "AI Capex 2026: The $690B Infrastructure Sprint"
- ActualTech Media: "The AI Risk Factors: What Tech Giants Tell Investors in 10-K Filings"
