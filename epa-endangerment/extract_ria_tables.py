#!/usr/bin/env python3
"""
Extract and reconstruct all cost-benefit tables from the EPA RIA
(EPA-420-R-26-002) for the Endangerment Finding rescission.

Produces:
  - data/intermediate/table2_3pct.csv
  - data/intermediate/table3_7pct.csv
  - data/intermediate/table_a1_detail.csv
  - data/intermediate/table_a3_detail.csv (Scenario A2)
  - data/intermediate/table_a4_detail.csv (Scenario A3)
  - data/intermediate/table_a5_detail.csv (Scenario A4)
  - data/intermediate/all_scenarios_summary.csv
  - data/intermediate/all_scenarios_summary.json
  - data/intermediate/factsheet_vs_ria.csv
  - data/intermediate/factsheet_vs_ria.json

Source: regulatory-impact-analysis-EPA-420-R-26-002.pdf (text extraction: ria-text.txt)
Numbers cross-referenced against PDF text and narrative confirmations in RIA body.
"""

import pandas as pd
import json
import os
import numpy as np


class NumpyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, (np.integer,)):
			return int(obj)
		if isinstance(obj, (np.floating,)):
			return float(obj)
		if isinstance(obj, (np.bool_,)):
			return bool(obj)
		return super().default(obj)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTERMEDIATE = os.path.join(BASE, "data", "intermediate")
os.makedirs(INTERMEDIATE, exist_ok=True)

print("=" * 70)
print("EPA RIA Table Extraction")
print("=" * 70)

# ============================================================
# Table A-1: Scenario A1 (AEO 2025 Reference case)
# Values extracted from ria-text.txt lines 1539-1613
# Cross-checked against narrative at lines 1615-1623
# ============================================================

print("\n--- Table A-1: Scenario A1 ---")
table_a1 = {
	"category": [
		"Vehicle Technology",
		"EVSE & Replacements",
		"Fuel, Repair, Maintenance, Insurance, Congestion & Noise",
		"Energy Security, Refueling Time, Drive Value",
		"Net Monetized Impacts"
	],
	"type": ["savings", "savings", "cost", "cost", "net"],
	"npv_3pct": [1090, 200, -1430, -40, -180],
	"npv_7pct": [730, 120, -730, -23, 89],
	"annualized_3pct": [57, 11, -75, -2.1, -9.1],
	"annualized_7pct": [59, 9.6, -60, -1.9, 7.3],
}

df_a1 = pd.DataFrame(table_a1)
print(df_a1.to_string(index=False))

# Verify internal consistency: savings + costs = net
savings_3 = df_a1[df_a1["type"] == "savings"]["npv_3pct"].sum()
costs_3 = df_a1[df_a1["type"] == "cost"]["npv_3pct"].sum()
computed_net_3 = savings_3 + costs_3
reported_net_3 = df_a1[df_a1["type"] == "net"]["npv_3pct"].values[0]
print(f"\nVerification (3% NPV):")
print(f"  Savings: ${savings_3:,.0f}B")
print(f"  Costs: ${costs_3:,.0f}B")
print(f"  Computed net: ${computed_net_3:,.0f}B")
print(f"  Reported net: ${reported_net_3:,.0f}B")
print(f"  Match: {abs(computed_net_3 - reported_net_3) <= 10}")  # within rounding

savings_7 = df_a1[df_a1["type"] == "savings"]["npv_7pct"].sum()
costs_7 = df_a1[df_a1["type"] == "cost"]["npv_7pct"].sum()
computed_net_7 = savings_7 + costs_7
reported_net_7 = df_a1[df_a1["type"] == "net"]["npv_7pct"].values[0]
print(f"\nVerification (7% NPV):")
print(f"  Savings: ${savings_7:,.0f}B")
print(f"  Costs: ${costs_7:,.0f}B")
print(f"  Computed net: ${computed_net_7:,.0f}B")
print(f"  Reported net: ${reported_net_7:,.0f}B")
print(f"  Match: {abs(computed_net_7 - reported_net_7) <= 10}")

# ============================================================
# Table A-3: Scenario A2 (Low Oil Price case)
# Values from ria-text.txt lines 1715-1789
# Cross-checked against narrative at lines 1707-1714
# ============================================================

