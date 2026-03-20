"""
CFPB Credit Reporting Relief Rate Analysis
Tests claim: "Experian's consumer relief rate dropped from ~20% in 2024 to <1% in 2025"
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)  # cfpb-relief-analysis/
EXPERIMENTS_DIR = os.path.dirname(PROJECT_DIR)  # experiments/

DATA_PATH = os.path.join(EXPERIMENTS_DIR, 'data', 'cfpb', 'raw', 'cfpb-credit-reporting-2020-2026.csv')
CHARTS_DIR = os.path.join(PROJECT_DIR, 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

BIG_THREE = [
	'Experian Information Solutions Inc.',
	'EQUIFAX, INC.',
	'TRANSUNION INTERMEDIATE HOLDINGS, INC.',
]
LABELS = {
	'Experian Information Solutions Inc.': 'Experian',
	'EQUIFAX, INC.': 'Equifax',
	'TRANSUNION INTERMEDIATE HOLDINGS, INC.': 'TransUnion',
}

RELIEF_RESPONSES = {'Closed with monetary relief', 'Closed with non-monetary relief'}
CLOSED_RESPONSES = {
	'Closed with explanation',
	'Closed with monetary relief',
	'Closed with non-monetary relief',
}

# ── Load data ──────────────────────────────────────────────────────────
print("Loading data...")
df = pd.read_csv(DATA_PATH, low_memory=False, on_bad_lines='skip')
print(f"Total rows loaded: {len(df):,}")

# Parse dates robustly
df['Date received'] = pd.to_datetime(df['Date received'], format='mixed', errors='coerce')
bad_dates = df['Date received'].isna().sum()
print(f"Unparseable dates dropped: {bad_dates:,}")
df = df.dropna(subset=['Date received'])
print(f"Rows after date cleanup: {len(df):,}")
print(f"Date range: {df['Date received'].min()} to {df['Date received'].max()}")

# Filter to big three
df_big3 = df[df['Company'].isin(BIG_THREE)].copy()
print(f"Big three rows: {len(df_big3):,}")

# Add month column
df_big3['month'] = df_big3['Date received'].dt.to_period('M')

# Classify responses
df_big3['is_relief'] = df_big3['Company response to consumer'].isin(RELIEF_RESPONSES)
df_big3['is_closed'] = df_big3['Company response to consumer'].isin(CLOSED_RESPONSES)
df_big3['is_monetary'] = df_big3['Company response to consumer'] == 'Closed with monetary relief'
df_big3['is_nonmonetary'] = df_big3['Company response to consumer'] == 'Closed with non-monetary relief'

# ── 1. Relief rate by company by month ─────────────────────────────────
print("\n=== RELIEF RATE BY COMPANY BY MONTH ===")

# Only count closed complaints (not in-progress, untimely, etc.)
df_closed = df_big3[df_big3['is_closed']].copy()

monthly = df_closed.groupby(['Company', 'month']).agg(
	total=('is_closed', 'sum'),
	relief=('is_relief', 'sum'),
	monetary=('is_monetary', 'sum'),
	nonmonetary=('is_nonmonetary', 'sum'),
).reset_index()

monthly['relief_rate'] = monthly['relief'] / monthly['total'] * 100
monthly['month_dt'] = monthly['month'].dt.to_timestamp()

# Chart 1: Relief rate time series
fig, ax = plt.subplots(figsize=(14, 7))
colors = {'Experian Information Solutions Inc.': '#e74c3c',
          'EQUIFAX, INC.': '#2ecc71',
          'TRANSUNION INTERMEDIATE HOLDINGS, INC.': '#3498db'}

for company in BIG_THREE:
	mask = monthly['Company'] == company
	data = monthly[mask].sort_values('month_dt')
	ax.plot(data['month_dt'], data['relief_rate'],
	        label=LABELS[company], color=colors[company], linewidth=1.5)

ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Relief Rate (%)', fontsize=12)
ax.set_title('CFPB Consumer Relief Rate by Bureau (2020-2026)\n'
             '"Relief" = Closed with monetary or non-monetary relief, as % of all closed complaints',
             fontsize=13)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'relief_rate_by_bureau.png'), dpi=150)
plt.close()
print("Saved: relief_rate_by_bureau.png")

# ── 2. Specific quarterly numbers ─────────────────────────────────────
print("\n=== QUARTERLY RELIEF RATES ===")

df_closed['quarter'] = df_closed['Date received'].dt.to_period('Q')

quarterly = df_closed.groupby(['Company', 'quarter']).agg(
	total=('is_closed', 'sum'),
	relief=('is_relief', 'sum'),
	monetary=('is_monetary', 'sum'),
	nonmonetary=('is_nonmonetary', 'sum'),
).reset_index()
quarterly['relief_rate'] = quarterly['relief'] / quarterly['total'] * 100

print("\nQ1 2024 vs Q1 2025 comparison:")
print("-" * 80)
for company in BIG_THREE:
	label = LABELS[company]
	q1_24 = quarterly[(quarterly['Company'] == company) & (quarterly['quarter'] == '2024Q1')]
	q1_25 = quarterly[(quarterly['Company'] == company) & (quarterly['quarter'] == '2025Q1')]

	if not q1_24.empty and not q1_25.empty:
		r24 = q1_24.iloc[0]
		r25 = q1_25.iloc[0]
		print(f"\n{label}:")
		print(f"  Q1 2024: {r24['relief_rate']:.2f}% relief ({r24['relief']:,.0f} / {r24['total']:,.0f} closed)")
		print(f"    - Monetary: {r24['monetary']:,.0f}  Non-monetary: {r24['nonmonetary']:,.0f}")
		print(f"  Q1 2025: {r25['relief_rate']:.2f}% relief ({r25['relief']:,.0f} / {r25['total']:,.0f} closed)")
		print(f"    - Monetary: {r25['monetary']:,.0f}  Non-monetary: {r25['nonmonetary']:,.0f}")
		print(f"  Change: {r25['relief_rate'] - r24['relief_rate']:+.2f} percentage points")
	else:
		print(f"\n{label}: missing data for comparison")
		if q1_24.empty:
			print("  Q1 2024: NO DATA")
		if q1_25.empty:
			print("  Q1 2025: NO DATA")

# Full quarterly table
print("\n\nFull quarterly breakdown:")
print("=" * 100)
for company in BIG_THREE:
	label = LABELS[company]
	print(f"\n{label}:")
	comp_q = quarterly[quarterly['Company'] == company].sort_values('quarter')
	for _, row in comp_q.iterrows():
		print(f"  {row['quarter']}: {row['relief_rate']:6.2f}%  "
		      f"(relief={row['relief']:>6,.0f} / closed={row['total']:>7,.0f})  "
		      f"monetary={row['monetary']:>5,.0f}  non-monetary={row['nonmonetary']:>5,.0f}")

# ── 3. Complaint volume by company by month ────────────────────────────
print("\n\n=== COMPLAINT VOLUME BY MONTH ===")

volume = df_big3.groupby(['Company', 'month']).size().reset_index(name='complaints')
volume['month_dt'] = volume['month'].dt.to_timestamp()

fig, ax = plt.subplots(figsize=(14, 7))
for company in BIG_THREE:
	mask = volume['Company'] == company
	data = volume[mask].sort_values('month_dt')
	ax.plot(data['month_dt'], data['complaints'],
	        label=LABELS[company], color=colors[company], linewidth=1.5)

ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Complaints', fontsize=12)
ax.set_title('CFPB Credit Reporting Complaints by Bureau (2020-2026)', fontsize=13)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'complaint_volume_by_bureau.png'), dpi=150)
plt.close()
print("Saved: complaint_volume_by_bureau.png")

# ── 4. Stress tests ───────────────────────────────────────────────────
print("\n\n=== STRESS TEST 1: Response category distribution over time ===")

# Check if response categories changed over time
df_big3['year'] = df_big3['Date received'].dt.year
resp_by_year = df_big3.groupby(['year', 'Company response to consumer']).size().reset_index(name='count')
resp_pivot = resp_by_year.pivot_table(index='Company response to consumer', columns='year',
                                       values='count', fill_value=0)
print("\nResponse categories by year (all companies combined):")
print(resp_pivot.to_string())

# Per-company response distribution
print("\n\n=== STRESS TEST 2: Experian-specific response distribution ===")
exp_resp = df_big3[df_big3['Company'] == 'Experian Information Solutions Inc.'].groupby(
	['year', 'Company response to consumer']).size().reset_index(name='count')
exp_pivot = exp_resp.pivot_table(index='Company response to consumer', columns='year',
                                  values='count', fill_value=0)
print("\nExperian response categories by year:")
print(exp_pivot.to_string())

# Calculate percentages
print("\nExperian response distribution (%):")
exp_pct = exp_pivot.div(exp_pivot.sum(axis=0), axis=1) * 100
print(exp_pct.round(2).to_string())

# ── Stress test 3: Monthly relief rate for Experian (granular) ──────
print("\n\n=== STRESS TEST 3: Experian monthly relief - granular view ===")
exp_monthly = monthly[monthly['Company'] == 'Experian Information Solutions Inc.'].sort_values('month')
print(f"\n{'Month':<10} {'Total':>8} {'Relief':>8} {'Rate':>8} {'Monetary':>8} {'NonMon':>8}")
print("-" * 58)
for _, row in exp_monthly.iterrows():
	print(f"{str(row['month']):<10} {row['total']:>8,.0f} {row['relief']:>8,.0f} "
	      f"{row['relief_rate']:>7.2f}% {row['monetary']:>8,.0f} {row['nonmonetary']:>8,.0f}")

# ── Stress test 4: Is this credit-reporting specific? ──────────────
print("\n\n=== STRESS TEST 4: Is this specific to credit reporting? ===")
print("Checking unique products in the dataset...")
products = df['Product'].value_counts()
print(products)
print("\n(This dataset is credit-reporting only, so we can't compare across products from this file.)")
print("However, we can check if the pattern holds across sub-products:")

sub_products = df_big3['Sub-product'].value_counts()
print(f"\nSub-products in Big Three data:")
print(sub_products)

# Check relief rate for different sub-products for Experian
print("\n\nExperian relief rate by sub-product and year:")
exp_sub = df_big3[df_big3['Company'] == 'Experian Information Solutions Inc.'].copy()
exp_sub_closed = exp_sub[exp_sub['is_closed']]
sub_year = exp_sub_closed.groupby(['Sub-product', 'year']).agg(
	total=('is_closed', 'sum'),
	relief=('is_relief', 'sum'),
).reset_index()
sub_year['rate'] = sub_year['relief'] / sub_year['total'] * 100
sub_pivot = sub_year.pivot_table(index='Sub-product', columns='year', values='rate')
print(sub_pivot.round(2).to_string())

# ── Chart 3: Relief rate with 2024-2025 transition highlighted ──────
fig, ax = plt.subplots(figsize=(14, 7))

for company in BIG_THREE:
	mask = monthly['Company'] == company
	data = monthly[mask].sort_values('month_dt')
	ax.plot(data['month_dt'], data['relief_rate'],
	        label=LABELS[company], color=colors[company], linewidth=2)

# Highlight the transition period
ax.axvspan(pd.Timestamp('2024-09-01'), pd.Timestamp('2025-03-01'),
           alpha=0.1, color='red', label='Transition period')
ax.axhline(y=1, color='gray', linestyle='--', alpha=0.5, label='1% threshold')

ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Relief Rate (%)', fontsize=12)
ax.set_title('The Experian Relief Rate Cliff\n'
             'CFPB Credit Reporting: % of closed complaints resulting in consumer relief',
             fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'relief_rate_cliff_highlighted.png'), dpi=150)
plt.close()
print("\nSaved: relief_rate_cliff_highlighted.png")

# ── Summary statistics ─────────────────────────────────────────────
print("\n\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

for company in BIG_THREE:
	label = LABELS[company]
	comp_data = quarterly[quarterly['Company'] == company]

	# 2024 average
	avg_2024 = comp_data[comp_data['quarter'].dt.year == 2024]['relief_rate'].mean()
	# 2025 average
	avg_2025 = comp_data[comp_data['quarter'].dt.year == 2025]['relief_rate'].mean()
	# 2023 average
	avg_2023 = comp_data[comp_data['quarter'].dt.year == 2023]['relief_rate'].mean()

	print(f"\n{label}:")
	print(f"  2023 avg relief rate: {avg_2023:.2f}%")
	print(f"  2024 avg relief rate: {avg_2024:.2f}%")
	print(f"  2025 avg relief rate: {avg_2025:.2f}%")
	if avg_2024 > 0:
		print(f"  2024→2025 change: {avg_2025 - avg_2024:+.2f} pp ({(avg_2025/avg_2024 - 1)*100:+.1f}%)")

print("\n\nDone.")
