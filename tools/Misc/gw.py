import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# === Updated Simulation Parameters ===

# Start from current date: July 31, 2025
start_date = datetime(2025, 7, 31)
simulation_days = 365
end_date = start_date + timedelta(days=simulation_days - 1)

# Corn data (same assumptions)
initial_corn_inventory = 2e9  # bushels carryover on July 31 (assumed)
annual_corn_production = 15e9  # bushels/year
harvest_start = datetime(2025, 10, 1)
harvest_end = datetime(2025, 11, 15)
harvest_days = (harvest_end - harvest_start).days + 1
daily_harvest = annual_corn_production / harvest_days

# Ethanol data
ethanol_per_bushel = 2.8
initial_ethanol_inventory = 1.2e9  # gallons on July 31 (assumed)
annual_corn_for_ethanol = 5e9
daily_corn_for_ethanol = annual_corn_for_ethanol / 365
annual_ethanol_prod = annual_corn_for_ethanol * ethanol_per_bushel
daily_ethanol_consumption = annual_ethanol_prod / 365

# Crop loss event: let's say it just happened or will happen soon
crop_loss_date = datetime(2025, 8, 15)  # example: two weeks from start date
crop_loss_percent = 100 # 70% crop loss

# === Initialize arrays ===

dates = [start_date + timedelta(days=i) for i in range(simulation_days)]
corn_inventory = np.zeros(simulation_days)
ethanol_inventory = np.zeros(simulation_days)
corn_supply_for_ethanol = np.zeros(simulation_days)

corn_inventory[0] = initial_corn_inventory
ethanol_inventory[0] = initial_ethanol_inventory

crop_loss_occurred = False
harvested_corn_total = 0

for i in range(1, simulation_days):
    today = dates[i]

    # Harvest period - add daily harvest to inventory, adjusted if crop loss occurred
    if harvest_start <= today <= harvest_end:
        daily_harvest_adjusted = daily_harvest
        if crop_loss_occurred:
            daily_harvest_adjusted *= (1 - crop_loss_percent / 100)
        corn_inventory[i] = corn_inventory[i-1] + daily_harvest_adjusted
        harvested_corn_total += daily_harvest_adjusted
    else:
        corn_inventory[i] = corn_inventory[i-1]

    # Trigger crop loss event
    if (not crop_loss_occurred) and (today >= crop_loss_date):
        crop_loss_occurred = True

    # Corn available for ethanol production
    corn_available = min(corn_inventory[i], daily_corn_for_ethanol)
    corn_supply_for_ethanol[i] = corn_available
    corn_inventory[i] -= corn_available

    # Ethanol produced
    ethanol_produced = corn_available * ethanol_per_bushel

    # Update ethanol inventory
    ethanol_inventory[i] = ethanol_inventory[i-1] + ethanol_produced - daily_ethanol_consumption
    if ethanol_inventory[i] < 0:
        ethanol_inventory[i] = 0

# Detect when ethanol inventory falls below threshold
threshold = 1e7  # 10 million gallons
zero_day_index = next((i for i, inv in enumerate(ethanol_inventory) if inv <= threshold), None)

if zero_day_index is not None:
    zero_date = dates[zero_day_index]
    print(f"Ethanol inventory falls below {threshold} gallons on {zero_date.strftime('%Y-%m-%d')}")
else:
    print("Ethanol inventory stays above threshold during simulation.")

# === Plot results ===
plt.figure(figsize=(14,8))

plt.subplot(2,1,1)
plt.plot(dates, corn_inventory/1e9, label='Corn Inventory (billion bushels)')
plt.axvline(crop_loss_date, color='red', linestyle='--', label='Crop Loss Event')
plt.title('Corn Inventory Starting July 31, 2025')
plt.ylabel('Inventory (billion bushels)')
plt.legend()
plt.grid(True)

plt.subplot(2,1,2)
plt.plot(dates, ethanol_inventory/1e9, label='Ethanol Inventory (billion gallons)', color='orange')
plt.axvline(crop_loss_date, color='red', linestyle='--', label='Crop Loss Event')
plt.title('Ethanol Inventory Starting July 31, 2025')
plt.ylabel('Inventory (billion gallons)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()