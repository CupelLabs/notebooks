#!/usr/bin/env python3
"""
Comprehensive analysis of federal AI contract data from USAspending.gov.
Produces findings for Cupel Labs.

Data: 573 unique contracts pulled by keyword search.
Source: /home/erdal/cupellabs/analyzer/experiments/data/usaspending/raw/ai_contracts.csv
"""

import pandas as pd
import numpy as np
import json
import os
import re
from collections import Counter

# ── Config ──
DATA_CSV = "/home/erdal/cupellabs/analyzer/experiments/data/usaspending/raw/ai_contracts.csv"
DATA_JSON = "/home/erdal/cupellabs/analyzer/experiments/data/usaspending/raw/ai_contracts_raw.json"
OUTPUT_DIR = "/home/erdal/cupellabs/analyzer/experiments/usaspending-analysis"

# ── Load ──
print("=" * 80)
print("LOADING DATA")
print("=" * 80)
df = pd.read_csv(DATA_CSV)
print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")
print()

# Basic schema info
print("COLUMN TYPES AND NULLS:")
for col in df.columns:
	null_count = df[col].isnull().sum()
	dtype = df[col].dtype
	print(f"  {col}: {dtype}, {null_count} nulls ({null_count/len(df)*100:.1f}%)")
print()

# ── Clean ──
df['Award Amount'] = pd.to_numeric(df['Award Amount'], errors='coerce')
df['Total Outlays'] = pd.to_numeric(df['Total Outlays'], errors='coerce')
df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')
df['start_year'] = df['Start Date'].dt.year

total_value = df['Award Amount'].sum()
print(f"TOTAL CONTRACT VALUE: ${total_value:,.2f}")
print(f"  = ${total_value/1e9:.2f}B")
print()

# ── Check for duplicates ──
print("=" * 80)
print("DUPLICATE CHECK")
print("=" * 80)
dupes_award_id = df['Award ID'].duplicated().sum()
dupes_internal = df['internal_id'].duplicated().sum()
print(f"Duplicate Award IDs: {dupes_award_id}")
print(f"Duplicate internal_ids: {dupes_internal}")

# Check if same Award ID appears with different search keywords
if dupes_award_id > 0:
	dupe_ids = df[df['Award ID'].duplicated(keep=False)].sort_values('Award ID')
	print(f"\nContracts appearing under multiple search keywords:")
	for aid, group in dupe_ids.groupby('Award ID'):
		keywords = group['_search_keyword'].tolist()
		amount = group['Award Amount'].iloc[0]
		print(f"  {aid}: keywords={keywords}, amount=${amount:,.0f}")
	print()
	print(f"WARNING: {dupes_award_id} duplicate Award IDs found.")
	print("These are likely the same contract matched by multiple search keywords.")
	print("Deduplicating by Award ID, keeping first occurrence...")
	df_deduped = df.drop_duplicates(subset='Award ID', keep='first')
	print(f"Before dedup: {len(df)} rows, ${df['Award Amount'].sum():,.0f}")
	print(f"After dedup: {len(df_deduped)} rows, ${df_deduped['Award Amount'].sum():,.0f}")
	df = df_deduped
	total_value = df['Award Amount'].sum()
	print(f"Using deduplicated dataset: {len(df)} contracts, ${total_value/1e9:.2f}B")
else:
	print("No duplicates found.")
print()

# ── QUESTION 1: DoD vs Civilian ──
print("=" * 80)
print("Q1: DoD vs CIVILIAN AGENCY SPENDING")
print("=" * 80)
agency_spend = df.groupby('Awarding Agency')['Award Amount'].sum().sort_values(ascending=False)

# Identify DoD-related agencies
dod_keywords = ['defense', 'army', 'navy', 'air force', 'marine']
def is_dod(agency_name):
	name_lower = str(agency_name).lower()
	return any(k in name_lower for k in dod_keywords)

df['is_dod'] = df['Awarding Agency'].apply(is_dod)