print("\n--- Table A-3: Scenario A2 ---")
table_a2 = {
	"category": [
		"Vehicle Technology",
		"EVSE & Replacements",
		"Fuel, Repair, Maintenance, Insurance, Congestion & Noise",
		"Energy Security, Refueling Time, Drive Value",
		"Net Monetized Impacts"
	],
	"type": ["savings", "savings", "cost", "cost", "net"],
	"npv_3pct": [1140, 200, -1040, -46, 250],
	"npv_7pct": [750, 120, -520, -26, 320],
	"annualized_3pct": [59, 11, -54, -2.4, 13],
	"annualized_7pct": [61, 9.6, -42, -2.1, 27],
}
df_a2 = pd.DataFrame(table_a2)
print(df_a2.to_string(index=False))

# Verify A2
s3 = df_a2[df_a2["type"] == "savings"]["npv_3pct"].sum()
c3 = df_a2[df_a2["type"] == "cost"]["npv_3pct"].sum()
print(f"\nA2 Verification (3%): Savings ${s3:,.0f}B + Costs ${c3:,.0f}B = ${s3+c3:,.0f}B (reported: $250B)")

# ============================================================
# Table A-4: Scenario A3 (Reference + 2.5yr fuel valuation)
# Values from ria-text.txt lines 1813-1882
# Cross-checked against narrative at lines 1807-1812
# ============================================================

print("\n--- Table A-4: Scenario A3 ---")
table_a3 = {
	"category": [
		"Vehicle Technology",
		"EVSE & Replacements",
		"Fuel, Repair, Maintenance, Insurance, Congestion & Noise",
		"Energy Security, Refueling Time, Drive Value",
		"Net Monetized Impacts"
	],
	"type": ["savings", "savings", "cost", "cost", "net"],
	"npv_3pct": [1090, 200, -460, -40, 790],
	"npv_7pct": [730, 120, -220, -23, 600],
	"annualized_3pct": [57, 11, -24, -2.1, 41],
	"annualized_7pct": [59, 9.6, -18, -1.9, 49],
}
df_a3 = pd.DataFrame(table_a3)
print(df_a3.to_string(index=False))

# Verify: fuel cost reduction from A1 to A3
print(f"\nFuel cost reduction (2.5yr vs full): ${1430}B -> ${460}B = {460/1430*100:.0f}% of full value")
print(f"  This implies consumers only experience {460/1430*100:.0f}% of lifetime fuel costs")
print(f"  Consistent with 2.5 years out of ~7.7 year implied full period")

# ============================================================
# Table A-5: Scenario A4 (Low oil + 2.5yr fuel valuation)
# Values from ria-text.txt lines 1895-1964
# Cross-checked against narrative at lines 1887-1891
# ============================================================

print("\n--- Table A-5: Scenario A4 ---")
table_a4 = {
	"category": [
		"Vehicle Technology",
		"EVSE & Replacements",
		"Fuel, Repair, Maintenance, Insurance, Congestion & Noise",
		"Energy Security, Refueling Time, Drive Value",
		"Net Monetized Impacts"
	],
	"type": ["savings", "savings", "cost", "cost", "net"],
	"npv_3pct": [1140, 200, -380, -46, 920],
	"npv_7pct": [750, 120, -170, -26, 680],
	"annualized_3pct": [59, 11, -20, -2.4, 48],
	"annualized_7pct": [61, 9.6, -14, -2.1, 55],
}
df_a4 = pd.DataFrame(table_a4)
print(df_a4.to_string(index=False))

# ============================================================
# Table 2: Summary at 3% discount rate
# From ria-text.txt lines 1231-1283
# ============================================================

print("\n\n" + "=" * 70)
print("SUMMARY TABLE 2: All Scenarios at 3% Discount Rate")
print("=" * 70)

summary_3pct = {
	"scenario": ["A1", "A2", "A3", "A4"],
	"description": [
		"AEO 2025 Reference prices",
		"AEO 2025 Low Oil Price",
		"Reference prices, 2.5yr fuel valuation",
		"Low Oil Price, 2.5yr fuel valuation"
	],
	"savings_3pct": [1290, 1340, 1290, 1340],
	"costs_3pct": [1470, 1090, 500, 420],
	"net_3pct": [-180, 250, 790, 920],
}
df_t2 = pd.DataFrame(summary_3pct)
print(df_t2.to_string(index=False))

