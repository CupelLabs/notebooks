#!/usr/bin/env python3
"""
FOIA Annual Report Analysis (FY2018-FY2024)
Cupel Labs - Analyzer

Reads 7 years of FOIA.gov annual report CSVs and produces:
- Processing time disparities by agency
- Backlog trends
- Denial/exemption patterns
- 20-day compliance rates
- Staffing vs performance correlation
- Ten oldest pending requests
- Overall system trends

All intermediate data exported to data/intermediate/.
"""

import os
import glob
import re
import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE = "/home/erdal/cupellabs/analyzer/experiments/foia-response-times"
RAW = os.path.join(BASE, "data/raw")
INTERMEDIATE = os.path.join(BASE, "data/intermediate")
os.makedirs(INTERMEDIATE, exist_ok=True)

YEARS = list(range(2018, 2025))

def find_csv(year_dir, base_name):
	"""Find a CSV file handling (N) suffix artifacts.
	base_name should be the canonical name without .csv extension."""
	# Try exact match first
	exact = os.path.join(year_dir, base_name + ".csv")
	if os.path.exists(exact):
		return exact
	# Try with (N) suffix
	pattern = os.path.join(year_dir, base_name + " (*).csv")
	matches = glob.glob(pattern)
	if matches:
		# Take the highest-numbered one (most recent download)
		return sorted(matches)[-1]
	return None

def load_csv_across_years(base_name, filter_agency_overall=True):
	"""Load a CSV file across all years, concatenating into one DataFrame."""
	frames = []
	for year in YEARS:
		year_dir = os.path.join(RAW, f"csv_{year}")
		path = find_csv(year_dir, base_name)
		if path is None:
			print(f"  WARNING: {base_name} not found for {year}")
			continue
		df = pd.read_csv(path, dtype=str)
		frames.append(df)
	if not frames:
		return pd.DataFrame()
	combined = pd.concat(frames, ignore_index=True)
	if filter_agency_overall:
		combined = combined[combined["Component"] == "Agency Overall"].copy()
		# CRITICAL: Exclude the "All agencies" summary row to prevent double-counting.
		# This row is a total row present in every CSV that sums all individual agencies.
		combined = combined[combined["Agency"] != "All agencies"].copy()
	# Normalize fiscal year
	combined["Fiscal Year"] = pd.to_numeric(combined["Fiscal Year"], errors="coerce").astype("Int64")
	return combined

def to_numeric_col(series):
	"""Convert a series to numeric, handling N/A and <1."""
	s = series.copy()
	s = s.replace({"N/A": np.nan, "n/a": np.nan, "": np.nan})
	s = s.str.strip() if hasattr(s, 'str') else s
	# Handle <1
	s = s.replace({"<1": "0.5"})
	# Remove commas in numbers
	if hasattr(s, 'str'):
		s = s.str.replace(",", "", regex=False)
	return pd.to_numeric(s, errors="coerce")

def normalize_agency_name(name):
	"""Normalize agency names across years."""
	if pd.isna(name):
		return name
	name = name.strip()
	# Known variations
	mapping = {
		"Corporation for National and Community Service (operating as AmeriCorps)": "AmeriCorps",
		"Corporation for National and Community Service": "AmeriCorps",
		"AmeriCorps": "AmeriCorps",
	}
	return mapping.get(name, name)


# ============================================================
# 1. PROCESSING TIMES
# ============================================================
print("=" * 60)
print("1. PROCESSING TIME ANALYSIS")
print("=" * 60)

proc_time = load_csv_across_years(
	"foia-processed-requests-response-time-for-all-processed-perfected-requests"
)

for col in proc_time.columns:
	if col not in ["Agency", "Component", "Fiscal Year"]:
		proc_time[col] = to_numeric_col(proc_time[col])

proc_time["Agency"] = proc_time["Agency"].apply(normalize_agency_name)

# Check for duplicates
dupes = proc_time.groupby(["Agency", "Fiscal Year"]).size()
dupes = dupes[dupes > 1]
if len(dupes) > 0:
	print(f"  ANOMALY: {len(dupes)} duplicate Agency+Year combinations found:")
	for idx in dupes.index[:10]:
		print(f"    {idx}: {dupes[idx]} rows")
	# Investigate
	for (agency, fy), count in dupes.items():
		subset = proc_time[(proc_time["Agency"] == agency) & (proc_time["Fiscal Year"] == fy)]
		print(f"\n  Duplicate detail for {agency}, FY{fy}:")
		print(subset[["Agency", "Fiscal Year", "Simple - Median Number of Days"]].to_string())
	print("  ACTION: Keeping first occurrence per Agency+Year after investigation")
	proc_time = proc_time.drop_duplicates(subset=["Agency", "Fiscal Year"], keep="first")

