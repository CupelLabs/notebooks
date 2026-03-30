# Student Loan Servicer Complaint Analysis

Analysis of CFPB student loan complaints around major servicer transitions and the federal payment restart.

## Article
[MOHELA Had 63 Complaints. Now It Has 7,000.](https://cupellabs.veron3.space/mohela-had-63-complaints-now-it-has-7000)

## Data Source
- CFPB Consumer Complaint Database API
- Product filter: "Student loan"
- Date range: January 2018 - March 2026
- 83,680 total complaints, 63,111 federal

## How to Reproduce

1. Run `download_complaints.py` (in the article experiment directory) to fetch data from the CFPB API
2. Run `analyze_servicer_transitions.py` against the downloaded CSV

The analysis script reads from a local CSV and outputs intermediate aggregations. The CFPB API is public and requires no authentication.

## Files
- `analyze_servicer_transitions.py` - Main analysis script
- `findings.md` - Key findings with cross-checks
- `monthly_complaints_by_servicer.csv` - Monthly complaint counts per servicer
- `monthly_total_complaints.csv` - Monthly total federal student loan complaints
- `yearly_complaints_by_servicer.csv` - Yearly totals per servicer
- `response_by_servicer.csv` - Company response types by servicer
- `summary.json` - Summary statistics