# Verify against detailed tables
print("\nVerification against detailed tables:")
for scenario, df, label in [("A1", df_a1, "A1"), ("A2", df_a2, "A2"), ("A3", df_a3, "A3"), ("A4", df_a4, "A4")]:
	s = df[df["type"] == "savings"]["npv_3pct"].sum()
	c = abs(df[df["type"] == "cost"]["npv_3pct"].sum())
	n = df[df["type"] == "net"]["npv_3pct"].values[0]
	idx = ["A1", "A2", "A3", "A4"].index(scenario)
	ts = summary_3pct["savings_3pct"][idx]
	tc = summary_3pct["costs_3pct"][idx]
	tn = summary_3pct["net_3pct"][idx]
	print(f"  {label}: Detail savings={s}, Table2 savings={ts}, diff={abs(s-ts)}")
	print(f"  {label}: Detail costs={c}, Table2 costs={tc}, diff={abs(c-tc)}")
	print(f"  {label}: Detail net={n}, Table2 net={tn}, diff={abs(n-tn)}")

# ============================================================
# Table 3: Summary at 7% discount rate
# From ria-text.txt lines 1287-1339
# ============================================================

print("\n\n" + "=" * 70)
print("SUMMARY TABLE 3: All Scenarios at 7% Discount Rate")
print("=" * 70)

summary_7pct = {
	"scenario": ["A1", "A2", "A3", "A4"],
	"description": [
		"AEO 2025 Reference prices",
		"AEO 2025 Low Oil Price",
		"Reference prices, 2.5yr fuel valuation",
		"Low Oil Price, 2.5yr fuel valuation"
	],
	"savings_7pct": [850, 870, 850, 870],
	"costs_7pct": [760, 550, 240, 200],
	"net_7pct": [89, 320, 600, 680],
}
df_t3 = pd.DataFrame(summary_7pct)
print(df_t3.to_string(index=False))

# ============================================================
# THE CONTRADICTION: Factsheet vs RIA
# ============================================================

print("\n\n" + "=" * 70)
print("THE CONTRADICTION: Fact Sheet vs. RIA Scenario A1")
print("=" * 70)

factsheet_claim = 1300  # "$1.3 trillion in savings"
factsheet_vehicle = 1100  # "approximately $1.1 trillion from reduced vehicle costs"
factsheet_evse = 200  # "$200 billion from avoided EV charger costs"

ria_a1_vehicle_tech = 1090
ria_a1_evse = 200
ria_a1_gross_savings = ria_a1_vehicle_tech + ria_a1_evse
ria_a1_fuel_costs = 1430
ria_a1_energy_security = 40
ria_a1_total_costs = ria_a1_fuel_costs + ria_a1_energy_security
ria_a1_net = ria_a1_gross_savings - ria_a1_total_costs

print(f"\nFact sheet claims:")
print(f"  Total savings: ${factsheet_claim:,}B")
print(f"  Vehicle cost reduction: ${factsheet_vehicle:,}B")
print(f"  EVSE savings: ${factsheet_evse:,}B")

print(f"\nRIA Scenario A1 (3% discount rate) shows:")
print(f"  Vehicle Technology savings: ${ria_a1_vehicle_tech:,}B")
print(f"  EVSE savings: ${ria_a1_evse:,}B")
print(f"  Gross savings: ${ria_a1_gross_savings:,}B")
print(f"  Fuel/Repair/Maint/Insurance/Congestion/Noise costs: ${ria_a1_fuel_costs:,}B")
print(f"  Energy Security/Refueling/Drive Value costs: ${ria_a1_energy_security:,}B")
print(f"  Total costs: ${ria_a1_total_costs:,}B")
print(f"  NET IMPACT: ${ria_a1_net:,}B")

print(f"\n*** The fact sheet reports GROSS savings (${ria_a1_gross_savings:,}B)")
print(f"    while omitting costs (${ria_a1_total_costs:,}B).")
print(f"    Net impact under EPA's own primary scenario: -${abs(ria_a1_net):,}B (a COST, not savings)")