# Focus on agencies with data in most years (at least 5 of 7)
agency_year_counts = proc_time.groupby("Agency")["Fiscal Year"].nunique()
persistent_agencies = agency_year_counts[agency_year_counts >= 5].index.tolist()
print(f"\n  {len(persistent_agencies)} agencies present in 5+ of 7 years")

# Simple request median processing time, FY2024
fy2024_simple = proc_time[proc_time["Fiscal Year"] == 2024][
	["Agency", "Simple - Median Number of Days", "Complex - Median Number of Days",
	 "Simple - Average Number of Days", "Complex - Average Number of Days"]
].dropna(subset=["Simple - Median Number of Days"]).copy()

fy2024_simple = fy2024_simple.sort_values("Simple - Median Number of Days", ascending=False)
print(f"\n  TOP 15 AGENCIES: SLOWEST SIMPLE REQUEST MEDIAN (FY2024)")
print(fy2024_simple.head(15)[["Agency", "Simple - Median Number of Days"]].to_string(index=False))

# Complex request median, FY2024
fy2024_complex = proc_time[proc_time["Fiscal Year"] == 2024][
	["Agency", "Complex - Median Number of Days"]
].dropna(subset=["Complex - Median Number of Days"]).copy()
fy2024_complex = fy2024_complex.sort_values("Complex - Median Number of Days", ascending=False)
print(f"\n  TOP 15 AGENCIES: SLOWEST COMPLEX REQUEST MEDIAN (FY2024)")
print(fy2024_complex.head(15)[["Agency", "Complex - Median Number of Days"]].to_string(index=False))

# Trend: agencies that got worse vs better (simple median, FY2018 vs FY2024)
trend = proc_time[proc_time["Fiscal Year"].isin([2018, 2024])][
	["Agency", "Fiscal Year", "Simple - Median Number of Days"]
].copy()
trend_pivot = trend.pivot_table(index="Agency", columns="Fiscal Year",
	values="Simple - Median Number of Days", aggfunc="first")
trend_pivot.columns = ["FY2018", "FY2024"]
trend_pivot = trend_pivot.dropna()
trend_pivot["Change"] = trend_pivot["FY2024"] - trend_pivot["FY2018"]
trend_pivot["Pct_Change"] = ((trend_pivot["FY2024"] - trend_pivot["FY2018"]) / trend_pivot["FY2018"].replace(0, np.nan)) * 100

print(f"\n  AGENCIES THAT GOT WORSE (Simple Median, FY2018 vs FY2024, top 10 by absolute change):")
worse = trend_pivot.sort_values("Change", ascending=False).head(10)
print(worse[["FY2018", "FY2024", "Change"]].to_string())

print(f"\n  AGENCIES THAT IMPROVED (top 10 by absolute improvement):")
improved = trend_pivot.sort_values("Change", ascending=True).head(10)
print(improved[["FY2018", "FY2024", "Change"]].to_string())

# Export
proc_time.to_csv(os.path.join(INTERMEDIATE, "processing_times_all.csv"), index=False)
fy2024_simple.to_csv(os.path.join(INTERMEDIATE, "fy2024_simple_processing.csv"), index=False)
fy2024_complex.to_csv(os.path.join(INTERMEDIATE, "fy2024_complex_processing.csv"), index=False)
trend_pivot.reset_index().to_csv(os.path.join(INTERMEDIATE, "simple_median_trend_2018_2024.csv"), index=False)
print("  Exported: processing_times_all.csv, fy2024_simple_processing.csv, fy2024_complex_processing.csv, simple_median_trend_2018_2024.csv")


# ============================================================
# 2. BACKLOG ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("2. BACKLOG ANALYSIS")
print("=" * 60)

backlogs = load_csv_across_years(
	"foia-backlogs-of-foia-requests-and-administrative-appeals"
)
backlogs["Agency"] = backlogs["Agency"].apply(normalize_agency_name)

for col in ["Number of Backlogged Requests as of End of Fiscal Year",
			"Number of Backlogged Appeals as of End of Fiscal Year"]:
	backlogs[col] = to_numeric_col(backlogs[col])

# Check for duplicates
dupes_bl = backlogs.groupby(["Agency", "Fiscal Year"]).size()
dupes_bl = dupes_bl[dupes_bl > 1]
if len(dupes_bl) > 0:
	print(f"  ANOMALY: {len(dupes_bl)} duplicate backlog rows")
	backlogs = backlogs.drop_duplicates(subset=["Agency", "Fiscal Year"], keep="first")

