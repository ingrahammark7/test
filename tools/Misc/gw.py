import numpy as np
import pandas as pd

# Parameters
starting_inventory = 600e6  # bushels at Jan 2025
acres_planted = 34.1e6
average_yield = 50  # bushels per acre
good_condition_pct = 0.54
annual_demand = 1_150e6
monthly_demand = annual_demand / 12
loss_factors = [0.1, 0.2, 0.3]  # yield loss scenarios
storage_loss_pct = 0.005  # 0.5% monthly storage loss (example)

# Months from Jan 2025 to Dec 2026
months = pd.date_range(start='2025-01-01', end='2026-12-31', freq='MS')

# Distribute production across harvest months (Jun, Jul, Aug)
harvest_months = [6, 7, 8]
production_total = acres_planted * average_yield * good_condition_pct

# Production split fraction for harvest months
production_per_month_fraction = 1 / len(harvest_months)

# Function to run monthly inventory model for a given loss factor
def run_monthly_model(loss_factor):
    production_after_loss = production_total * (1 - loss_factor)
    monthly_production = {month: 0 for month in months}
    
    for month in months:
        if month.month in harvest_months:
            monthly_production[month] = production_after_loss * production_per_month_fraction
    
    inventory = starting_inventory
    records = []
    
    for month in months:
        inventory += monthly_production[month]      # Add production if any
        inventory -= monthly_demand                  # Subtract monthly demand
        inventory -= inventory * storage_loss_pct   # Subtract storage loss
        inventory = max(inventory, 0)                # Prevent negative inventory
        
        records.append({'Month': month.strftime('%Y-%m'),
                        'Inventory (Million Bushels)': inventory / 1e6,
                        'Production (Million Bushels)': monthly_production[month] / 1e6,
                        'Demand (Million Bushels)': monthly_demand / 1e6})
    
    return pd.DataFrame(records)

# Run model and print results for each loss factor
for lf in loss_factors:
    print(f"\n--- Inventory Projection with {int(lf*100)}% Yield Loss ---")
    df = run_monthly_model(lf)
    print(df.to_string(index=False))