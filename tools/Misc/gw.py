# real_ev_lithium_forecast.py
# Estimates lithium production vs EV lithium consumption using real‑world forecasts.

# Constants / real estimates
START_YEAR = 2024
END_YEAR = 2030

# Global lithium production in 2024 (LCE tonnes)
# Industry estimate scaled from reported data.
lithium_prod_2024 = 240_000.0

# Annual production growth (assumption)
LITHIUM_GROWTH_RATE = 0.10  # 10% per year

# EV sales baseline
# BloombergNEF expects ~22M EV+PHEV sales in 2025
ev_sales_2025 = 22_000_000

# Annual EV sales growth assumption
EV_GROWTH_RATE = 0.15  # 15% YoY

# Lithium consumption per EV (kg of Li metal)
LI_PER_EV_KG = 8.0

print("Year | Li Prod (t) | EVs Sold (units) | Li Consumed (t) | Gap (t)")
print("---------------------------------------------------------------")

# Initialize
lithium_prod = lithium_prod_2024
ev_sales = ev_sales_2025 / (1.0 + EV_GROWTH_RATE)  # back‑calculate for 2024

for year in range(START_YEAR, END_YEAR + 1):
    # Lithium consumed by EVs (kg → t)
    lithium_consumed = (ev_sales * LI_PER_EV_KG) / 1000.0
    gap = lithium_prod - lithium_consumed

    print(f"{year:4d} | {lithium_prod:11.0f} | {ev_sales:15.0f} | "
          f"{lithium_consumed:12.0f} | {gap:8.0f}")

    # Next year
    lithium_prod *= (1.0 + LITHIUM_GROWTH_RATE)
    ev_sales *= (1.0 + EV_GROWTH_RATE)