import matplotlib.pyplot as plt
import numpy as np

years = 75  # 2025–2100
years_range = np.arange(2025, 2025 + years)

# Steel & bio-material construction parameters
initial_steel_stock = 11000  # Mt
annual_depreciation_rate = 0.015  # 1.5%
recycling_efficiency = 0.85
construction_steel_demand = 90  # Mt/year
min_steel_threshold = 1000  # Mt

initial_bio_production = 10  # Mt/year bio materials now
bio_growth_rate = 0.03       # 3% annual growth

# Concrete market shares parameters
concrete_traditional_share = np.zeros(years)
concrete_bio_share = np.zeros(years)

concrete_traditional_share[0] = 0.98
concrete_bio_share[0] = 0.02

concrete_bio_growth_rate = 0.15  # 15% CAGR
concrete_traditional_decline_rate = -0.015  # -1.5% CAGR

# Initialize arrays
steel_stock = np.zeros(years)
steel_available_for_construction = np.zeros(years)
construction_steel_activity = np.zeros(years)
bio_construction_production = np.zeros(years)
total_construction = np.zeros(years)

steel_stock[0] = initial_steel_stock
bio_construction_production[0] = initial_bio_production

for t in range(1, years):
    # Steel stock update
    steel_lost = steel_stock[t-1] * annual_depreciation_rate
    recycled_steel = steel_lost * recycling_efficiency
    steel_stock[t] = steel_stock[t-1] - steel_lost + recycled_steel
    
    steel_available_for_construction[t] = max(0, steel_stock[t] - min_steel_threshold)
    construction_steel_activity[t] = min(construction_steel_demand, steel_available_for_construction[t])
    steel_stock[t] -= construction_steel_activity[t]
    
    # Bio materials grow modestly
    bio_construction_production[t] = bio_construction_production[t-1] * (1 + bio_growth_rate)
    total_construction[t] = construction_steel_activity[t] + bio_construction_production[t]
    
    # Concrete shares update
    concrete_bio_share[t] = concrete_bio_share[t-1] * (1 + concrete_bio_growth_rate)
    concrete_traditional_share[t] = concrete_traditional_share[t-1] * (1 + concrete_traditional_decline_rate)
    # Normalize
    total_share = concrete_bio_share[t] + concrete_traditional_share[t]
    concrete_bio_share[t] /= total_share
    concrete_traditional_share[t] /= total_share

# Plot combined results
fig, axs = plt.subplots(2, 1, figsize=(12, 10))

# Construction volumes
axs[0].plot(years_range, steel_stock, label='Steel Stock (Mt)')
axs[0].plot(years_range, construction_steel_activity, label='Steel-based Construction (Mt/year)')
axs[0].plot(years_range, bio_construction_production, label='Bio-based Construction (Mt/year)')
axs[0].plot(years_range, total_construction, label='Total Construction (Mt/year)', linestyle='--')
axs[0].axhline(min_steel_threshold, color='red', linestyle='--', label='Min Steel Threshold')
axs[0].set_title('U.S. Construction Materials 2025–2100')
axs[0].set_xlabel('Year')
axs[0].set_ylabel('Million Metric Tons (Mt)')
axs[0].legend()
axs[0].grid(True)

# Concrete market shares
axs[1].plot(years_range, concrete_traditional_share * 100, label='Traditional Concrete')
axs[1].plot(years_range, concrete_bio_share * 100, label='Bio / Low-Carbon Concrete')
axs[1].set_title('Projected Concrete Market Share 2025–2100')
axs[1].set_xlabel('Year')
axs[1].set_ylabel('Market Share (%)')
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.show()