# FY2024 backlog ranking
fy2024_bl = backlogs[backlogs["Fiscal Year"] == 2024][
	["Agency", "Number of Backlogged Requests as of End of Fiscal Year"]
].copy()
fy2024_bl.columns = ["Agency", "Backlog"]
fy2024_bl = fy2024_bl.sort_values("Backlog", ascending=False)
print(f"\n  TOP 15 AGENCIES: BIGGEST BACKLOG (FY2024)")
print(fy2024_bl.head(15).to_string(index=False))

# DHS verification
dhs_bl = backlogs[backlogs["Agency"] == "Department of Homeland Security"]
print(f"\n  DHS BACKLOG OVER TIME:")
print(dhs_bl[["Fiscal Year", "Number of Backlogged Requests as of End of Fiscal Year"]].to_string(index=False))

# Total federal backlog over time
total_bl = backlogs.groupby("Fiscal Year")["Number of Backlogged Requests as of End of Fiscal Year"].sum()
print(f"\n  TOTAL FEDERAL BACKLOG (all agencies):")
for fy, val in total_bl.items():
	print(f"    FY{fy}: {val:,.0f}")

# Backlog trend by top agencies
top_bl_agencies = fy2024_bl.head(10)["Agency"].tolist()
bl_trend = backlogs[backlogs["Agency"].isin(top_bl_agencies)].pivot_table(
	index="Fiscal Year",
	columns="Agency",
	values="Number of Backlogged Requests as of End of Fiscal Year",
	aggfunc="first"
)
bl_trend.to_csv(os.path.join(INTERMEDIATE, "backlog_trend_top10.csv"))

# Backlog ratio: backlog / requests received
volumes = load_csv_across_years(
	"foia-received-processed-and-pending-foia-requests"
)
volumes["Agency"] = volumes["Agency"].apply(normalize_agency_name)
for col in volumes.columns:
	if col not in ["Agency", "Component", "Fiscal Year"]:
		volumes[col] = to_numeric_col(volumes[col])

# Check for volume duplicates
dupes_vol = volumes.groupby(["Agency", "Fiscal Year"]).size()
dupes_vol = dupes_vol[dupes_vol > 1]
if len(dupes_vol) > 0:
	print(f"  ANOMALY: {len(dupes_vol)} duplicate volume rows")
	volumes = volumes.drop_duplicates(subset=["Agency", "Fiscal Year"], keep="first")

# Merge backlog with received
bl_ratio = backlogs[backlogs["Fiscal Year"] == 2024][["Agency", "Number of Backlogged Requests as of End of Fiscal Year"]].merge(
	volumes[volumes["Fiscal Year"] == 2024][["Agency", "Number of Requests Received in Fiscal Year"]],
	on="Agency", how="inner"
)
bl_ratio.columns = ["Agency", "Backlog", "Received"]
bl_ratio["Backlog_Ratio"] = bl_ratio["Backlog"] / bl_ratio["Received"].replace(0, np.nan)
bl_ratio = bl_ratio.sort_values("Backlog_Ratio", ascending=False)
print(f"\n  TOP 15: BACKLOG-TO-RECEIVED RATIO (FY2024)")
# Only agencies with non-trivial volume
bl_ratio_filtered = bl_ratio[bl_ratio["Received"] >= 100]
print(bl_ratio_filtered.head(15).to_string(index=False))

# Export
backlogs.to_csv(os.path.join(INTERMEDIATE, "backlogs_all.csv"), index=False)
fy2024_bl.to_csv(os.path.join(INTERMEDIATE, "fy2024_backlogs.csv"), index=False)
total_bl.to_frame("Total_Backlog").to_csv(os.path.join(INTERMEDIATE, "total_federal_backlog.csv"))
bl_ratio.to_csv(os.path.join(INTERMEDIATE, "fy2024_backlog_ratio.csv"), index=False)
volumes.to_csv(os.path.join(INTERMEDIATE, "volumes_all.csv"), index=False)
print("  Exported: backlogs_all.csv, fy2024_backlogs.csv, total_federal_backlog.csv, fy2024_backlog_ratio.csv, volumes_all.csv")


# ============================================================
# 3. DENIAL AND EXEMPTION PATTERNS
# ============================================================
print("\n" + "=" * 60)
print("3. DENIAL AND EXEMPTION PATTERNS")
print("=" * 60)

disposition = load_csv_across_years(
	"foia-disposition-of-foia-requests-all-processed-requests"
)
disposition["Agency"] = disposition["Agency"].apply(normalize_agency_name)
for col in disposition.columns:
	if col not in ["Agency", "Component", "Fiscal Year"]:
		disposition[col] = to_numeric_col(disposition[col])