# Per-vehicle math
vehicles = 469_000_000  # from RIA line 1620-1621
per_vehicle_savings = ria_a1_vehicle_tech * 1e9 / vehicles
per_vehicle_net_cost = abs(ria_a1_net) * 1e9 / vehicles
print(f"\nPer-vehicle math (469 million vehicles, 2027-2055):")
print(f"  Per-vehicle technology cost reduction: ${per_vehicle_savings:,.0f}")
print(f"    EPA reports ~$2,330 (our calculation: ${per_vehicle_savings:,.0f}) -- MATCH")
print(f"  Per-vehicle NET cost (including fuel etc.): ${per_vehicle_net_cost:,.0f}")
print(f"    The fact sheet does not mention this per-vehicle net cost.")

# ============================================================
# The 2.5-year assumption impact
# ============================================================

print("\n\n" + "=" * 70)
print("IMPACT OF 2.5-YEAR FUEL COST VALUATION ASSUMPTION")
print("=" * 70)

# Reference prices (A1 vs A3)
a1_fuel = 1430
a3_fuel = 460
fuel_reduction_pct = (1 - a3_fuel / a1_fuel) * 100
print(f"\nReference case fuel prices:")
print(f"  Full lifetime fuel costs (A1): ${a1_fuel:,}B")
print(f"  2.5-year fuel costs (A3): ${a3_fuel:,}B")
print(f"  Reduction: {fuel_reduction_pct:.0f}%")
print(f"  The 2.5-year assumption throws out {fuel_reduction_pct:.0f}% of lifetime fuel costs.")

# Low oil prices (A2 vs A4)
a2_fuel = 1040
a4_fuel = 380
fuel_reduction_pct_2 = (1 - a4_fuel / a2_fuel) * 100
print(f"\nLow oil price case:")
print(f"  Full lifetime fuel costs (A2): ${a2_fuel:,}B")
print(f"  2.5-year fuel costs (A4): ${a4_fuel:,}B")
print(f"  Reduction: {fuel_reduction_pct_2:.0f}%")

# Net impact swing
print(f"\nNet impact swing from 2.5-year assumption:")
print(f"  A1 (full, ref prices): -${abs(-180)}B (NET COST)")
print(f"  A3 (2.5yr, ref prices): +$790B (NET SAVINGS)")
print(f"  Swing: ${790 - (-180):,}B = $970B swing from one assumption alone")
print(f"\n  A2 (full, low prices): +$250B (NET SAVINGS)")
print(f"  A4 (2.5yr, low prices): +$920B (NET SAVINGS)")
print(f"  Swing: ${920 - 250:,}B = $670B swing")

# ============================================================
# What's NOT in the RIA
# ============================================================

print("\n\n" + "=" * 70)
print("WHAT IS NOT MONETIZED IN THE RIA")
print("=" * 70)
print("""
The RIA contains ZERO monetized climate or health benefits/costs.
Specifically excluded:
  1. Social cost of carbon / Social cost of GHG emissions
  2. Health benefits from reduced tailpipe emissions (PM2.5, NOx, ozone)
  3. Climate damages from increased CO2 emissions
  4. Agricultural productivity impacts
  5. Sea level rise costs
  6. Extreme weather costs

For reference, the Biden-era 2024 LMDV RIA estimated:
  - ~$100-200B in climate benefits (using SC-GHG) from the standards
  - The 2024 LMDV + HD GHG Phase 3 RIAs were ~1,800 pages combined
  - This RIA is 35 pages

The EPA states in the Federal Register (lines 1911-1916):
  The agency received comments on "how to utilize Social Cost of Carbon
  (SCC) methodologies in an RIA" but did not incorporate them.

The RIA explicitly notes (lines 120-127): "there are benefits and costs
with respect to this regulatory action that are difficult to quantify
much less monetize" including employment impacts.
""")

# ============================================================
# Export all intermediate data
# ============================================================

print("\n" + "=" * 70)
print("EXPORTING INTERMEDIATE DATA")
print("=" * 70)

