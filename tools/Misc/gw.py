import numpy as np
import matplotlib.pyplot as plt

# Parameters
months = np.arange(1, 25)  # Model for 2 years, month by month
initial_inventory = 570  # Arbitrary starting inventory (e.g., million bushels)
monthly_consumption = 100  # Average monthly consumption/drawdown
harvest_month = 5  # Month of harvest (September)
harvest_addition = 1000  # Inventory added by harvest

# Varying loss scenarios as percentage reductions in harvest_addition
loss_scenarios = {
    "No Loss": 0,
    "10% Loss": 0.10,
    "20% Loss": 0.20,
    "30% Loss": 0.30,
    "40% Loss": 0.40,
}

plt.figure(figsize=(10, 6))

for label, loss in loss_scenarios.items():
    inventory = np.zeros_like(months, dtype=float)
    inventory[0] = initial_inventory
    for i in range(1, len(months)):
        # Add harvest inventory once a year in harvest month
        if (i % 12) == harvest_month:
            added_inventory = harvest_addition * (1 - loss)
        else:
            added_inventory = 0
        
        # Inventory from previous month minus consumption plus harvest addition if any
        inventory[i] = max(inventory[i-1] - monthly_consumption + added_inventory, 0)
    
    plt.plot(months, inventory, label=label)

plt.title("Modeled Grain Inventory Over 2 Years with Varying Harvest Loss")
plt.xlabel("Month")
plt.ylabel("Inventory (million bushels, arbitrary units)")
plt.xticks(ticks=np.arange(0, 24, 3), labels=[
    "Jan Y1", "Apr Y1", "Jul Y1", "Oct Y1", "Jan Y2", "Apr Y2", "Jul Y2", "Oct Y2"
])
plt.legend()
plt.grid(True)
plt.show() 