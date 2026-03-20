"""
Fetch R&D expense and Capital Expenditure data from SEC EDGAR XBRL API
for major tech companies. No API key needed, just a User-Agent header.
"""
import json
import urllib.request
import csv
import os
import time

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

COMPANIES = {
    "Microsoft":  "0000789019",
    "Alphabet":   "0001652044",
    "Amazon":     "0001018724",
    "Meta":       "0001326801",
    "Apple":      "0000320193",
    "NVIDIA":     "0001045810",
}

# XBRL taxonomy fields we want
FIELDS = {
    "rd": [
        "ResearchAndDevelopmentExpense",
        "ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost",
    ],
    "capex": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsForCapitalImprovements",
    ],
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
        "Revenue",
        "SalesRevenueNet",
    ],
    "depreciation": [
        "DepreciationAndAmortization",
        "DepreciationDepletionAndAmortization",
        "Depreciation",
    ],
}

HEADERS = {
    "User-Agent": "CupelLabs research@cupellabs.com",
    "Accept": "application/json",
}

def fetch_company_facts(cik):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

def extract_annual_values(facts, field_names):
    """Extract 10-K (annual) values for given XBRL field names."""
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    
    for field in field_names:
        if field not in us_gaap:
            continue
        units = us_gaap[field].get("units", {})
        usd_entries = units.get("USD", [])
        
        # Filter for 10-K annual filings (full year, ~365 day periods)
        annual = []
        for entry in usd_entries:
            form = entry.get("form", "")
            if form not in ("10-K", "10-K/A"):
                continue
            # Only full-year periods (not quarterly)
            start = entry.get("start", "")
            end = entry.get("end", "")
            if start and end:
                from datetime import datetime
                try:
                    s = datetime.strptime(start, "%Y-%m-%d")
                    e = datetime.strptime(end, "%Y-%m-%d")
                    days = (e - s).days
                    if days < 300:  # skip quarterly
                        continue
                except:
                    pass
            
            year = int(entry["end"][:4])
            val = entry["val"]
            annual.append({"year": year, "value": val, "field": field, "end": entry["end"]})
        
        if annual:
            # Deduplicate by year, keeping latest filing
            by_year = {}
            for a in annual:
                y = a["year"]
                if y not in by_year or a["end"] > by_year[y]["end"]:
                    by_year[y] = a
            return by_year
    
    return {}

def main():
    all_data = []
    
    for company, cik in COMPANIES.items():
        print(f"Fetching {company} (CIK: {cik})...")
        try:
            facts = fetch_company_facts(cik)
            # Save raw facts
            with open(os.path.join(DATA_DIR, f"{company.lower()}_facts.json"), "w") as f:
                json.dump(facts, f)
            
            rd = extract_annual_values(facts, FIELDS["rd"])
            capex = extract_annual_values(facts, FIELDS["capex"])
            revenue = extract_annual_values(facts, FIELDS["revenue"])
            depreciation = extract_annual_values(facts, FIELDS["depreciation"])
            
            # Get all years present
            years = sorted(set(list(rd.keys()) + list(capex.keys()) + list(revenue.keys())))
            
            for year in years:
                row = {
                    "company": company,
                    "year": year,
                    "rd_expense": rd.get(year, {}).get("value"),
                    "rd_field": rd.get(year, {}).get("field"),
                    "capex": capex.get(year, {}).get("value"),
                    "capex_field": capex.get(year, {}).get("field"),
                    "revenue": revenue.get(year, {}).get("value"),
                    "revenue_field": revenue.get(year, {}).get("field"),
                    "depreciation": depreciation.get(year, {}).get("value"),
                    "depreciation_field": depreciation.get(year, {}).get("field"),
                }
                all_data.append(row)
                
            print(f"  -> {len(years)} years of data")
            time.sleep(0.2)  # Be nice to EDGAR
            
        except Exception as e:
            print(f"  ERROR: {e}")
    
    # Save combined CSV
    outfile = os.path.join(DATA_DIR, "rd_vs_capex.csv")
    fieldnames = ["company", "year", "rd_expense", "rd_field", "capex", "capex_field", 
                   "revenue", "revenue_field", "depreciation", "depreciation_field"]
    with open(outfile, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)
    
    print(f"\nSaved {len(all_data)} rows to {outfile}")
    
    # Print summary
    print("\n=== SUMMARY ===")
    for company in COMPANIES:
        rows = [r for r in all_data if r["company"] == company]
        recent = [r for r in rows if r["year"] and r["year"] >= 2020]
        for r in sorted(recent, key=lambda x: x["year"]):
            rd_b = f"${r['rd_expense']/1e9:.1f}B" if r['rd_expense'] else "N/A"
            capex_b = f"${r['capex']/1e9:.1f}B" if r['capex'] else "N/A"
            rev_b = f"${r['revenue']/1e9:.1f}B" if r['revenue'] else "N/A"
            ratio = ""
            if r['rd_expense'] and r['capex']:
                ratio = f" (capex/rd={r['capex']/r['rd_expense']:.2f})"
            print(f"  {company} {r['year']}: R&D={rd_b}, CapEx={capex_b}, Rev={rev_b}{ratio}")

if __name__ == "__main__":
    main()
