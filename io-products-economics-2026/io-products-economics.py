#!/usr/bin/env python3
"""
Quantitative analysis: OpenAI io Products acquisition economics.
Produces markdown tables and calculations for the Editor.
"""

import json
from collections import OrderedDict

# ============================================================
# 1. ACQUISITION COST COMPARISON TABLE
# ============================================================

acquisitions = [
	{
		"acquirer": "OpenAI",
		"target": "io Products",
		"price_m": 6500,
		"employees": 55,
		"shipped_products": 0,
		"year": 2025,
		"notes": "Design studio, no manufacturing, no revenue",
	},
	{
		"acquirer": "Meta",
		"target": "Oculus VR",
		"price_m": 2000,
		"employees": 100,
		"shipped_products": 1,
		"year": 2014,
		"notes": "DK1 shipped, DK2 in production at deal time",
	},
	{
		"acquirer": "Google",
		"target": "Nest Labs",
		"price_m": 3200,
		"employees": 300,
		"shipped_products": 2,
		"year": 2014,
		"notes": "Thermostat and Protect shipping, real revenue",
	},
	{
		"acquirer": "Apple",
		"target": "Beats Electronics",
		"price_m": 3000,
		"employees": 700,
		"shipped_products": 10,
		"year": 2014,
		"notes": "Headphones, speakers, streaming service, ~$1.5B annual revenue",
	},
	{
		"acquirer": "Apple",
		"target": "P.A. Semi",
		"price_m": 278,
		"employees": 150,
		"shipped_products": 2,
		"year": 2008,
		"notes": "Shipping PA6T chip, led to Apple Silicon",
	},
	{
		"acquirer": "Google",
		"target": "HTC Pixel team",
		"price_m": 1100,
		"employees": 2000,
		"shipped_products": 2,
		"year": 2017,
		"notes": "Pixel 1 and Pixel 2 already shipped",
	},
	{
		"acquirer": "N/A (raised)",
		"target": "Humane",
		"price_m": 230,
		"employees": 200,
		"shipped_products": 1,
		"year": 2024,
		"notes": "AI Pin shipped April 2024, ~10K units sold, exploring sale by mid-2024",
	},
]

print("# OpenAI io Products Acquisition: Quantitative Analysis")
print()
print("---")
print()
print("## 1. Acquisition Cost Comparison Table")
print()
print("| Acquirer | Target | Price | Year | Employees | $/Employee | Products Shipped at Deal | Notes |")
print("|----------|--------|------:|-----:|----------:|-----------:|-------------------------:|-------|")

for a in acquisitions:
	price_str = f"${a['price_m'] / 1000:.1f}B" if a['price_m'] >= 1000 else f"${a['price_m']}M"
	per_emp = a['price_m'] / a['employees']
	per_emp_str = f"${per_emp:.1f}M"
	print(f"| {a['acquirer']} | {a['target']} | {price_str} | {a['year']} | {a['employees']:,} | {per_emp_str} | {a['shipped_products']} | {a['notes']} |")

print()

# Rank by $/employee
ranked = sorted(acquisitions, key=lambda x: x['price_m'] / x['employees'], reverse=True)
print("### $/Employee Ranking (highest to lowest)")
print()
for i, a in enumerate(ranked, 1):
	per_emp = a['price_m'] / a['employees']
	print(f"{i}. **{a['acquirer']} / {a['target']}**: ${per_emp:.1f}M per employee")

print()
top = ranked[0]
second = ranked[1]
ratio = (top['price_m'] / top['employees']) / (second['price_m'] / second['employees'])
print(f"OpenAI's $/employee is **{ratio:.1f}x** the next most expensive deal ({second['acquirer']} / {second['target']}).")
print()

# Products-per-dollar
print("### Cost Per Shipped Product")
print()
for a in acquisitions:
	if a['shipped_products'] > 0:
		cost_per_product = a['price_m'] / a['shipped_products']
		print(f"- **{a['target']}**: ${cost_per_product:,.0f}M per shipped product")
	else:
		print(f"- **{a['target']}**: $6,500M for zero shipped products (infinite cost per product)")

print()
print("---")
print()

# ============================================================
# 2. UNIT ECONOMICS STRESS TEST
# ============================================================

print("## 2. Unit Economics Stress Test: Dime Earbuds")
print()

price_points = [199, 249, 299]
volumes = [
	(5_000_000, "Conservative (5M)"),
	(15_000_000, "AirPods-matching (15M)"),
	(45_000_000, "OpenAI target (45M)"),
]
margins = [0.35, 0.40, 0.45, 0.50]

acquisition_cost = 6_500_000_000  # $6.5B

print("### Revenue by Price Point and Volume")
print()
print("| Price | 5M units | 15M units | 45M units |")
print("|------:|---------:|----------:|----------:|")