# Check for duplicates
dupes_disp = disposition.groupby(["Agency", "Fiscal Year"]).size()
dupes_disp = dupes_disp[dupes_disp > 1]
if len(dupes_disp) > 0:
	print(f"  ANOMALY: {len(dupes_disp)} duplicate disposition rows")
	disposition = disposition.drop_duplicates(subset=["Agency", "Fiscal Year"], keep="first")

# Denial rate: (Full Denials Based on Exemptions) / Total
fy2024_disp = disposition[disposition["Fiscal Year"] == 2024].copy()
fy2024_disp["Denial_Rate"] = fy2024_disp["Number of Full Denials Based on Exemptions"] / fy2024_disp["Total"].replace(0, np.nan)
fy2024_disp["Full_Grant_Rate"] = fy2024_disp["Number of Full Grants"] / fy2024_disp["Total"].replace(0, np.nan)
fy2024_disp["Partial_Rate"] = fy2024_disp["Number of Partial Grants/Partial Denials"] / fy2024_disp["Total"].replace(0, np.nan)

# Filter to agencies with >= 100 processed
fy2024_disp_sig = fy2024_disp[fy2024_disp["Total"] >= 100].copy()
fy2024_disp_sig = fy2024_disp_sig.sort_values("Denial_Rate", ascending=False)
print(f"\n  TOP 15: FULL DENIAL RATE (FY2024, agencies with 100+ processed)")
print(fy2024_disp_sig[["Agency", "Number of Full Denials Based on Exemptions", "Total", "Denial_Rate"]].head(15).to_string(index=False))

# Also: lowest full grant rate
fy2024_disp_sig_fg = fy2024_disp_sig.sort_values("Full_Grant_Rate", ascending=True)
print(f"\n  LOWEST FULL GRANT RATE (FY2024, agencies with 100+ processed)")
print(fy2024_disp_sig_fg[["Agency", "Number of Full Grants", "Total", "Full_Grant_Rate"]].head(15).to_string(index=False))

# Exemptions
exemptions = load_csv_across_years(
	"foia-disposition-of-foia-requests-number-of-times-exemptions-applied"
)
exemptions["Agency"] = exemptions["Agency"].apply(normalize_agency_name)
ex_cols = [c for c in exemptions.columns if c.startswith("Ex.")]
for col in ex_cols:
	exemptions[col] = to_numeric_col(exemptions[col])

# Check for duplicates
dupes_ex = exemptions.groupby(["Agency", "Fiscal Year"]).size()
dupes_ex = dupes_ex[dupes_ex > 1]
if len(dupes_ex) > 0:
	print(f"  ANOMALY: {len(dupes_ex)} duplicate exemption rows")
	exemptions = exemptions.drop_duplicates(subset=["Agency", "Fiscal Year"], keep="first")

# Total exemption usage across all agencies, FY2024
fy2024_ex = exemptions[exemptions["Fiscal Year"] == 2024].copy()
total_ex = fy2024_ex[ex_cols].sum()
print(f"\n  TOTAL EXEMPTION USAGE ACROSS ALL AGENCIES (FY2024):")
for ex_name, count in total_ex.sort_values(ascending=False).items():
	print(f"    {ex_name}: {count:,.0f}")

# Per-agency top exemptions
fy2024_ex["Total_Exemptions"] = fy2024_ex[ex_cols].sum(axis=1)
fy2024_ex_sig = fy2024_ex[fy2024_ex["Total_Exemptions"] >= 50].copy()
# Compute share of b5 and b7 (broad exemptions)
b7_cols = [c for c in ex_cols if c.startswith("Ex. 7")]
fy2024_ex_sig["B5_Share"] = fy2024_ex_sig["Ex. 5"] / fy2024_ex_sig["Total_Exemptions"]
fy2024_ex_sig["B7_Total"] = fy2024_ex_sig[b7_cols].sum(axis=1)
fy2024_ex_sig["B7_Share"] = fy2024_ex_sig["B7_Total"] / fy2024_ex_sig["Total_Exemptions"]
fy2024_ex_sig["B5_B7_Share"] = (fy2024_ex_sig["Ex. 5"] + fy2024_ex_sig["B7_Total"]) / fy2024_ex_sig["Total_Exemptions"]

print(f"\n  AGENCIES WITH HIGHEST B5+B7 SHARE (broad exemptions, FY2024, 50+ total exemptions):")
top_broad = fy2024_ex_sig.sort_values("B5_B7_Share", ascending=False)
print(top_broad[["Agency", "Ex. 5", "B7_Total", "Total_Exemptions", "B5_B7_Share"]].head(15).to_string(index=False))

