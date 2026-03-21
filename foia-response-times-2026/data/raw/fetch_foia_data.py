#!/usr/bin/env python3
"""
Fetch all FOIA annual report data from api.foia.gov.
Uses DEMO_KEY. Downloads via curl to handle large responses,
then extracts only the 'data' portion (discarding 'included' relationship bloat).
"""

import json
import csv
import subprocess
import sys
import time
from pathlib import Path

BASE_URL = "https://api.foia.gov/api/annual_foia_report"
API_KEY = "DEMO_KEY"
OUTPUT_DIR = Path(__file__).parent
PAGE_SIZE = 50


def extract_value(val):
    """Some fields are dicts with 'value' key, others are plain."""
    if isinstance(val, dict):
        return val.get('value', '')
    return val


def fetch_page(offset=0, retries=3):
    """Fetch one page via curl (handles large responses better than urllib)."""
    url = (
        f"{BASE_URL}?api_key={API_KEY}"
        f"&page%5Blimit%5D={PAGE_SIZE}"
        f"&page%5Boffset%5D={offset}"
    )
    for attempt in range(retries):
        try:
            result = subprocess.run(
                ['curl', '-s', '--max-time', '180', url],
                capture_output=True, text=True, timeout=200
            )
            if result.returncode != 0:
                raise RuntimeError(f"curl failed: {result.stderr}")
            data = json.loads(result.stdout)
            return data
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}", file=sys.stderr)
            if attempt < retries - 1:
                time.sleep(3)
            else:
                raise


def main():
    all_records = []
    offset = 0

    print("Fetching FOIA annual report data from api.foia.gov...")

    while True:
        print(f"  Fetching offset={offset}...", end=' ', flush=True)
        data = fetch_page(offset)
        records = data.get('data', [])
        print(f"got {len(records)} records")

        if not records:
            break

        for rec in records:
            attrs = rec.get('attributes', {})
            row = {}
            row['id'] = rec.get('id', '')
            for key, val in attrs.items():
                row[key] = extract_value(val)
            all_records.append(row)

        # Check for next page
        links = data.get('links', {})
        if 'next' not in links:
            print("  No more pages.")
            break

        offset += PAGE_SIZE
        # Rate limit: DEMO_KEY allows 30 requests/hr on api.data.gov
        # But foia.gov may have different limits. Be conservative.
        time.sleep(2)

    print(f"\nTotal records fetched: {len(all_records)}")

    if not all_records:
        print("ERROR: No records fetched!", file=sys.stderr)
        sys.exit(1)

    # Get all unique keys
    all_keys = set()
    for rec in all_records:
        all_keys.update(rec.keys())
    sorted_keys = sorted(all_keys)

    # Save full JSON
    json_path = OUTPUT_DIR / "foia_annual_reports_all.json"
    with open(json_path, 'w') as f:
        json.dump(all_records, f, indent=2)
    size_mb = json_path.stat().st_size / 1024 / 1024
    print(f"Saved JSON: {json_path} ({size_mb:.1f} MB)")

    # Save as CSV
    csv_path = OUTPUT_DIR / "foia_annual_reports_all.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=sorted_keys)
        writer.writeheader()
        writer.writerows(all_records)
    size_mb = csv_path.stat().st_size / 1024 / 1024
    print(f"Saved CSV: {csv_path} ({size_mb:.1f} MB)")

    # Print summary
    years = set()
    agencies = set()
    for rec in all_records:
        yr = rec.get('field_foia_annual_report_yr')
        abbr = rec.get('field_agency_abbr', '')
        if not abbr:
            title = rec.get('title', '')
            abbr = title.split(' - ')[0] if ' - ' in title else title
        if yr:
            years.add(yr)
        if abbr:
            agencies.add(abbr)

    print(f"\nSummary:")
    print(f"  Years covered: {sorted(years)}")
    print(f"  Unique agencies: {len(agencies)}")
    print(f"  Sample agencies: {sorted(agencies)[:20]}")
    print(f"  Records per year (approx): {len(all_records) / max(len(years), 1):.0f}")
    print(f"  Total attributes: {len(sorted_keys)}")


if __name__ == '__main__':
    main()