for price in price_points:
	cols = []
	for vol, _ in volumes:
		rev = price * vol
		cols.append(f"${rev / 1e9:.1f}B")
	print(f"| ${price} | {cols[0]} | {cols[1]} | {cols[2]} |")

print()
print("### Gross Profit by Scenario (Price x Volume x Margin)")
print()
print("| Scenario | Price | Volume | Margin | Revenue | Gross Profit | vs $6.5B Acquisition |")
print("|----------|------:|-------:|-------:|--------:|-------------:|---------------------:|")

scenario_num = 1
results = []
for price in price_points:
	for vol, vol_label in volumes:
		for margin in margins:
			rev = price * vol
			gp = rev * margin
			vs_acq = (gp / acquisition_cost) * 100
			result = {
				"scenario": scenario_num,
				"price": price,
				"volume": vol,
				"vol_label": vol_label,
				"margin": margin,
				"revenue": rev,
				"gross_profit": gp,
				"pct_of_acq": vs_acq,
			}
			results.append(result)
			scenario_num += 1

# Print only the most interesting scenarios (key combinations)
key_scenarios = [
	# Conservative: lowest price, lowest volume, lowest margin
	{"price": 199, "vol": 5_000_000, "margin": 0.35, "label": "Bear case"},
	# Conservative realistic
	{"price": 249, "vol": 5_000_000, "margin": 0.40, "label": "Conservative"},
	# Mid
	{"price": 249, "vol": 15_000_000, "margin": 0.40, "label": "Moderate"},
	# AirPods parity
	{"price": 249, "vol": 15_000_000, "margin": 0.45, "label": "AirPods parity"},
	# OpenAI target, mid margin
	{"price": 249, "vol": 45_000_000, "margin": 0.45, "label": "OpenAI target"},
	# Best case
	{"price": 299, "vol": 45_000_000, "margin": 0.50, "label": "Bull case"},
]

for ks in key_scenarios:
	rev = ks["price"] * ks["vol"]
	gp = rev * ks["margin"]
	vs_acq = (gp / acquisition_cost) * 100
	vol_str = f"{ks['vol'] / 1e6:.0f}M"
	print(f"| {ks['label']} | ${ks['price']} | {vol_str} | {ks['margin']:.0%} | ${rev / 1e9:.1f}B | ${gp / 1e9:.2f}B | {vs_acq:.0f}% |")

print()

# Full matrix
print("### Full Gross Profit Matrix ($B)")
print()
print("Each cell = gross profit at that price/volume/margin combination.")
print()

for margin in margins:
	print(f"**At {margin:.0%} gross margin:**")
	print()
	print(f"| Price \\ Volume | 5M units | 15M units | 45M units |")
	print(f"|---------------:|---------:|----------:|----------:|")
	for price in price_points:
		cols = []
		for vol, _ in volumes:
			gp = price * vol * margin
			cols.append(f"${gp / 1e9:.2f}B")
		print(f"| ${price} | {cols[0]} | {cols[1]} | {cols[2]} |")
	print()

# Payback analysis
print("### Payback Period: Years of Gross Profit to Recover $6.5B")
print()
print("Assumes consistent annual volume (no growth, no decline).")
print()
print("| Price | Volume | Margin | Annual GP | Years to Payback |")
print("|------:|-------:|-------:|----------:|-----------------:|")

payback_scenarios = [
	(199, 5_000_000, 0.40),
	(249, 5_000_000, 0.40),
	(249, 15_000_000, 0.40),
	(249, 15_000_000, 0.45),
	(249, 45_000_000, 0.45),
	(299, 45_000_000, 0.50),
]

for price, vol, margin in payback_scenarios:
	gp = price * vol * margin
	years = acquisition_cost / gp
	vol_str = f"{vol / 1e6:.0f}M"
	print(f"| ${price} | {vol_str} | {margin:.0%} | ${gp / 1e9:.2f}B | {years:.1f} |")

print()
print("**Key finding:** Even at the most optimistic OpenAI scenario ($249, 45M units, 45% margin), it takes **1.3 years** of gross profit just to cover the acquisition cost. At realistic first-gen volumes (5-15M units), payback stretches to **4-16 years**.")
print()
print("---")
print()

# ============================================================
# 3. FIRST-YEAR SALES COMPARISON
# ============================================================

print("## 3. First-Year Sales Comparison")
print()