# Exemption trend over time
ex_trend = exemptions.groupby("Fiscal Year")[ex_cols].sum()
print(f"\n  EXEMPTION TRENDS (total across all agencies by year):")
print(ex_trend.to_string())

# Export
disposition.to_csv(os.path.join(INTERMEDIATE, "disposition_all.csv"), index=False)
fy2024_disp[["Agency", "Number of Full Grants", "Number of Partial Grants/Partial Denials",
	"Number of Full Denials Based on Exemptions", "No Records", "Total",
	"Denial_Rate", "Full_Grant_Rate"]].to_csv(
	os.path.join(INTERMEDIATE, "fy2024_disposition_rates.csv"), index=False)
exemptions.to_csv(os.path.join(INTERMEDIATE, "exemptions_all.csv"), index=False)
fy2024_ex_sig[["Agency"] + ex_cols + ["Total_Exemptions", "B5_Share", "B7_Share", "B5_B7_Share"]].to_csv(
	os.path.join(INTERMEDIATE, "fy2024_exemption_shares.csv"), index=False)
ex_trend.to_csv(os.path.join(INTERMEDIATE, "exemption_trends_by_year.csv"))
print("  Exported: disposition_all.csv, fy2024_disposition_rates.csv, exemptions_all.csv, fy2024_exemption_shares.csv, exemption_trends_by_year.csv")


# ============================================================
# 4. THE 20-DAY RULE
# ============================================================
print("\n" + "=" * 60)
print("4. THE 20-DAY RULE (Processing Time Distributions)")
print("=" * 60)

simple_dist = load_csv_across_years(
	"foia-processed-requests-response-time-in-day-increments-simple-requests"
)
simple_dist["Agency"] = simple_dist["Agency"].apply(normalize_agency_name)
for col in simple_dist.columns:
	if col not in ["Agency", "Component", "Fiscal Year"]:
		simple_dist[col] = to_numeric_col(simple_dist[col])

# Check for duplicates
dupes_sd = simple_dist.groupby(["Agency", "Fiscal Year"]).size()
dupes_sd = dupes_sd[dupes_sd > 1]
if len(dupes_sd) > 0:
	print(f"  ANOMALY: {len(dupes_sd)} duplicate simple distribution rows")
	simple_dist = simple_dist.drop_duplicates(subset=["Agency", "Fiscal Year"], keep="first")

# The <1-20 Days bucket = within the 20-business-day window
# (Note: these are calendar days in the data, 20 business days ~ 28 calendar days.
#  But the bucket is labeled "<1-20 Days" which is likely 20 calendar days.
#  This is a known caveat - the FOIA statute says 20 business days but the
#  reporting uses calendar day buckets.)

fy2024_sd = simple_dist[simple_dist["Fiscal Year"] == 2024].copy()
fy2024_sd["Within_20_Days"] = fy2024_sd["<1-20 Days"]
fy2024_sd["Over_20_Days"] = fy2024_sd["Total"] - fy2024_sd["<1-20 Days"]
fy2024_sd["Compliance_Rate"] = fy2024_sd["Within_20_Days"] / fy2024_sd["Total"].replace(0, np.nan)

fy2024_sd_sig = fy2024_sd[fy2024_sd["Total"] >= 50].copy()
fy2024_sd_sig = fy2024_sd_sig.sort_values("Compliance_Rate", ascending=True)
print(f"\n  LOWEST COMPLIANCE RATE (Simple requests within 1-20 days, FY2024, 50+ processed)")
print(f"  CAVEAT: Bucket is '<1-20 calendar days', FOIA statute is 20 BUSINESS days (~28 calendar)")
print(fy2024_sd_sig[["Agency", "Within_20_Days", "Total", "Compliance_Rate"]].head(15).to_string(index=False))

# Overall compliance rate
total_within = fy2024_sd["Within_20_Days"].sum()
total_all = fy2024_sd["Total"].sum()
print(f"\n  OVERALL SIMPLE REQUEST COMPLIANCE (FY2024):")
print(f"    Within 1-20 days: {total_within:,.0f} of {total_all:,.0f} = {total_within/total_all*100:.1f}%")

# Compliance trend
compliance_trend = simple_dist.groupby("Fiscal Year").agg(
	Within_20=("<1-20 Days", "sum"),
	Total=("Total", "sum")
)
compliance_trend["Compliance_Rate"] = compliance_trend["Within_20"] / compliance_trend["Total"]
print(f"\n  SIMPLE REQUEST COMPLIANCE TREND:")
for fy, row in compliance_trend.iterrows():
	print(f"    FY{fy}: {row['Compliance_Rate']*100:.1f}% ({row['Within_20']:,.0f} / {row['Total']:,.0f})")