dod_total = df[df['is_dod']]['Award Amount'].sum()
civilian_total = df[~df['is_dod']]['Award Amount'].sum()
dod_pct = dod_total / total_value * 100
civilian_pct = civilian_total / total_value * 100

print(f"DoD: ${dod_total:,.0f} ({dod_pct:.1f}%)")
print(f"Civilian: ${civilian_total:,.0f} ({civilian_pct:.1f}%)")
print()

print("DoD agencies breakdown:")
dod_agencies = df[df['is_dod']].groupby('Awarding Agency')['Award Amount'].sum().sort_values(ascending=False)
for agency, amount in dod_agencies.items():
	print(f"  {agency}: ${amount:,.0f} ({amount/total_value*100:.1f}%)")
print()

print("Top civilian agencies:")
civ_agencies = df[~df['is_dod']].groupby('Awarding Agency')['Award Amount'].sum().sort_values(ascending=False)
for agency, amount in civ_agencies.head(10).items():
	print(f"  {agency}: ${amount:,.0f} ({amount/total_value*100:.1f}%)")
print()

# ── QUESTION 1b: DoD sub-agencies ──
print("=" * 80)
print("Q1b: DoD SUB-AGENCY SPENDING")
print("=" * 80)
dod_sub = df[df['is_dod']].groupby('Awarding Sub Agency')['Award Amount'].sum().sort_values(ascending=False)
print("DoD sub-agency spending:")
for sub, amount in dod_sub.items():
	pct = amount / dod_total * 100
	count = len(df[(df['is_dod']) & (df['Awarding Sub Agency'] == sub)])
	print(f"  {sub}: ${amount:,.0f} ({pct:.1f}% of DoD, {amount/total_value*100:.1f}% of total) [{count} contracts]")
print()

# ── QUESTION 2: Top Recipients ──
print("=" * 80)
print("Q2: CONCENTRATION - TOP RECIPIENTS")
print("=" * 80)
recipient_spend = df.groupby('Recipient Name')['Award Amount'].sum().sort_values(ascending=False)
recipient_count = df.groupby('Recipient Name').size()

print("Top 20 recipients:")
for i, (name, amount) in enumerate(recipient_spend.head(20).items()):
	pct = amount / total_value * 100
	n_contracts = recipient_count.get(name, 0)
	print(f"  {i+1}. {name}: ${amount:,.0f} ({pct:.1f}%) [{n_contracts} contracts]")
print()

top5_total = recipient_spend.head(5).sum()
top10_total = recipient_spend.head(10).sum()
top20_total = recipient_spend.head(20).sum()
print(f"Top 5 recipients: ${top5_total:,.0f} ({top5_total/total_value*100:.1f}% of total)")
print(f"Top 10 recipients: ${top10_total:,.0f} ({top10_total/total_value*100:.1f}% of total)")
print(f"Top 20 recipients: ${top20_total:,.0f} ({top20_total/total_value*100:.1f}% of total)")
print(f"Total unique recipients: {len(recipient_spend)}")
print()

# ── QUESTION 3: Year-over-year trend ──
print("=" * 80)
print("Q3: YEAR-OVER-YEAR TREND")
print("=" * 80)
yearly = df.groupby('start_year').agg(
	total_value=('Award Amount', 'sum'),
	count=('Award Amount', 'count'),
	median_value=('Award Amount', 'median'),
	mean_value=('Award Amount', 'mean'),
).sort_index()

print("Year-by-year breakdown:")
for year, row in yearly.iterrows():
	if pd.notna(year):
		print(f"  {int(year)}: {int(row['count'])} contracts, "
			  f"total=${row['total_value']:,.0f} ({row['total_value']/total_value*100:.1f}%), "
			  f"median=${row['median_value']:,.0f}, mean=${row['mean_value']:,.0f}")
print()

