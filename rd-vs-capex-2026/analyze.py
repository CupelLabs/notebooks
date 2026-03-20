"""
Analyze R&D vs CapEx trends for Big Tech.
Produce clean computed data and findings.
"""
import csv
import json
import os

DATA_DIR = os.path.dirname(__file__) + "/data"

# Load the data
rows = []
with open(os.path.join(DATA_DIR, "rd_vs_capex.csv")) as f:
    for r in csv.DictReader(f):
        r["year"] = int(r["year"])
        r["rd_expense"] = float(r["rd_expense"]) if r["rd_expense"] else None
        r["capex"] = float(r["capex"]) if r["capex"] else None
        r["revenue"] = float(r["revenue"]) if r["revenue"] else None
        rows.append(r)

# Focus on Microsoft, Alphabet, Meta, Apple (2015-2025)
COMPANIES = ["Microsoft", "Alphabet", "Meta", "Apple"]
YEARS = range(2015, 2026)

# Build analysis table
analysis = []
for company in COMPANIES:
    for year in YEARS:
        r = next((r for r in rows if r["company"] == company and r["year"] == year), None)
        if not r or not r["rd_expense"] or not r["capex"]:
            continue
        
        rd = r["rd_expense"]
        capex = r["capex"]
        rev = r["revenue"]
        
        row = {
            "company": company,
            "year": year,
            "rd_billions": round(rd / 1e9, 1),
            "capex_billions": round(capex / 1e9, 1),
            "revenue_billions": round(rev / 1e9, 1) if rev else None,
            "capex_to_rd_ratio": round(capex / rd, 2),
            "rd_pct_revenue": round(rd / rev * 100, 1) if rev else None,
            "capex_pct_revenue": round(capex / rev * 100, 1) if rev else None,
            "capex_minus_rd_billions": round((capex - rd) / 1e9, 1),
        }
        analysis.append(row)

# Save analysis CSV
outfile = os.path.join(DATA_DIR, "analysis.csv")
fields = ["company", "year", "rd_billions", "capex_billions", "revenue_billions",
          "capex_to_rd_ratio", "rd_pct_revenue", "capex_pct_revenue", "capex_minus_rd_billions"]
with open(outfile, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(analysis)

# Save chart-ready JSON
chart_data = {}
for company in COMPANIES:
    chart_data[company] = [r for r in analysis if r["company"] == company]

with open(os.path.join(DATA_DIR, "chart_data.json"), "w") as f:
    json.dump(chart_data, f, indent=2)

# Compute key findings
print("=" * 60)
print("KEY FINDINGS")
print("=" * 60)

for company in COMPANIES:
    data = [r for r in analysis if r["company"] == company]
    
    # Find crossover year
    crossover = None
    for r in data:
        if r["capex_to_rd_ratio"] >= 1.0:
            crossover = r["year"]
            break
    
    latest = data[-1] if data else None
    earliest = next((r for r in data if r["year"] == 2020), data[0])
    
    print(f"\n{company}:")
    print(f"  Capex/R&D ratio: {earliest['capex_to_rd_ratio']} ({earliest['year']}) -> {latest['capex_to_rd_ratio']} ({latest['year']})")
    if crossover:
        print(f"  CROSSOVER YEAR: {crossover} (capex first exceeded R&D)")
    else:
        print(f"  NO CROSSOVER (R&D still exceeds capex)")
    print(f"  2025: R&D=${latest['rd_billions']}B, CapEx=${latest['capex_billions']}B, Gap=${latest['capex_minus_rd_billions']}B")
    if latest.get("capex_pct_revenue") and earliest.get("capex_pct_revenue"):
        print(f"  CapEx as % of revenue: {earliest['capex_pct_revenue']}% ({earliest['year']}) -> {latest['capex_pct_revenue']}% ({latest['year']})")

# Combined totals
print(f"\n{'='*60}")
print("AGGREGATE (Microsoft + Alphabet + Meta)")
print("="*60)

for year in [2020, 2025]:
    big3 = [r for r in analysis if r["company"] in ["Microsoft", "Alphabet", "Meta"] and r["year"] == year]
    total_rd = sum(r["rd_billions"] for r in big3)
    total_capex = sum(r["capex_billions"] for r in big3)
    print(f"  {year}: R&D=${total_rd:.1f}B, CapEx=${total_capex:.1f}B, Ratio={total_capex/total_rd:.2f}")

print(f"\nCapEx growth (2020->2025) for the three that crossed:")
for company in ["Microsoft", "Alphabet", "Meta"]:
    d2020 = next(r for r in analysis if r["company"] == company and r["year"] == 2020)
    d2025 = next(r for r in analysis if r["company"] == company and r["year"] == 2025)
    capex_growth = (d2025["capex_billions"] / d2020["capex_billions"] - 1) * 100
    rd_growth = (d2025["rd_billions"] / d2020["rd_billions"] - 1) * 100
    print(f"  {company}: CapEx +{capex_growth:.0f}%, R&D +{rd_growth:.0f}%")

print(f"\nApple (control):")
a2020 = next(r for r in analysis if r["company"] == "Apple" and r["year"] == 2020)
a2025 = next(r for r in analysis if r["company"] == "Apple" and r["year"] == 2025)
print(f"  CapEx/R&D ratio stayed at {a2020['capex_to_rd_ratio']} -> {a2025['capex_to_rd_ratio']}")
print(f"  R&D=${a2025['rd_billions']}B vs CapEx=${a2025['capex_billions']}B")

print(f"\nSaved analysis.csv and chart_data.json to {DATA_DIR}")
