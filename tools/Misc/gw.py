import numpy as np

# Vehicle mix assumptions (illustrative but realistic structure)

vehicle_mix = {
    "full_size_trucks": {"units": 900_000, "avg_price": 68_000},
    "large_suvs":       {"units": 700_000, "avg_price": 62_000},
    "mid_suvs":         {"units": 650_000, "avg_price": 42_000},
    "crossovers":       {"units": 300_000, "avg_price": 32_000},
    "fleet_vehicles":   {"units": 150_000, "avg_price": 28_000},
}

reported_gmna = 157_000_000_000

total_revenue = 0

print("Segment breakdown:\n")

for k, v in vehicle_mix.items():
    segment_rev = v["units"] * v["avg_price"]
    total_revenue += segment_rev
    
    print(f"{k}:")
    print(f"  units = {v['units']:,}")
    print(f"  avg price = ${v['avg_price']:,}")
    print(f"  revenue = ${segment_rev:,.0f}\n")

print("TOTAL MODELED GMNA:", f"${total_revenue:,.0f}")
print("REPORTED GMNA:", f"${reported_gmna:,.0f}")
print("DIFFERENCE:", f"${reported_gmna - total_revenue:,.0f}")
print("RATIO:", reported_gmna / total_revenue)