# Deep dive into 2020 spike
print("2020 SPIKE DEEP DIVE:")
df_2020 = df[df['start_year'] == 2020].sort_values('Award Amount', ascending=False)
print(f"  2020 contracts: {len(df_2020)}")
print(f"  2020 total: ${df_2020['Award Amount'].sum():,.0f}")
print(f"  Top 2020 contracts:")
for _, row in df_2020.head(10).iterrows():
	print(f"    {row['Recipient Name']}: ${row['Award Amount']:,.0f}")
	print(f"      Agency: {row['Awarding Agency']} / {row['Awarding Sub Agency']}")
	desc = str(row['Description'])[:120]
	print(f"      Desc: {desc}")
print()

# ── QUESTION 4: What are the contracts actually for? ──
print("=" * 80)
print("Q4: CONTRACT DESCRIPTIONS - REAL AI OR BUZZWORDS?")
print("=" * 80)

# Categorize by description content
def categorize_contract(desc):
	desc = str(desc).upper()
	categories = []

	# Strong AI indicators
	if any(term in desc for term in ['MACHINE LEARNING', 'DEEP LEARNING', 'NEURAL NETWORK',
		'NATURAL LANGUAGE PROCESSING', 'NLP', 'COMPUTER VISION',
		'AUTONOMOUS', 'PREDICTIVE MODEL', 'ALGORITHM']):
		categories.append('SPECIFIC_AI_TECH')

	# Generic AI mention
	if 'ARTIFICIAL INTELLIGENCE' in desc or ' AI ' in desc or desc.startswith('AI '):
		categories.append('AI_MENTIONED')

	# IT services patterns
	if any(term in desc for term in ['IT SUPPORT', 'IT SERVICES', 'HELP DESK',
		'INFORMATION TECHNOLOGY SUPPORT', 'PROGRAMMATIC SUPPORT',
		'ADVISORY AND ASSISTANCE', 'MANAGEMENT SUPPORT']):
		categories.append('IT_SERVICES')

	# R&D
	if any(term in desc for term in ['RESEARCH', 'R&D', 'PROTOTYPE', 'DEVELOP']):
		categories.append('RD_DEVELOPMENT')

	# Cloud/infrastructure
	if any(term in desc for term in ['CLOUD', 'DATA CENTER', 'INFRASTRUCTURE', 'HOSTING']):
		categories.append('CLOUD_INFRA')

	# Cybersecurity
	if any(term in desc for term in ['CYBER', 'SECURITY', 'THREAT']):
		categories.append('CYBERSECURITY')

	if not categories:
		categories.append('UNCLEAR')

	return categories

df['categories'] = df['Description'].apply(categorize_contract)

# Count each category
cat_counts = Counter()
cat_dollars = Counter()
for _, row in df.iterrows():
	for cat in row['categories']:
		cat_counts[cat] += 1
		cat_dollars[cat] += row['Award Amount']

print("Contract categorization (contracts can appear in multiple categories):")
for cat, count in cat_counts.most_common():
	dollars = cat_dollars[cat]
	print(f"  {cat}: {count} contracts, ${dollars:,.0f} ({dollars/total_value*100:.1f}%)")
print()

# Contracts that mention AI but look like generic IT
ai_mentioned = set()
it_services = set()
for idx, row in df.iterrows():
	cats = row['categories']
	if 'AI_MENTIONED' in cats:
		ai_mentioned.add(idx)
	if 'IT_SERVICES' in cats:
		it_services.add(idx)

overlap = ai_mentioned & it_services
print(f"Contracts mentioning AI: {len(ai_mentioned)}")
print(f"Contracts that look like IT services: {len(it_services)}")
print(f"Both (AI buzzword on IT contract): {len(overlap)}")
print()

# Contracts with NO AI mention at all
no_ai = df[~df.index.isin(ai_mentioned)]
specific_ai = df[df['categories'].apply(lambda x: 'SPECIFIC_AI_TECH' in x)]
print(f"Contracts with specific AI tech mentioned: {len(specific_ai)} (${specific_ai['Award Amount'].sum():,.0f}, {specific_ai['Award Amount'].sum()/total_value*100:.1f}%)")
print(f"Contracts with generic AI mention only: {len(ai_mentioned) - len(specific_ai)} contracts")
no_ai_no_specific = df[~df.index.isin(ai_mentioned) & ~df['categories'].apply(lambda x: 'SPECIFIC_AI_TECH' in x)]
print(f"Contracts with no AI/ML mention in description: {len(no_ai_no_specific)}")
print()

