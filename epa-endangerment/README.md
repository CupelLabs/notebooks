# EPA Endangerment Finding Rescission: Analysis

## What this is

Analysis of the EPA's Regulatory Impact Analysis (EPA-420-R-26-002) for the rescission of the Greenhouse Gas Endangerment Finding, published February 2026. The EPA's fact sheet claims $1.3 trillion in savings. The RIA's primary scenario shows a $180 billion net cost.

## Source documents

- **RIA:** EPA-420-R-26-002 (35 pages). [Download from EPA](https://nepis.epa.gov/Exe/ZyPDF.cgi?Dockey=P101HV06.pdf)
- **Fact sheet:** EPA-420-F-26-002. [Download from EPA](https://www.epa.gov/system/files/documents/2026-03/420f26002.pdf)
- **Federal Register final rule:** 91 FR 7686 (111 pages). [View on Federal Register](https://www.federalregister.gov/documents/2026/02/18/2026-03157/rescission-of-the-greenhouse-gas-endangerment-finding-and-motor-vehicle-greenhouse-gas-emission)

## How to reproduce

```bash
pip install pandas openpyxl
python extract_ria_tables.py
```

The script extracts tables from the RIA text, computes the fact sheet vs. RIA contradiction, and exports intermediate CSVs/JSONs. Source PDFs are not included (download from URLs above). The text extraction (`ria-text.txt`) was generated from the PDF using standard PDF-to-text tools.

## Files

- `extract_ria_tables.py` — Analysis script
- `findings.md` — Structured findings with cross-checks
- `*.csv` / `*.json` — Intermediate computed data (scenario summaries, per-vehicle breakdowns, assumption impact analysis)

## Key finding

The EPA fact sheet reports $1.3 trillion in gross savings (vehicle technology + EVSE). The RIA's Scenario A1 (AEO 2025 Reference case, full lifetime fuel costs, 3% discount rate) shows those savings are offset by $1.47 trillion in costs (fuel, repair, maintenance, insurance, congestion, noise). Net impact: -$180 billion.