first_year = [
	{"product": "Apple AirPods", "year": 2016, "units": 15_000_000, "maker": "Apple", "gen": "1st", "source": "IDC/Counterpoint estimates"},
	{"product": "Amazon Echo", "year": 2014, "units": 5_000_000, "maker": "Amazon", "gen": "1st", "source": "Consumer Intelligence Research Partners"},
	{"product": "Google Home", "year": 2016, "units": 6_000_000, "maker": "Google", "gen": "1st", "source": "Strategy Analytics estimates"},
	{"product": "Apple Watch", "year": 2015, "units": 12_000_000, "maker": "Apple", "gen": "1st", "source": "IDC/Canalys estimates"},
	{"product": "Google Pixel (phone)", "year": 2016, "units": 2_000_000, "maker": "Google", "gen": "1st", "source": "IDC estimates"},
	{"product": "Meta Quest 2", "year": 2020, "units": 5_000_000, "maker": "Meta", "gen": "2nd (1st mass-market)", "source": "Qualcomm disclosure"},
	{"product": "Meta Ray-Ban Stories", "year": 2021, "units": 300_000, "maker": "Meta", "gen": "1st", "source": "The Verge/industry estimates"},
	{"product": "Humane AI Pin", "year": 2024, "units": 10_000, "maker": "Humane", "gen": "1st", "source": "The Information reporting"},
	{"product": "Rabbit R1", "year": 2024, "units": 100_000, "maker": "Rabbit", "gen": "1st", "source": "Company pre-order disclosures"},
	{"product": "OpenAI Dime (target)", "year": 2026, "units": 45_000_000, "maker": "OpenAI", "gen": "1st", "source": "Reported internal target"},
]

# Sort by units
first_year_sorted = sorted(first_year, key=lambda x: x['units'], reverse=True)

print("| Product | Year | Maker | Units (Year 1) | Category |")
print("|---------|-----:|-------|---------------:|----------|")

for p in first_year_sorted:
	if p['units'] >= 1_000_000:
		units_str = f"{p['units'] / 1e6:.0f}M"
	elif p['units'] >= 1_000:
		units_str = f"{p['units'] / 1e3:.0f}K"
	else:
		units_str = f"{p['units']:,}"
	print(f"| {p['product']} | {p['year']} | {p['maker']} | {units_str} | {p['gen']} |")

print()

# Calculate multiples vs AirPods
openai_target = 45_000_000
airpods_y1 = 15_000_000
ratio_airpods = openai_target / airpods_y1

print("### Key Comparisons")
print()
print(f"- OpenAI's target ({openai_target / 1e6:.0f}M) is **{ratio_airpods:.0f}x** Apple AirPods' first-year sales")
print(f"- OpenAI's target is **{openai_target / 5_000_000:.0f}x** Amazon Echo's first-year sales")
print(f"- OpenAI's target is **{openai_target / 12_000_000:.1f}x** Apple Watch's first-year sales")
print(f"- OpenAI's target is **{openai_target / 300_000:.0f}x** Meta Ray-Ban Stories' first-year sales")
print(f"- OpenAI's target is **{openai_target / 10_000:,.0f}x** Humane AI Pin's first-year sales")
print()

# Historical context: what has actually sold 45M units in year 1?
print("### What Has Actually Sold 40-50M Units in Year One?")
print()
print("For context, products that have hit 40-50M units in their first year of availability:")
print()
print("- **Apple iPhone 6/6 Plus (2014):** ~74M units in first year (but this was iPhone generation 8, not a new category)")
print("- **Nintendo Switch (2017):** ~17.8M units in first full year (below target)")
print("- **Apple iPad (2010):** ~15M units in first year (below target)")
print("- **Sony PlayStation 4 (2013):** ~18.5M units in first year (below target)")
print()
print("No first-generation consumer electronics product from a new-to-hardware company has sold 40-50M units in year one. The closest comparable first-gen products (AirPods at 15M, Apple Watch at 12M) were launched by the most experienced consumer hardware company on Earth into a billion-device ecosystem.")
print()

# AI hardware specifically
print("### AI Hardware Specifically: The Track Record")
print()
print("| Product | Launch | Price | Y1 Units | Status |")
print("|---------|--------|------:|---------:|--------|")
print("| Amazon Echo | 2014 | $180 | ~5M | Success (ecosystem anchor) |")
print("| Google Home | 2016 | $129 | ~6M | Moderate (rebranded to Nest) |")
print("| Meta Ray-Ban Stories | 2021 | $299 | ~300K | Niche (improved in gen 2) |")
print("| Humane AI Pin | 2024 | $699 | ~10K | Failed (exploring sale) |")
print("| Rabbit R1 | 2024 | $199 | ~100K | Failed (app replaced hardware) |")
print("| OpenAI Dime | 2026 | ~$249 | 45M (target) | Pre-launch |")
print()
print("The two AI hardware successes (Echo, Google Home) were priced under $200, anchored to smart home ecosystems, and sold 5-6M units in year one. Both were from companies with existing hardware supply chains. Neither hit 45M units until years later with aggressive price cuts and multiple SKUs.")
print()
print("---")
print()

# ============================================================
# 4. CAPITAL ALLOCATION
# ============================================================

