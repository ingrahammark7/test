import json
from collections import defaultdict

# Load JSON
with open("f.json", "r") as f:
    data = json.load(f)

years_data = data["years"]

# Prepare yearly retirements
yearly_retirements = []
for i, year_entry in enumerate(years_data):
    if i == 0:
        # No prior year, assume no retirements
        retired = 0
    else:
        # Retired = previous year in-service - current year in-service + deliveries this year
        prev_in_service = years_data[i-1]["in_service_estimate"]
        curr_in_service = year_entry["in_service_estimate"]
        deliveries = year_entry["deliveries"] - years_data[i-1]["deliveries"]
        retired = max(prev_in_service + deliveries - curr_in_service, 0)
    yearly_retirements.append({
        "year": year_entry["year"],
        "retired": retired,
        "in_service": year_entry["in_service_estimate"]
    })

# Aggregate into 5-year buckets
buckets = defaultdict(lambda: {"retired": 0, "starting_inventory": 0})

for entry in yearly_retirements:
    year = entry["year"]
    bucket_start = year - (year % 5)  # e.g., 1994 → 1990, 1997 → 1995
    if buckets[bucket_start]["starting_inventory"] == 0:
        # first year of bucket: use starting inventory
        buckets[bucket_start]["starting_inventory"] = entry["in_service"] + entry["retired"]
    buckets[bucket_start]["retired"] += entry["retired"]

# Calculate depreciation rate per bucket
print("5-Year Depreciation Rates for Boeing 777:")
for bucket_start in sorted(buckets.keys()):
    retired = buckets[bucket_start]["retired"]
    starting_inventory = buckets[bucket_start]["starting_inventory"]
    if starting_inventory == 0:
        rate = 0
    else:
        rate = retired / starting_inventory
    print(f"{bucket_start}-{bucket_start+4}: {rate:.2%} ({retired} retired / {starting_inventory} in-service)")