# Also do complex requests
complex_dist = load_csv_across_years(
	"foia-processed-requests-response-time-in-day-increments-complex-requests"
)
complex_dist["Agency"] = complex_dist["Agency"].apply(normalize_agency_name)
for col in complex_dist.columns:
	if col not in ["Agency", "Component", "Fiscal Year"]:
		complex_dist[col] = to_numeric_col(complex_dist[col])

dupes_cd = complex_dist.groupby(["Agency", "Fiscal Year"]).size()
dupes_cd = dupes_cd[dupes_cd > 1]
if len(dupes_cd) > 0:
	complex_dist = complex_dist.drop_duplicates(subset=["Agency", "Fiscal Year"], keep="first")

fy2024_cd = complex_dist[complex_dist["Fiscal Year"] == 2024].copy()
fy2024_cd["Within_20_Days"] = fy2024_cd["<1-20 Days"]
total_complex_within = fy2024_cd["Within_20_Days"].sum()
total_complex_all = fy2024_cd["Total"].sum()
print(f"\n  COMPLEX REQUEST COMPLIANCE (FY2024):")
print(f"    Within 1-20 days: {total_complex_within:,.0f} of {total_complex_all:,.0f} = {total_complex_within/total_complex_all*100:.1f}%")

# Export
fy2024_sd[["Agency", "Within_20_Days", "Over_20_Days", "Total", "Compliance_Rate"]].to_csv(
	os.path.join(INTERMEDIATE, "fy2024_simple_compliance.csv"), index=False)
compliance_trend.to_csv(os.path.join(INTERMEDIATE, "simple_compliance_trend.csv"))
simple_dist.to_csv(os.path.join(INTERMEDIATE, "simple_time_dist_all.csv"), index=False)
complex_dist.to_csv(os.path.join(INTERMEDIATE, "complex_time_dist_all.csv"), index=False)
print("  Exported: fy2024_simple_compliance.csv, simple_compliance_trend.csv, simple_time_dist_all.csv, complex_time_dist_all.csv")


# ============================================================
# 5. STAFFING VS PERFORMANCE
# ============================================================
print("\n" + "=" * 60)
print("5. STAFFING VS PERFORMANCE")
print("=" * 60)

personnel = load_csv_across_years("foia-foia-personnel")
personnel["Agency"] = personnel["Agency"].apply(normalize_agency_name)
for col in personnel.columns:
	if col not in ["Agency", "Component", "Fiscal Year"]:
		personnel[col] = to_numeric_col(personnel[col])

dupes_per = personnel.groupby(["Agency", "Fiscal Year"]).size()
dupes_per = dupes_per[dupes_per > 1]
if len(dupes_per) > 0:
	print(f"  ANOMALY: {len(dupes_per)} duplicate personnel rows")
	personnel = personnel.drop_duplicates(subset=["Agency", "Fiscal Year"], keep="first")

costs = load_csv_across_years("foia-foia-costs-and-fees-collected-for-processing-requests")
costs["Agency"] = costs["Agency"].apply(normalize_agency_name)
for col in costs.columns:
	if col not in ["Agency", "Component", "Fiscal Year"]:
		costs[col] = to_numeric_col(costs[col])

dupes_cost = costs.groupby(["Agency", "Fiscal Year"]).size()
dupes_cost = dupes_cost[dupes_cost > 1]
if len(dupes_cost) > 0:
	print(f"  ANOMALY: {len(dupes_cost)} duplicate cost rows")
	costs = costs.drop_duplicates(subset=["Agency", "Fiscal Year"], keep="first")

# Merge staffing with processing time and volume for FY2024
fy2024_staff = personnel[personnel["Fiscal Year"] == 2024][
	["Agency", 'Total Number of "Full-Time FOIA Staff"']
].copy()
fy2024_staff.columns = ["Agency", "Total_Staff"]

fy2024_cost = costs[costs["Fiscal Year"] == 2024][
	["Agency", "Processing Costs", "Total Costs"]
].copy()

fy2024_vol = volumes[volumes["Fiscal Year"] == 2024][
	["Agency", "Number of Requests Processed in Fiscal Year"]
].copy()
fy2024_vol.columns = ["Agency", "Processed"]

fy2024_pt = proc_time[proc_time["Fiscal Year"] == 2024][
	["Agency", "Simple - Median Number of Days"]
].copy()
fy2024_pt.columns = ["Agency", "Simple_Median_Days"]

