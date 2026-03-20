# Federal AI Contracts (2020-2026)

Data and analysis behind [The Government Buys AI Through Middlemen](https://cupellabs.veron3.space/federal-ai-contracts-middleman-economy).

## What's here

| File | Description |
|------|-------------|
| `fetch_ai_contracts.py` | Pulls AI-related contracts from the USAspending.gov API |
| `ai_contracts.csv` | 573 deduplicated contracts, $2.12B total |
| `analyze_contracts.py` | Full analysis: agency breakdown, recipient concentration, yearly trends, description categorization |
| `findings.md` | Plain-English summary of every finding with confidence levels |

## Data source

[USAspending.gov API](https://api.usaspending.gov). Keyword search across 8 AI-related terms (artificial intelligence, machine learning, deep learning, neural network, NLP, computer vision, autonomous systems, large language model). Contract awards only, 2020-2026.

## Reproduce

```bash
# Pull fresh data from the API
python3 fetch_ai_contracts.py

# Run the analysis
python3 analyze_contracts.py
```

Requires `pandas`. The fetch script hits the live API and may return different results as new contracts are awarded.

## Key findings

- DoD: $1.47B (69.3% of all federal AI contract value)
- Top 5 recipients hold 32.5% of total ($689M)
- OpenAI, Anthropic, Google, Microsoft, Amazon, Meta, NVIDIA: zero direct contracts
- 2020 JAIC spike: $664M in one year, driven by 4 mega-contracts
