"""Analyze CFPB student loan complaints for servicer transition impacts."""
import pandas as pd
import json
import os

OUT_DIR = "/home/erdal/cupellabs/analyzer/experiments/student-loan-servicers/data/intermediate"
RAW_FILE = "/home/erdal/cupellabs/analyzer/experiments/student-loan-servicers/data/raw/cfpb_student_loans.csv"

print("Loading data...")
df = pd.read_csv(RAW_FILE, low_memory=False)
df["date_received"] = pd.to_datetime(df["date_received"], format="ISO8601", utc=True)
df["year_month"] = df["date_received"].dt.to_period("M")
df["year"] = df["date_received"].dt.year
df["quarter"] = df["date_received"].dt.to_period("Q")

# Focus on federal student loans (where servicer transitions happen)
fed = df[df["sub_product"] == "Federal student loan servicing"].copy()
print(f"Total complaints: {len(df)}")
print(f"Federal student loan complaints: {len(fed)}")

# Key servicer transitions:
# 1. FedLoan (AES/PHEAA) -> MOHELA: Transfer began Dec 2021, completed mid-2022
# 2. Navient -> Aidvantage (Maximus): Navient exited Jan 2022, Maximus took over
# 3. Granite State (GSMR) -> EdFinancial: 2022
# 4. COVID forbearance ended Sep 2023, payment restart Oct 2023

# Monthly complaints by company
key_servicers = ["MOHELA", "Navient Solutions, LLC.", "AES/PHEAA", 
                 "Maximus Federal Services, Inc.", "Nelnet, Inc.", 
                 "EdFinancial Services"]

print("\n=== MONTHLY COMPLAINTS BY SERVICER ===")
monthly_by_company = fed[fed["company"].isin(key_servicers)].groupby(
    [fed[fed["company"].isin(key_servicers)]["year_month"], "company"]
).size().unstack(fill_value=0)

# Convert to serializable format
monthly_dict = {}
for col in monthly_by_company.columns:
    monthly_dict[col] = {str(k): int(v) for k, v in monthly_by_company[col].items()}

# Save monthly data
monthly_export = monthly_by_company.copy()
monthly_export.index = monthly_export.index.astype(str)
monthly_export.to_csv(os.path.join(OUT_DIR, "monthly_complaints_by_servicer.csv"))
print("Saved monthly_complaints_by_servicer.csv")

# Overall monthly total (all student loans)
monthly_total = fed.groupby("year_month").size()
monthly_total_df = monthly_total.reset_index()
monthly_total_df.columns = ["year_month", "count"]
monthly_total_df["year_month"] = monthly_total_df["year_month"].astype(str)
monthly_total_df.to_csv(os.path.join(OUT_DIR, "monthly_total_complaints.csv"), index=False)
print("Saved monthly_total_complaints.csv")

# Key transition analysis
print("\n=== TRANSITION 1: FedLoan (AES/PHEAA) -> MOHELA ===")
# FedLoan transfer announced June 2021, accounts transferred Dec 2021 - mid 2022
pheaa_monthly = fed[fed["company"] == "AES/PHEAA"].groupby("year_month").size()
mohela_monthly = fed[fed["company"] == "MOHELA"].groupby("year_month").size()

print("\nAES/PHEAA (FedLoan) monthly complaints:")
for p in sorted(pheaa_monthly.index):
    if str(p) >= "2021-06" and str(p) <= "2023-06":
        print(f"  {p}: {pheaa_monthly[p]}")

print("\nMOHELA monthly complaints:")
for p in sorted(mohela_monthly.index):
    if str(p) >= "2021-06" and str(p) <= "2023-06":
        print(f"  {p}: {mohela_monthly[p]}")

# Combined FedLoan+MOHELA to see the handoff
print("\nCombined FedLoan+MOHELA (the transferred portfolio):")
combined = pd.concat([pheaa_monthly, mohela_monthly], axis=1).fillna(0)
combined.columns = ["AES_PHEAA", "MOHELA"]
combined["total"] = combined.sum(axis=1)
for p in sorted(combined.index):
    if str(p) >= "2021-06" and str(p) <= "2023-12":
        row = combined.loc[p]
        print(f"  {p}: PHEAA={int(row['AES_PHEAA'])} MOHELA={int(row['MOHELA'])} total={int(row['total'])}")

print("\n=== TRANSITION 2: Navient -> Aidvantage (Maximus) ===")
# Navient announced exit June 2021, transferred to Aidvantage (Maximus) Jan 2022
navient_monthly = fed[fed["company"] == "Navient Solutions, LLC."].groupby("year_month").size()
maximus_monthly = fed[fed["company"] == "Maximus Federal Services, Inc."].groupby("year_month").size()

print("\nNavient monthly complaints:")
for p in sorted(navient_monthly.index):
    if str(p) >= "2021-06" and str(p) <= "2023-06":
        print(f"  {p}: {navient_monthly[p]}")

print("\nMaximus (Aidvantage) monthly complaints:")
for p in sorted(maximus_monthly.index):
    if str(p) >= "2021-06" and str(p) <= "2023-06":
        print(f"  {p}: {maximus_monthly[p]}")