staff_perf = fy2024_staff.merge(fy2024_cost, on="Agency", how="inner") \
	.merge(fy2024_vol, on="Agency", how="inner") \
	.merge(fy2024_pt, on="Agency", how="inner")

staff_perf["Requests_Per_Staff"] = staff_perf["Processed"] / staff_perf["Total_Staff"].replace(0, np.nan)
staff_perf["Cost_Per_Request"] = staff_perf["Processing Costs"] / staff_perf["Processed"].replace(0, np.nan)

# Filter to agencies with non-trivial operations
staff_perf_sig = staff_perf[(staff_perf["Processed"] >= 100) & (staff_perf["Total_Staff"] > 0)].copy()

# Correlation: total costs vs simple median days
corr_cost_time = staff_perf_sig[["Processing Costs", "Simple_Median_Days"]].dropna()
if len(corr_cost_time) >= 10:
	r = np.corrcoef(corr_cost_time["Processing Costs"], corr_cost_time["Simple_Median_Days"])[0, 1]
	print(f"\n  Correlation (Processing Costs vs Simple Median Days): r={r:.3f}")

corr_staff_time = staff_perf_sig[["Total_Staff", "Simple_Median_Days"]].dropna()
if len(corr_staff_time) >= 10:
	r2 = np.corrcoef(corr_staff_time["Total_Staff"], corr_staff_time["Simple_Median_Days"])[0, 1]
	print(f"  Correlation (Total Staff vs Simple Median Days): r={r2:.3f}")

# Cost per request vs median time
corr_cpr = staff_perf_sig[["Cost_Per_Request", "Simple_Median_Days"]].dropna()
if len(corr_cpr) >= 10:
	r3 = np.corrcoef(corr_cpr["Cost_Per_Request"], corr_cpr["Simple_Median_Days"])[0, 1]
	print(f"  Correlation (Cost Per Request vs Simple Median Days): r={r3:.3f}")

# Top spenders
staff_perf_sig_sorted = staff_perf_sig.sort_values("Processing Costs", ascending=False)
print(f"\n  TOP 10 SPENDERS (FY2024):")
print(staff_perf_sig_sorted[["Agency", "Processing Costs", "Processed", "Cost_Per_Request",
	"Simple_Median_Days"]].head(10).to_string(index=False))

# Total federal FOIA spending
total_spending = costs[costs["Fiscal Year"] == 2024]["Total Costs"].sum()
total_processing = costs[costs["Fiscal Year"] == 2024]["Processing Costs"].sum()
print(f"\n  TOTAL FEDERAL FOIA SPENDING (FY2024):")
print(f"    Processing costs: ${total_processing:,.0f}")
print(f"    Total costs (incl litigation): ${total_spending:,.0f}")

# Spending trend
spending_trend = costs.groupby("Fiscal Year").agg(
	Processing=("Processing Costs", "sum"),
	Total=("Total Costs", "sum")
)
print(f"\n  FOIA SPENDING TREND:")
for fy, row in spending_trend.iterrows():
	print(f"    FY{fy}: ${row['Processing']:,.0f} processing, ${row['Total']:,.0f} total")

# Export
staff_perf.to_csv(os.path.join(INTERMEDIATE, "fy2024_staffing_performance.csv"), index=False)
spending_trend.to_csv(os.path.join(INTERMEDIATE, "spending_trend.csv"))
personnel.to_csv(os.path.join(INTERMEDIATE, "personnel_all.csv"), index=False)
costs.to_csv(os.path.join(INTERMEDIATE, "costs_all.csv"), index=False)
print("  Exported: fy2024_staffing_performance.csv, spending_trend.csv, personnel_all.csv, costs_all.csv")


# ============================================================
# 6. TEN OLDEST PENDING REQUESTS
# ============================================================
print("\n" + "=" * 60)
print("6. TEN OLDEST PENDING REQUESTS")
print("=" * 60)

oldest = load_csv_across_years(
	"foia-pending-requests-ten-oldest-pending-perfected-requests"
)
oldest["Agency"] = oldest["Agency"].apply(normalize_agency_name)

# The CSV has alternating Date/Days columns for each of the 10 oldest
# Extract the "Oldest Number of Days Pending" column
days_cols = [c for c in oldest.columns if "Number of Days Pending" in c]
date_cols = [c for c in oldest.columns if c == "Date" or c.startswith("Date")]

# The oldest one is the last pair
if "Oldest Number of Days Pending" in oldest.columns:
	oldest["Max_Days_Pending"] = to_numeric_col(oldest["Oldest Number of Days Pending"])
