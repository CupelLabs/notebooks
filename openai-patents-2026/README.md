# OpenAI Patent Analysis (2023-2025)

Data and analysis behind [62 Patents. Zero Hardware.](https://cupellabs.veron3.space/62-patents-zero-hardware)

## What's here

| File | What it contains |
|------|-----------------|
| `query.sql` | The BigQuery query used to pull all OpenAI patents |
| `summary.json` | Aggregated stats: total count, granted vs applications, CPC breakdown, inventor count |
| `categories.json` | Patents grouped by CPC technology domain |

## How to reproduce

1. Open [Google BigQuery](https://console.cloud.google.com/bigquery) (free tier: 1TB/month)
2. Run `query.sql` against the `patents-public-data` dataset
3. You'll get ~106 results. We cleaned to 62 by filtering out non-OpenAI entities caught by fuzzy name matching (e.g., companies with "openai" as a substring in their assignee name)

## What's NOT here

The full patent JSON (62 records with titles, abstracts, inventors, and CPC codes) is not published to keep the repo lightweight. The summary and category files contain everything referenced in the post.

The cleanup pipeline (assignee filtering logic, audit decisions) is internal tooling and not published.

## Limitations

- BigQuery lags USPTO by 1-4 weeks
- Acquired patents may not appear under OpenAI's assignee name
- 39 of 62 filings are applications that may never be granted
- Analysis covers bibliographic data and abstracts only, not full patent descriptions