# Combined Navient+Maximus
nav_combined = pd.concat([navient_monthly, maximus_monthly], axis=1).fillna(0)
nav_combined.columns = ["Navient", "Maximus"]
nav_combined["total"] = nav_combined.sum(axis=1)
print("\nCombined Navient+Maximus:")
for p in sorted(nav_combined.index):
    if str(p) >= "2021-06" and str(p) <= "2023-12":
        row = nav_combined.loc[p]
        print(f"  {p}: Navient={int(row['Navient'])} Maximus={int(row['Maximus'])} total={int(row['total'])}")

print("\n=== COVID FORBEARANCE END: Payment Restart Oct 2023 ===")
# Payments restarted October 2023 after 3.5 year pause
print("\nTotal federal student loan complaints by quarter:")
quarterly = fed.groupby("quarter").size()
for q in sorted(quarterly.index):
    print(f"  {q}: {quarterly[q]}")

print("\n=== YEARLY TOTALS BY SERVICER ===")
yearly_by_company = fed[fed["company"].isin(key_servicers)].groupby(
    ["year", "company"]
).size().unstack(fill_value=0)
print(yearly_by_company.to_string())
yearly_by_company.to_csv(os.path.join(OUT_DIR, "yearly_complaints_by_servicer.csv"))

print("\n=== ISSUE BREAKDOWN AROUND TRANSITIONS ===")
# What are people complaining about during transition periods?
transition_period = fed[
    (fed["date_received"] >= "2022-01-01") & 
    (fed["date_received"] <= "2022-12-31")
]
pre_transition = fed[
    (fed["date_received"] >= "2020-01-01") & 
    (fed["date_received"] <= "2020-12-31")
]

print("\nTop issues during transition (2022):")
print(transition_period["issue"].value_counts().head(10).to_string())

print("\nTop issues pre-transition (2020):")
print(pre_transition["issue"].value_counts().head(10).to_string())

# MOHELA-specific issues during ramp-up
print("\n=== MOHELA ISSUE BREAKDOWN (2022-2023) ===")
mohela_transition = fed[
    (fed["company"] == "MOHELA") & 
    (fed["date_received"] >= "2022-01-01") & 
    (fed["date_received"] <= "2023-12-31")
]
print(mohela_transition["issue"].value_counts().to_string())

# Company response analysis
print("\n=== COMPANY RESPONSE BY SERVICER (2022-2025) ===")
recent = fed[fed["year"] >= 2022]
response_by_company = recent[recent["company"].isin(key_servicers)].groupby(
    ["company", "company_response"]
).size().unstack(fill_value=0)
print(response_by_company.to_string())
response_by_company.to_csv(os.path.join(OUT_DIR, "response_by_servicer.csv"))

# Timeliness
print("\n=== TIMELY RESPONSE RATE BY SERVICER AND YEAR ===")
timely_analysis = fed[fed["company"].isin(key_servicers)].copy()
timely_analysis["timely_bool"] = timely_analysis["timely"] == "Yes"
timely_rate = timely_analysis.groupby(["year", "company"])["timely_bool"].mean()
print(timely_rate.unstack().to_string())

# Payment restart impact
print("\n=== PAYMENT RESTART IMPACT ===")
# Compare H1 2023 (still paused) to H2 2023 (payments restart Oct) to H1 2024
h1_2023 = fed[(fed["date_received"] >= "2023-01-01") & (fed["date_received"] < "2023-07-01")]
h2_2023 = fed[(fed["date_received"] >= "2023-07-01") & (fed["date_received"] < "2024-01-01")]
h1_2024 = fed[(fed["date_received"] >= "2024-01-01") & (fed["date_received"] < "2024-07-01")]

print(f"H1 2023 (payments paused): {len(h1_2023)} complaints")
print(f"H2 2023 (payments restart Oct): {len(h2_2023)} complaints")
print(f"H1 2024 (payments active): {len(h1_2024)} complaints")
print(f"Change H1->H2 2023: {((len(h2_2023)/len(h1_2023))-1)*100:.1f}%")
print(f"Change H2 2023->H1 2024: {((len(h1_2024)/len(h2_2023))-1)*100:.1f}%")

# Top servicer complaints in 2025 (current)
print("\n=== 2025 COMPLAINTS BY SERVICER ===")
complaints_2025 = fed[fed["year"] >= 2025]
print(complaints_2025["company"].value_counts().head(10).to_string())
print(f"\nTotal 2025+: {len(complaints_2025)}")

# Save key summary data
summary = {
    "total_complaints": len(df),
    "federal_complaints": len(fed),
    "date_range": f"{df['date_received'].min()} to {df['date_received'].max()}",
    "key_servicers_complaint_counts": fed[fed["company"].isin(key_servicers)]["company"].value_counts().to_dict(),
}
with open(os.path.join(OUT_DIR, "summary.json"), "w") as f:
    json.dump(summary, f, indent=2, default=str)

print("\n=== DONE ===")
