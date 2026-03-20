# OpenAI io Products Acquisition: Unit Economics Analysis

**Article:** [$6.5 Billion for Zero Products](https://cupellabs.veron3.space/article/6-5-billion-for-zero-products)

## What this is

Quantitative analysis of OpenAI's $6.5 billion acquisition of io Products. Compares acquisition cost per employee against historical tech hardware deals, stress-tests unit economics across price, volume, and margin scenarios, and benchmarks the first-year sales target against every comparable hardware launch.

## Files

- `io-products-economics.py` — Python script that produces all calculations and tables
- `findings.md` — Full analysis output with all numbers, scenarios, and comparisons

## How to reproduce

```bash
python3 io-products-economics.py
```

No external dependencies. No datasets to download. The script uses publicly reported acquisition prices, employee counts, and unit sales estimates compiled from SEC filings, IDC, Counterpoint Research, Strategy Analytics, CIRP, and Qualcomm investor disclosures.

## Key findings

- OpenAI paid $118.2M per employee, 5.9x the next most expensive comparable deal (Meta/Oculus at $20M)
- The 45M first-year unit target is 3x AirPods and 4x all AI hardware products combined
- Even at the target scenario ($249, 45M units, 45% margin), gross profit covers only 78% of acquisition cost
- At realistic first-gen volumes (5-15M units), payback stretches to 4-16 years
- No first-generation product from a new-to-hardware company has ever sold 40M+ units in year one