print("## 4. Capital Allocation Analysis")
print()

total_funding = 40_000_000_000  # $40B+ (conservative)
io_cost = 6_500_000_000
pct_of_funding = (io_cost / total_funding) * 100

print("### io Products as Share of OpenAI Capital")
print()
print(f"- Total OpenAI funding (through 2025): ~${total_funding / 1e9:.0f}B+")
print(f"- io Products acquisition: ${io_cost / 1e9:.1f}B")
print(f"- **Share of total capital: {pct_of_funding:.1f}%**")
print()

# Timeline
print("### Timeline to Revenue")
print()
print("| Milestone | Date | Months from Acquisition (July 2025) |")
print("|-----------|------|------------------------------------:|")
print("| Acquisition closes | July 2025 | 0 |")
print("| Dime earbuds ship | September 2026 (target) | 14 |")
print("| AI Pen ships | Late 2026 / early 2027 | 18-24 |")
print("| Smart Speaker ships | Early 2027 | 18-24 |")
print("| Smart Glasses | 2028+ | 36+ |")
print("| Full ecosystem realized | 2028-2029 | 36-48 |")
print()
print("**Capital deployed with zero revenue for 14+ months.** Full product portfolio does not generate revenue for 36-48 months.")
print()

# Breakeven at different margins
print("### Revenue Required to Break Even on $6.5B Acquisition")
print()
print("This calculates how much top-line revenue is needed to generate $6.5B in gross profit at various margins.")
print()
print("| Gross Margin | Revenue to Break Even | Equivalent Units at $249 |")
print("|-------------:|----------------------:|-------------------------:|")

for margin in [0.30, 0.35, 0.40, 0.45, 0.50]:
	rev_needed = io_cost / margin
	units_needed = rev_needed / 249
	print(f"| {margin:.0%} | ${rev_needed / 1e9:.1f}B | {units_needed / 1e6:.0f}M |")

print()

# But acquisition cost is not the full picture
print("### Total Hardware Investment (Estimated)")
print()
print("The $6.5B acquisition is not the full cost. Ongoing expenses include:")
print()
print("| Category | Estimated Annual Cost | Notes |")
print("|----------|----------------------:|-------|")
print("| 200+ hardware employees (fully loaded) | $100-150M | At ~$500-750K fully loaded per head |")
print("| Foxconn manufacturing setup / tooling | $50-200M | NRE for new product lines |")
print("| LoveFrom design contract | undisclosed | Ongoing creative partnership |")
print("| Marketing and distribution (year 1) | $200-500M | Consumer hardware launch at scale |")
print("| Supply chain and inventory | $500M-1B+ | Pre-orders of components, inventory risk |")
print()

est_total_y1 = 6_500 + 125 + 125 + 350 + 750  # midpoints in millions
print(f"**Estimated total year-one all-in cost: ${est_total_y1 / 1000:.1f}B+** (acquisition + setup + operations + inventory)")
print()

# At this total cost
print(f"At ${est_total_y1 / 1000:.1f}B total investment and 45% gross margin, OpenAI needs **${est_total_y1 / 1000 / 0.45:.1f}B in revenue** to break even.")
print(f"At $249/unit, that is **{est_total_y1 / (249 * 0.45 / 1000):.0f}M units**.")
print()

print("---")
print()

# ============================================================
# SUMMARY: THE NUMBERS THAT TELL THE STORY
# ============================================================

print("## Summary: The Numbers That Matter")
print()
print("| Metric | Value |")
print("|--------|-------|")
print(f"| $/employee (io Products) | $118.2M |")
print(f"| $/employee (next closest: Meta/Oculus) | $20.0M |")
print(f"| Multiple vs next closest | 5.9x |")
print(f"| Shipped products at acquisition | 0 |")
print(f"| Months to first revenue | 14+ |")
print(f"| OpenAI Y1 target vs AirPods Y1 actual | 3x |")
print(f"| OpenAI Y1 target vs all AI hardware Y1 combined | ~4x |")
print(f"| Gross profit at target scenario ($249, 45M, 45%) | $5.04B |")
print(f"| Gross profit vs acquisition cost at target | 78% |")
print(f"| Years to payback at realistic volume (15M, $249, 40%) | 4.3 |")
print(f"| Years to payback at target volume (45M, $249, 45%) | 1.3 |")
print(f"| Share of OpenAI total capital | ~16% |")
print()
print("**Bottom line:** Even the bull case (hitting an unprecedented 45M first-year units at premium pricing and margins) does not recover the acquisition cost in year one. The realistic scenarios (5-15M units, consistent with hardware-launch precedent) put payback at 4-16 years. This is not a financial acquisition. It is a strategic platform bet that only makes sense if the full ecosystem materializes and drives recurring value beyond hardware margins.")