# Show some examples of the "no AI mention" contracts
print("Sample contracts with NO AI/ML in description (found by keyword search of USAspending):")
for _, row in no_ai_no_specific.head(5).iterrows():
	print(f"  {row['Recipient Name']}: ${row['Award Amount']:,.0f}")
	print(f"    Keyword: {row['_search_keyword']}")
	print(f"    Desc: {str(row['Description'])[:150]}")
print()

# ── QUESTION 5: NAICS codes ──
print("=" * 80)
print("Q5: NAICS CODES - WHAT INDUSTRIES?")
print("=" * 80)
naics_null = df['NAICS Code'].isnull().sum()
naics_desc_null = df['NAICS Description'].isnull().sum()
print(f"NAICS Code null: {naics_null}/{len(df)} ({naics_null/len(df)*100:.1f}%)")
print(f"NAICS Description null: {naics_desc_null}/{len(df)} ({naics_desc_null/len(df)*100:.1f}%)")
print()

if naics_null < len(df):
	naics_spend = df.groupby(['NAICS Code', 'NAICS Description']).agg(
		total=('Award Amount', 'sum'),
		count=('Award Amount', 'count')
	).sort_values('total', ascending=False)
	print("Top NAICS codes by dollar value:")
	for (code, desc), row in naics_spend.head(15).iterrows():
		print(f"  {code} - {desc}: {int(row['count'])} contracts, ${row['total']:,.0f} ({row['total']/total_value*100:.1f}%)")
else:
	print("ALL NAICS codes are null. This field was not populated in the API response.")
print()

# ── QUESTION 6: Contract size distribution ──
print("=" * 80)
print("Q6: CONTRACT SIZE DISTRIBUTION")
print("=" * 80)
amounts = df['Award Amount'].dropna()
print(f"Total contracts with amount: {len(amounts)}")
print(f"Min: ${amounts.min():,.0f}")
print(f"Max: ${amounts.max():,.0f}")
print(f"Mean: ${amounts.mean():,.0f}")
print(f"Median: ${amounts.median():,.0f}")
print(f"Std Dev: ${amounts.std():,.0f}")
print()

# Buckets
buckets = [
	('Under $100K', 0, 100_000),
	('$100K - $1M', 100_000, 1_000_000),
	('$1M - $10M', 1_000_000, 10_000_000),
	('$10M - $50M', 10_000_000, 50_000_000),
	('$50M - $100M', 50_000_000, 100_000_000),
	('Over $100M', 100_000_000, float('inf')),
]

print("Size distribution:")
for label, low, high in buckets:
	mask = (amounts >= low) & (amounts < high)
	count = mask.sum()
	value = amounts[mask].sum()
	print(f"  {label}: {count} contracts ({count/len(amounts)*100:.1f}%), ${value:,.0f} ({value/total_value*100:.1f}%)")
print()

# Top 10 contracts by value
print("Top 10 contracts by value:")
top10 = df.nlargest(10, 'Award Amount')
for _, row in top10.iterrows():
	print(f"  ${row['Award Amount']:,.0f} - {row['Recipient Name']}")
	print(f"    Agency: {row['Awarding Agency']} / {row['Awarding Sub Agency']}")
	print(f"    Desc: {str(row['Description'])[:120]}")
print()

# ── QUESTION 7: Big AI companies ──
print("=" * 80)
print("Q7: BIG AI COMPANIES AS DIRECT RECIPIENTS")
print("=" * 80)

