import numpy as np

# -----------------------------
# Parameters
# -----------------------------
arable_land_ha = 1.5e9           # global arable land
topsoil_depth_m = 1               # assume 1 meter
soil_density_kg_m3 = 1300

# Topsoil lost per ton of food (kg/ton) — carbon-based
topsoil_loss_per_ton_food_kg = 10# 5 kg soil carbon per ton of food

# Global food production over time (tons/year)
years = np.arange(1800, 2126)
food_production_tons = 0.2e9 * (1.02 ** (years - 1800))  # start 0.2B tons, 2% growth/year

# -----------------------------
# Initial total topsoil mass
# -----------------------------
total_topsoil_kg = arable_land_ha * 10000 * topsoil_depth_m * soil_density_kg_m3
topsoil_remaining = total_topsoil_kg

# -----------------------------
# Yearly simulation
# -----------------------------
print(f"{'Year':<6} {'Topsoil remaining (%)':>20}")
for year, production in zip(years, food_production_tons):
    annual_loss = production * 1e3 * topsoil_loss_per_ton_food_kg  # tons food to kg soil lost
    topsoil_remaining -= annual_loss
    if topsoil_remaining < 0:
        topsoil_remaining = 0
    remaining_percent = 100 * topsoil_remaining / total_topsoil_kg
    print(f"{year:<6} {remaining_percent:>20.6f}")
    if topsoil_remaining <= 0:
        break

print(f"\nTopsoil fully depleted by {year} if consumption continues at this rate.")