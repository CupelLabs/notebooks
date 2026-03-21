## Dataset: FOIA.gov Annual Report Data (All Agencies)
- **Source:** https://www.foia.gov/foia-dataset-download.html
- **Downloaded:** 2026-03-21
- **Format:** CSV (32 files per fiscal year, inside ZIP archives)
- **Date range:** FY2018 through FY2024 (7 fiscal years)
- **Agency count:** 118-123 agencies per year (varies slightly as agencies are created/merged), plus "All agencies" total row
- **Total file size:** ~5.5 MB uncompressed across all years
- **ZIP archives:** ~870 KB total (7 ZIP files, ~125 KB each)

## Download URLs
CSV archives: `https://www.foia.gov/downloads/all_agencies_csv_[YEAR].zip`
XML archives: `https://www.foia.gov/[YEAR]-FOIASetFull.zip`
(We downloaded CSV only. XML is available at those URLs if needed.)

## Files (32 CSVs per year)

Each year's ZIP extracts to 32 CSV files. Key files for this analysis:

### Processing Times
- `foia-processed-requests-response-time-for-all-processed-perfected-requests.csv` - Median/avg/min/max days for simple, complex, and expedited requests. **This is the core file for response time analysis.**
- `foia-processed-requests-response-time-for-perfected-requests-in-which-information-was-granted.csv` - Same metrics but only for requests where information was actually granted.
- `foia-processed-requests-response-time-in-day-increments-simple-requests.csv` - Distribution of simple request processing times in day buckets (1-20, 21-40, ..., 401+).
- `foia-processed-requests-response-time-in-day-increments-complex-requests.csv` - Same distribution for complex requests.
- `foia-processed-requests-response-time-in-day-increments-requests-granted-expedited-processing.csv` - Same for expedited processing.

### Request Volumes and Disposition
- `foia-received-processed-and-pending-foia-requests.csv` - Requests pending at start, received, processed, pending at end. **Core volume file.**
- `foia-disposition-of-foia-requests-all-processed-requests.csv` - How requests were resolved: full grants, partial grants/denials, full denials, no records, withdrawn, fee-related, etc.
- `foia-disposition-of-foia-requests-other-reasons.csv` - Breakdown of "other" disposition reasons.

### Exemption Usage
- `foia-disposition-of-foia-requests-number-of-times-exemptions-applied.csv` - Count of each FOIA exemption invoked: Ex.1 (national security), Ex.2 (internal rules), Ex.3 (statutory), Ex.4 (trade secrets), Ex.5 (deliberative process), Ex.6 (privacy), Ex.7A-F (law enforcement), Ex.8 (financial), Ex.9 (geological). **Core exemption file.**

### Backlogs
- `foia-backlogs-of-foia-requests-and-administrative-appeals.csv` - Backlog count at end of fiscal year. **Core backlog file.**
- `foia-comparison-of-backlogged-requests-from-previous-year-and-current-year-annual-report.csv` - Year-over-year backlog comparison.
- `foia-comparison-of-backlogged-administrative-appeals-from-previous-year-and-current-year-annual-report.csv` - Same for appeals.

### Pending Requests
- `foia-pending-requests-all-pending-perfected-requests.csv` - Number pending and median/avg days for simple, complex, expedited.
- `foia-pending-requests-ten-oldest-pending-perfected-requests.csv` - The 10 oldest pending requests per agency with dates and days pending. **Good for identifying worst-case stonewalling.**

### Appeals
- `foia-received-processed-and-pending-administrative-appeals.csv` - Appeal volumes.
- `foia-disposition-of-administrative-appeals-all-processed-appeals.csv` - Appeal outcomes.
- `foia-response-time-for-administrative-appeals.csv` - Appeal processing times.
- `foia-ten-oldest-administrative-appeals.csv` - 10 oldest pending appeals per agency.
- `foia-reasons-for-denial-on-appeal-number-of-times-exemptions-applied.csv` - Exemptions cited on appeal.
- `foia-reasons-for-denial-on-appeal-other-reasons.csv` - Other denial reasons on appeal.
- `foia-reasons-for-denial-on-appeal-reasons-other-than-exemptions.csv` - Non-exemption denial reasons.