big_ai_terms = {
	'OpenAI': ['OPENAI', 'OPEN AI'],
	'Anthropic': ['ANTHROPIC'],
	'Google': ['GOOGLE', 'ALPHABET', 'DEEPMIND'],
	'Microsoft': ['MICROSOFT'],
	'Amazon/AWS': ['AMAZON', 'AWS'],
	'Meta/Facebook': ['META', 'FACEBOOK'],
	'Palantir': ['PALANTIR'],
	'IBM': ['IBM', 'INTERNATIONAL BUSINESS MACHINES'],
	'Booz Allen': ['BOOZ ALLEN'],
	'NVIDIA': ['NVIDIA'],
	'Lockheed Martin': ['LOCKHEED'],
	'Raytheon': ['RAYTHEON', 'RTX'],
	'Northrop Grumman': ['NORTHROP'],
	'General Dynamics': ['GENERAL DYNAMICS'],
	'SAIC': ['SAIC'],
	'Leidos': ['LEIDOS'],
	'BAE Systems': ['BAE SYSTEMS'],
	'L3Harris': ['L3HARRIS', 'L3 HARRIS'],
}

for company, terms in big_ai_terms.items():
	matches = df[df['Recipient Name'].str.upper().apply(
		lambda x: any(t in str(x) for t in terms)
	)]
	if len(matches) > 0:
		total = matches['Award Amount'].sum()
		print(f"{company}: {len(matches)} contracts, ${total:,.0f} ({total/total_value*100:.1f}%)")
		for _, row in matches.iterrows():
			print(f"    ${row['Award Amount']:,.0f} - {row['Awarding Agency']} - {str(row['Description'])[:100]}")
	else:
		print(f"{company}: NO CONTRACTS FOUND")
print()

# ── QUESTION 8: Search keyword distribution ──
print("=" * 80)
print("BONUS: SEARCH KEYWORD DISTRIBUTION")
print("=" * 80)
kw_counts = df['_search_keyword'].value_counts()
kw_dollars = df.groupby('_search_keyword')['Award Amount'].sum().sort_values(ascending=False)
print("Contracts by search keyword:")
for kw in kw_dollars.index:
	count = kw_counts.get(kw, 0)
	dollars = kw_dollars[kw]
	print(f"  '{kw}': {count} contracts, ${dollars:,.0f} ({dollars/total_value*100:.1f}%)")
print()

# ── Contract type distribution ──
print("=" * 80)
print("BONUS: CONTRACT TYPE DISTRIBUTION")
print("=" * 80)
type_spend = df.groupby('Contract Award Type')['Award Amount'].sum().sort_values(ascending=False)
type_count = df.groupby('Contract Award Type').size()
for ctype, amount in type_spend.items():
	count = type_count.get(ctype, 0)
	print(f"  {ctype}: {count} contracts, ${amount:,.0f} ({amount/total_value*100:.1f}%)")
print()

# ── Negative amounts check ──
print("=" * 80)
print("DATA QUALITY: NEGATIVE AMOUNTS")
print("=" * 80)
negatives = df[df['Award Amount'] < 0]
print(f"Contracts with negative amounts: {len(negatives)}")
if len(negatives) > 0:
	print(f"Total negative value: ${negatives['Award Amount'].sum():,.0f}")
	for _, row in negatives.iterrows():
		print(f"  {row['Recipient Name']}: ${row['Award Amount']:,.0f} - {str(row['Description'])[:100]}")
print()

# ── Thesis test summary ──
print("=" * 80)
print("THESIS TEST: 'Same defense contractors with new buzzwords'")
print("=" * 80)

# Are top recipients defense contractors?
print("\nTop 10 recipients - are they defense/IT contractors?")
for i, (name, amount) in enumerate(recipient_spend.head(10).items()):
	is_defense = df[df['Recipient Name'] == name]['is_dod'].any()
	pct = amount / total_value * 100
	print(f"  {i+1}. {name}: ${amount:,.0f} ({pct:.1f}%) - DoD contract: {is_defense}")

print(f"\nDoD share: {dod_pct:.1f}% (thesis claimed 69%)")
print(f"Top 5 concentration: {top5_total/total_value*100:.1f}%")
print(f"Top 10 concentration: {top10_total/total_value*100:.1f}%")

# How many of top 20 recipients are traditional defense/IT contractors vs AI-native?
print("\nDone. All numbers above are computed from the data.")