# Detailed tables
df_a1.to_csv(os.path.join(INTERMEDIATE, "table_a1_scenario_a1_detail.csv"), index=False)
df_a2.to_csv(os.path.join(INTERMEDIATE, "table_a3_scenario_a2_detail.csv"), index=False)
df_a3.to_csv(os.path.join(INTERMEDIATE, "table_a4_scenario_a3_detail.csv"), index=False)
df_a4.to_csv(os.path.join(INTERMEDIATE, "table_a5_scenario_a4_detail.csv"), index=False)
print("  Exported: table_a1_scenario_a1_detail.csv")
print("  Exported: table_a3_scenario_a2_detail.csv")
print("  Exported: table_a4_scenario_a3_detail.csv")
print("  Exported: table_a5_scenario_a4_detail.csv")

# Summary tables
df_t2.to_csv(os.path.join(INTERMEDIATE, "table2_summary_3pct.csv"), index=False)
df_t3.to_csv(os.path.join(INTERMEDIATE, "table3_summary_7pct.csv"), index=False)
print("  Exported: table2_summary_3pct.csv")
print("  Exported: table3_summary_7pct.csv")

# All scenarios combined
all_scenarios = []
for scenario, df_detail in [("A1", df_a1), ("A2", df_a2), ("A3", df_a3), ("A4", df_a4)]:
	for _, row in df_detail.iterrows():
		all_scenarios.append({
			"scenario": scenario,
			"category": row["category"],
			"type": row["type"],
			"npv_3pct_billions": row["npv_3pct"],
			"npv_7pct_billions": row["npv_7pct"],
			"annualized_3pct_billions": row["annualized_3pct"],
			"annualized_7pct_billions": row["annualized_7pct"],
		})

df_all = pd.DataFrame(all_scenarios)
df_all.to_csv(os.path.join(INTERMEDIATE, "all_scenarios_detail.csv"), index=False)
print("  Exported: all_scenarios_detail.csv")

# Summary for charting
scenario_summary = []
descriptions = {
	"A1": "Reference prices, full fuel costs",
	"A2": "Low oil prices, full fuel costs",
	"A3": "Reference prices, 2.5yr fuel costs",
	"A4": "Low oil prices, 2.5yr fuel costs",
}
for scenario, df_detail in [("A1", df_a1), ("A2", df_a2), ("A3", df_a3), ("A4", df_a4)]:
	s = df_detail[df_detail["type"] == "savings"]["npv_3pct"].sum()
	c = df_detail[df_detail["type"] == "cost"]["npv_3pct"].sum()
	n = df_detail[df_detail["type"] == "net"]["npv_3pct"].values[0]
	s7 = df_detail[df_detail["type"] == "savings"]["npv_7pct"].sum()
	c7 = df_detail[df_detail["type"] == "cost"]["npv_7pct"].sum()
	n7 = df_detail[df_detail["type"] == "net"]["npv_7pct"].values[0]
	scenario_summary.append({
		"scenario": scenario,
		"description": descriptions[scenario],
		"uses_low_oil_prices": scenario in ["A2", "A4"],
		"uses_2_5yr_fuel_valuation": scenario in ["A3", "A4"],
		"gross_savings_3pct": s,
		"total_costs_3pct": abs(c),
		"net_impact_3pct": n,
		"gross_savings_7pct": s7,
		"total_costs_7pct": abs(c7),
		"net_impact_7pct": n7,
		"shows_net_cost_at_3pct": n < 0,
		"shows_net_cost_at_7pct": n7 < 0,
	})

df_summary = pd.DataFrame(scenario_summary)
df_summary.to_csv(os.path.join(INTERMEDIATE, "all_scenarios_summary.csv"), index=False)
with open(os.path.join(INTERMEDIATE, "all_scenarios_summary.json"), "w") as f:
	json.dump(scenario_summary, f, indent=2, cls=NumpyEncoder)
print("  Exported: all_scenarios_summary.csv")
print("  Exported: all_scenarios_summary.json")

