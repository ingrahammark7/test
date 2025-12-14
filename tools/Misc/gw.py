# real_ev_lithium_forecast_fixed.py
# Estimates lithium production vs EV lithium consumption using real‑world forecasts.

START_YEAR = 2024
END_YEAR = 2030

# Global lithium production in 2024 (t LCE)
lithium_prod_2024 = 240_000.0

# Annual lithium production growth
LITHIUM_GROWTH_RATE = 0.10  # 10% per year

# EV sales baseline (22M in 2025)
ev_sales_2025 = 22_000_000
EV_GROWTH_RATE = 0.15  # 15% YoY

# Lithium consumption per EV (kg Li)
LI_PER_EV_KG = 8.0

print("Year | Li Prod (t) | EVs Sold (units) | Li Consumed (t) | Gap (%)")
print("---------------------------------------------------------------")

# Initialize values
lithium_prod = lithium_prod_2024
ev_sales = ev_sales_2025 / (1.0 + EV_GROWTH_RATE)  # back-calculate 2024 sales

for year in range(START_YEAR, END_YEAR + 1):
    # Lithium consumed by EVs in t
    lithium_consumed = (ev_sales * LI_PER_EV_KG) / 1000.0

    # Gap: % of production remaining after EV consumption
    gap_percent = ((lithium_prod - lithium_consumed) / lithium_prod) * 100.0

    print(f"{year:4d} | {lithium_prod:11.0f} | {ev_sales:15.0f} | "
          f"{lithium_consumed:12.0f} | {gap_percent:8.1f}%")

    # Update for next year
    lithium_prod *= (1.0 + LITHIUM_GROWTH_RATE)
    ev_sales *= (1.0 + EV_GROWTH_RATE)