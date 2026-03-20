"""
Fetch federal AI-related contract awards from USAspending.gov API.
Searches for AI keywords in contract descriptions, FY2020-2026.
"""

import requests
import json
import csv
import time
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(SCRIPT_DIR, 'raw')
os.makedirs(RAW_DIR, exist_ok=True)

API_URL = 'https://api.usaspending.gov/api/v2/search/spending_by_award/'

KEYWORDS = [
	'artificial intelligence',
	'machine learning',
	'natural language processing',
	'computer vision',
	'autonomous systems',
	'deep learning',
	'neural network',
	'large language model',
]

# Contract award types: A=BPA, B=Purchase Order, C=Delivery Order, D=Definitive Contract
AWARD_TYPES = ['A', 'B', 'C', 'D']

FIELDS = [
	'Award ID',
	'Recipient Name',
	'Description',
	'Start Date',
	'End Date',
	'Award Amount',
	'Total Outlays',
	'Awarding Agency',
	'Awarding Sub Agency',
	'Contract Award Type',
	'NAICS Code',
	'NAICS Description',
	'PSC Code',
]

all_results = []

for keyword in KEYWORDS:
	print(f"\n--- Searching: '{keyword}' ---")
	page = 1
	keyword_count = 0
	last_id = None
	last_sort = None

	while True:
		payload = {
			'filters': {
				'keywords': [keyword],
				'award_type_codes': AWARD_TYPES,
				'time_period': [
					{'start_date': '2020-01-01', 'end_date': '2026-12-31'}
				],
			},
			'fields': FIELDS,
			'page': page,
			'limit': 100,
			'sort': 'Award Amount',
			'order': 'desc',
		}

		# Use cursor-based pagination if available
		if last_id and last_sort:
			payload['last_record_unique_id'] = last_id
			payload['last_record_sort_value'] = last_sort

		try:
			resp = requests.post(API_URL, json=payload, timeout=60)
			resp.raise_for_status()
			data = resp.json()
		except Exception as e:
			print(f"  Error on page {page}: {e}")
			break

		results = data.get('results', [])
		if not results:
			break

		for r in results:
			r['_search_keyword'] = keyword
		all_results.extend(results)
		keyword_count += len(results)

		meta = data.get('page_metadata', {})
		total = meta.get('total', 0)
		has_next = meta.get('hasNext', False)
		last_id = meta.get('last_record_unique_id')
		last_sort = meta.get('last_record_sort_value')

		print(f"  Page {page}: {len(results)} results (total available: {total})")

		# Cap at 1000 per keyword to keep manageable
		if not has_next or page * 100 >= min(total, 1000):
			if total > 1000:
				print(f"  Capped at 1000 of {total} results")
			break

		page += 1
		time.sleep(0.3)

	print(f"  Total for '{keyword}': {keyword_count}")

print(f"\n\n=== TOTAL RAW RESULTS: {len(all_results)} ===")

# Deduplicate by Award ID
seen = set()
unique = []
for r in all_results:
	aid = r.get('Award ID', '')
	if aid and aid not in seen:
		seen.add(aid)
		unique.append(r)
	elif not aid:
		unique.append(r)

print(f"After dedup by Award ID: {len(unique)}")

# Save raw JSON
json_path = os.path.join(RAW_DIR, 'ai_contracts_raw.json')
with open(json_path, 'w') as f:
	json.dump(unique, f, indent=2)
print(f"Saved: {json_path}")

# Save as CSV
csv_path = os.path.join(RAW_DIR, 'ai_contracts.csv')
if unique:
	fieldnames = list(unique[0].keys())
	with open(csv_path, 'w', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(unique)
	print(f"Saved: {csv_path}")

# Quick summary
print("\n=== QUICK SUMMARY ===")
agencies = {}
recipients = {}
total_amount = 0
years = {}
for r in unique:
	agency = r.get('Awarding Agency', 'Unknown')
	recipient = r.get('Recipient Name', 'Unknown')
	amount = r.get('Award Amount', 0) or 0
	start = r.get('Start Date', '')
	year = start[:4] if start else 'Unknown'

	agencies[agency] = agencies.get(agency, 0) + amount
	recipients[recipient] = recipients.get(recipient, 0) + amount
	years[year] = years.get(year, 0) + amount
	total_amount += amount

print(f"\nTotal contract value: ${total_amount:,.0f}")
print(f"Unique contracts: {len(unique)}")
print(f"Unique agencies: {len(agencies)}")
print(f"Unique recipients: {len(recipients)}")

print("\nBy year:")
for year in sorted(years.keys()):
	print(f"  {year}: ${years[year]:,.0f}")

print("\nTop 15 agencies by contract value:")
for agency, amt in sorted(agencies.items(), key=lambda x: -x[1])[:15]:
	count = sum(1 for r in unique if r.get('Awarding Agency') == agency)
	print(f"  {agency}: ${amt:,.0f} ({count} contracts)")

print("\nTop 20 recipients by contract value:")
for recip, amt in sorted(recipients.items(), key=lambda x: -x[1])[:20]:
	count = sum(1 for r in unique if r.get('Recipient Name') == recip)
	print(f"  {recip}: ${amt:,.0f} ({count} contracts)")

print("\nDone.")