### Staffing and Costs
- `foia-foia-personnel.csv` - Full-time equivalent staff and total staff per agency.
- `foia-foia-costs-and-fees-collected-for-processing-requests.csv` - Processing costs, litigation costs, fees collected.

### Other
- `foia-requests-for-expedited-processing.csv` - Expedited processing requests granted/denied.
- `foia-requests-for-fee-waiver.csv` - Fee waiver requests granted/denied.
- `foia-consultations-on-foia-requests-received-processed-and-pending-consultations.csv` - Inter-agency consultations.
- `foia-consultations-on-foia-requests-ten-oldest-consultations-received-from-other-agencies-pending-at-agency.csv` - Oldest pending consultations.
- `foia-comparison-of-numbers-of-requests-from-previous-year-and-current-year-annual-report.csv` - YoY request comparison.
- `foia-comparison-of-numbers-of-administrative-appeals-from-previous-year-and-current-year-annual-report.csv` - YoY appeal comparison.
- `foia-number-of-subsection-a-postings.csv` - Proactive disclosures.
- `foia-number-of-times-subsection-c-used.csv` - Subsection (c) usage.
- `foia-exemption-statutes.csv` - Specific statutes cited for Exemption 3 (statutory exemptions). Large file (~140KB).

## Schema (common to all files)

Every CSV has these first three columns:
| Column | Type | Description |
|--------|------|-------------|
| Agency | string | Full agency name (e.g., "Department of Justice") |
| Component | string | Sub-component name, or "Agency Overall" for the agency-level total |
| Fiscal Year | int | The fiscal year (e.g., 2024 = Oct 2023 - Sep 2024) |

Remaining columns vary by file (see descriptions above). Numeric fields are quoted strings. Some contain "N/A" for not applicable, "<1" for less than one day.

## Supplementary: API Data

Additionally, 50 records were fetched from the FOIA.gov JSON API (`https://api.foia.gov/api/annual_foia_report?api_key=DEMO_KEY`) before rate limiting kicked in. These cover FY2019-2020 and contain 281 attributes per agency-year record (a superset of the CSV data). Saved as:
- `foia_annual_reports_all.json` (0.6 MB)
- `foia_annual_reports_all.csv` (0.1 MB)

The API data includes the same metrics in a different structure. The CSV bulk downloads are more complete (7 years vs 2) and should be the primary data source for analysis.

## What I Could NOT Find
- **FY2025 data:** Not yet published. FY2025 ends September 2025; reports typically published the following spring.
- **Sub-component breakdowns for all years:** The CSVs include sub-component data (Component != "Agency Overall"), but completeness varies. Some agencies report only at the agency level.
- **Actual request text or subjects:** The annual reports are statistical summaries. What requesters actually asked for is not in this dataset.
- **Timeliness compliance details:** Whether responses met the 20-business-day statutory deadline is not explicitly tracked as a boolean field. Must be inferred from processing time data.

## Data Quality Issues
- **Naming inconsistencies in ZIP archives:** Some years have files with " (1)" or " (2)" suffixes (likely browser download artifacts from whoever at DOJ packaged the ZIPs). These are duplicate copies of existing files and can be ignored.
- **N/A values:** Some agencies report "N/A" for metrics that don't apply (e.g., no expedited processing requests). These need to be handled as nulls, not zeros.
- **"<1" values:** Processing time fields sometimes contain "<1" (less than one day). Need to decide whether to treat as 0.5 or 1 for analysis.
- **Agency name variations:** Some agencies changed names across years (e.g., "Corporation for National and Community Service (operating as AmeriCorps)"). Need normalization.
- **Agency count varies:** 118-123 agencies per year. Agencies are created, merged, or removed. Year-over-year comparisons need to account for this.
- **Self-reported data:** All data is self-reported by the agencies themselves. There is no independent audit. Agencies have an incentive to underreport backlogs or overreport compliance.

## Directory Structure
```
raw/
  all_agencies_csv_2018.zip through all_agencies_csv_2024.zip  (original downloads)
  csv_2018/ through csv_2024/  (extracted CSVs, 32 files each)
  foia_annual_reports_all.json  (API data, 50 records, FY2019-2020)
  foia_annual_reports_all.csv   (API data in CSV format)
  fetch_foia_data.py            (API fetch script, rate-limited after 50 records)
  README.md                     (this file)
```
