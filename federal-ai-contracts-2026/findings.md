# Federal AI Contract Analysis: Findings

**Date:** 2026-03-20
**Analyst:** Analyzer
**Script:** `scripts/analyze_contracts.py`
**Data:** 573 unique contracts, $2.12B total, from USAspending.gov API keyword search (2014-2026)

---

## Finding 1: The Pentagon gets 69 cents of every federal AI dollar

- **Number:** DoD: $1.47B (69.3%). Civilian agencies: $650M (30.7%). Within DoD, the Army dominates at $674M (45.9% of DoD, 31.8% of total), followed by Air Force $281M (19.1%) and DARPA $106M (7.2%).
- **Script:** `scripts/analyze_contracts.py` -- Q1 section
- **Confidence:** HIGH
- **Caveats:** Keyword search may miss classified or obliquely described DoD contracts. Civilian agencies may also use AI without labeling it as such. This likely understates DoD's true share.

## Finding 2: Five companies get a third of all federal AI money

- **Number:** Top 5 recipients = $689M (32.5%). Top 10 = $949M (44.8%). Top 20 = $1.15B (54.5%). Total unique recipients: 378. The #1 recipient (ECS Federal) holds 12% of all federal AI contract value across just 3 contracts.
- **Script:** `scripts/analyze_contracts.py` -- Q2 section
- **Confidence:** HIGH
- **Caveats:** Some recipients may be subsidiaries of the same parent company. Concentration could be even higher when accounting for corporate structure.

## Finding 3: OpenAI, Anthropic, Google, Microsoft, Amazon, Meta, and NVIDIA have zero direct federal AI contracts

- **Number:** Zero. None of the major AI labs or hyperscalers appear as direct recipients. The money goes to federal IT contractors: ECS Federal ($255M), Tuknik ($128M), Accenture Federal Services ($94M). The only "AI company" in the top 5 is Scale AI ($108M) and Palantir ($104M).
- **Script:** `scripts/analyze_contracts.py` -- Q7 section
- **Confidence:** HIGH
- **Caveats:** These companies may be subcontractors. Microsoft Azure, AWS, and Google Cloud almost certainly provide infrastructure under prime contracts held by integrators. The data shows who signs the contract, not who does the work.

## Finding 4: The 2020 spike is real and concentrated

- **Number:** 2020: $664M across 83 contracts (31.3% of all-time total). Driven by 4 mega-contracts: ECS Federal $119M (Army AI/ML prototypes), Tuknik $107M (JAIC support), Scale AI $106M (Army ML testing), Palantir $91M (Army AI defense use cases). After 2020, spending dropped to $149M (2021) before recovering to $256M (2024).
- **Script:** `scripts/analyze_contracts.py` -- Q3 section
- **Confidence:** HIGH
- **Caveats:** The 2020 spike aligns with the Joint AI Center (JAIC) push under the first Trump administration. The drop in 2021 may reflect procurement cycles, not a policy retreat.

## Finding 5: Most contracts are legitimately AI-related, not buzzword-stuffed IT services

- **Number:** 447 of 573 contracts (78%) mention specific AI technologies (machine learning, deep learning, neural networks, NLP, computer vision, autonomous systems). Only 3 contracts matched the "AI buzzword on generic IT services" pattern. 35 contracts (2.5% of value) were unclear.
- **Script:** `scripts/analyze_contracts.py` -- Q4 section
- **Confidence:** MEDIUM
- **Caveats:** Description analysis is keyword-based. A contract can mention "machine learning" without the actual work being meaningfully AI. The descriptions are government procurement language, not technical specifications. "Develop AI/ML prototypes" could mean anything from cutting-edge research to basic data dashboards.

## Finding 6: Contract size is bimodal -- lots of small, a few enormous

- **Number:** 290 contracts (50.6%) are under $1M, totaling just $75M (3.5%). Meanwhile, 6 contracts (1%) are over $50M and account for $587M (27.7%). Median contract: $984K. Mean: $3.7M. The top 3 contracts alone ($119M + $107M + $106M) represent 15.6% of all federal AI spending.
- **Script:** `scripts/analyze_contracts.py` -- Q6 section
- **Confidence:** HIGH
- **Caveats:** None. Distribution is clear in the data.

## Finding 7: The traditional defense primes barely show up

- **Number:** Lockheed Martin: $6.2M (3 contracts). Raytheon/RTX: $31M (5 contracts, mostly through BBN Technologies). Northrop Grumman: $15.4M (2 contracts). General Dynamics: $1.1M (1 contract). BAE Systems: $13M (3 contracts). Combined defense primes: ~$67M (3.2% of total). The money is going to mid-tier federal IT integrators and a handful of AI-native companies, not the Big Five defense contractors.
- **Script:** `scripts/analyze_contracts.py` -- Q7 section
- **Confidence:** MEDIUM
- **Caveats:** Defense primes may conduct AI work under broader contracts not specifically labeled "AI." Their AI spending may be embedded in weapons systems contracts that don't surface in keyword searches.

---

## Overall Assessment

**The thesis is partially confirmed but more nuanced than expected.**

DoD dominance (69%) confirmed exactly. Concentration confirmed (top 5 = 33%). But the "same defense contractors" claim is wrong -- the traditional primes (Lockheed, Raytheon, Northrop) are barely present. Instead, a new class of federal AI contractor has emerged: mid-tier IT integrators (ECS Federal, Tuknik, Accenture Federal Services) and AI-native companies (Scale AI, Palantir). The major AI labs (OpenAI, Anthropic, Google, etc.) are completely absent as direct recipients.

The most interesting finding is #3: the companies building the most capable AI in the world have zero direct federal AI contracts. The government buys AI through middlemen.

**What the data does NOT tell us:** Subcontractor relationships, classified spending, how much of these contracts involves actual AI vs. AI-adjacent IT work, and whether the "AI" label is applied strategically for funding purposes.

## Limitations

- Data pulled via keyword search of USAspending.gov API. Not all AI contracts use these keywords.
- API returned max 100 results per query with no reliable total count (pagination metadata showed 0).
- NAICS codes were not populated in the API response (100% null), limiting industry categorization.
- Classified contracts are not in this database.
- We cannot determine subcontractor relationships from this data.