else:
	# Find the rightmost days column
	oldest["Max_Days_Pending"] = to_numeric_col(oldest[days_cols[-1]])

# FY2024 oldest
fy2024_oldest = oldest[oldest["Fiscal Year"] == 2024][
	["Agency", "Max_Days_Pending"]
].dropna().copy()
fy2024_oldest = fy2024_oldest.sort_values("Max_Days_Pending", ascending=False)
print(f"\n  AGENCIES WITH OLDEST PENDING REQUESTS (FY2024)")
print(f"  (Max days pending for the single oldest request)")
for _, row in fy2024_oldest.head(20).iterrows():
	years_pending = row["Max_Days_Pending"] / 365.25
	print(f"    {row['Agency']}: {row['Max_Days_Pending']:,.0f} days ({years_pending:.1f} years)")

# How many agencies have requests older than 5 years (1826 days)?
over_5yr = fy2024_oldest[fy2024_oldest["Max_Days_Pending"] > 1826]
print(f"\n  Agencies with requests older than 5 years: {len(over_5yr)}")

over_10yr = fy2024_oldest[fy2024_oldest["Max_Days_Pending"] > 3652]
print(f"  Agencies with requests older than 10 years: {len(over_10yr)}")

# Export
fy2024_oldest.to_csv(os.path.join(INTERMEDIATE, "fy2024_oldest_pending.csv"), index=False)
oldest.to_csv(os.path.join(INTERMEDIATE, "ten_oldest_all.csv"), index=False)
print("  Exported: fy2024_oldest_pending.csv, ten_oldest_all.csv")


# ============================================================
# 7. OVERALL TRENDS
# ============================================================
print("\n" + "=" * 60)
print("7. OVERALL TRENDS")
print("=" * 60)

# Total requests received, processed, pending over time
vol_trend = volumes.groupby("Fiscal Year").agg(
	Pending_Start=("Number of Requests Pending as of Start of Fiscal Year", "sum"),
	Received=("Number of Requests Received in Fiscal Year", "sum"),
	Processed=("Number of Requests Processed in Fiscal Year", "sum"),
	Pending_End=("Number of Requests Pending as of End of Fiscal Year", "sum")
)
print(f"\n  FEDERAL FOIA VOLUMES OVER TIME:")
print(vol_trend.to_string())

# Net processing gap (received - processed)
vol_trend["Net_Gap"] = vol_trend["Received"] - vol_trend["Processed"]
print(f"\n  NET GAP (Received - Processed):")
for fy, row in vol_trend.iterrows():
	gap_sign = "+" if row["Net_Gap"] > 0 else ""
	print(f"    FY{fy}: {gap_sign}{row['Net_Gap']:,.0f}")

# Total backlog trend (already computed above)
print(f"\n  TOTAL BACKLOG (from backlog file):")
for fy, val in total_bl.items():
	print(f"    FY{fy}: {val:,.0f}")

# Export
vol_trend.to_csv(os.path.join(INTERMEDIATE, "volume_trends.csv"))
print("  Exported: volume_trends.csv")


# ============================================================
# SUMMARY STATISTICS
# ============================================================
print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)

# Key numbers for findings.md
print(f"\n  Total requests received FY2024: {vol_trend.loc[2024, 'Received']:,.0f}")
print(f"  Total processed FY2024: {vol_trend.loc[2024, 'Processed']:,.0f}")
print(f"  Total pending end FY2024: {vol_trend.loc[2024, 'Pending_End']:,.0f}")
print(f"  Total backlogged FY2024: {total_bl[2024]:,.0f}")
print(f"  Total FOIA spending FY2024: ${total_spending:,.0f}")
print(f"  Simple request overall compliance (1-20 days): {total_within/total_all*100:.1f}%")

# Backlog change FY2018 to FY2024
bl_2018 = total_bl.get(2018, 0)
bl_2024 = total_bl.get(2024, 0)
print(f"  Backlog FY2018: {bl_2018:,.0f}")
print(f"  Backlog FY2024: {bl_2024:,.0f}")
if bl_2018 > 0:
	print(f"  Backlog change: {((bl_2024 - bl_2018) / bl_2018) * 100:.1f}%")

# DHS share of total backlog
dhs_2024_bl = fy2024_bl[fy2024_bl["Agency"] == "Department of Homeland Security"]["Backlog"].values
if len(dhs_2024_bl) > 0:
	print(f"  DHS backlog FY2024: {dhs_2024_bl[0]:,.0f}")
	print(f"  DHS share of total backlog: {dhs_2024_bl[0] / bl_2024 * 100:.1f}%")

print("\n  ANALYSIS COMPLETE. All intermediate data exported.")