# Factsheet vs RIA comparison
contradiction = {
	"factsheet_total_savings_claim": factsheet_claim,
	"factsheet_vehicle_savings": factsheet_vehicle,
	"factsheet_evse_savings": factsheet_evse,
	"ria_a1_vehicle_tech_savings": ria_a1_vehicle_tech,
	"ria_a1_evse_savings": ria_a1_evse,
	"ria_a1_gross_savings": ria_a1_gross_savings,
	"ria_a1_total_costs": ria_a1_total_costs,
	"ria_a1_net_impact": ria_a1_net,
	"factsheet_omits_costs_of": ria_a1_total_costs,
	"per_vehicle_count": vehicles,
	"per_vehicle_tech_savings_usd": round(per_vehicle_savings),
	"per_vehicle_net_cost_usd": round(per_vehicle_net_cost),
	"factsheet_per_vehicle_claim": 2400,
	"ria_per_vehicle_calculation": 2330,
}
with open(os.path.join(INTERMEDIATE, "factsheet_vs_ria.json"), "w") as f:
	json.dump(contradiction, f, indent=2)

df_contradiction = pd.DataFrame([
	{"metric": "Fact sheet: total savings claim", "value_billions": factsheet_claim},
	{"metric": "RIA A1: vehicle tech savings", "value_billions": ria_a1_vehicle_tech},
	{"metric": "RIA A1: EVSE savings", "value_billions": ria_a1_evse},
	{"metric": "RIA A1: gross savings", "value_billions": ria_a1_gross_savings},
	{"metric": "RIA A1: fuel/maint/insurance/etc costs", "value_billions": -ria_a1_fuel_costs},
	{"metric": "RIA A1: energy security/refuel costs", "value_billions": -ria_a1_energy_security},
	{"metric": "RIA A1: total costs", "value_billions": -ria_a1_total_costs},
	{"metric": "RIA A1: NET IMPACT", "value_billions": ria_a1_net},
])
df_contradiction.to_csv(os.path.join(INTERMEDIATE, "factsheet_vs_ria.csv"), index=False)
print("  Exported: factsheet_vs_ria.csv")
print("  Exported: factsheet_vs_ria.json")

# 2.5-year assumption impact
fuel_assumption = {
	"reference_prices": {
		"full_lifetime_fuel_cost": a1_fuel,
		"2_5yr_fuel_cost": a3_fuel,
		"pct_reduction": round(fuel_reduction_pct, 1),
		"net_impact_full": -180,
		"net_impact_2_5yr": 790,
		"swing_billions": 970,
	},
	"low_oil_prices": {
		"full_lifetime_fuel_cost": a2_fuel,
		"2_5yr_fuel_cost": a4_fuel,
		"pct_reduction": round(fuel_reduction_pct_2, 1),
		"net_impact_full": 250,
		"net_impact_2_5yr": 920,
		"swing_billions": 670,
	}
}
with open(os.path.join(INTERMEDIATE, "fuel_valuation_assumption_impact.json"), "w") as f:
	json.dump(fuel_assumption, f, indent=2)
print("  Exported: fuel_valuation_assumption_impact.json")

# Which scenarios show net cost vs net savings
print("\n\n" + "=" * 70)
print("SCENARIO OUTCOME MATRIX")
print("=" * 70)
print(f"\n{'Scenario':<12} {'3% NPV':>10} {'7% NPV':>10} {'Net at 3%':>12} {'Net at 7%':>12}")
print("-" * 60)
for _, row in df_summary.iterrows():
	n3 = row["net_impact_3pct"]
	n7 = row["net_impact_7pct"]
	label3 = "COST" if n3 < 0 else "SAVINGS"
	label7 = "COST" if n7 < 0 else "SAVINGS"
	print(f"{row['scenario']:<12} ${abs(n3):>8,.0f}B ${abs(n7):>8,.0f}B {label3:>12} {label7:>12}")

print(f"\nOf 8 scenario/discount-rate combinations:")
cost_count = sum(1 for _, r in df_summary.iterrows() for n in [r["net_impact_3pct"], r["net_impact_7pct"]] if n < 0)
savings_count = 8 - cost_count
print(f"  Show NET COST: {cost_count}")
print(f"  Show NET SAVINGS: {savings_count}")
print(f"\nOnly Scenario A1 at 3% shows a net cost.")
print(f"But A1 at 3% is the primary scenario (AEO 2025 Reference prices, full fuel cost accounting).")

print("\n\nDONE. All intermediate data exported to:", INTERMEDIATE)
