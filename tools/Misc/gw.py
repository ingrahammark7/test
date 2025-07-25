import pandas as pd

# Wastewater data (full data as given)
wastewater_data = [
    {"month": "2020-01", "index": 5.2},
    {"month": "2020-02", "index": 4.9},
    {"month": "2020-03", "index": 12.5},
    {"month": "2020-04", "index": 28.3},
    {"month": "2020-05", "index": 35.1},
    {"month": "2020-06", "index": 42.7},
    {"month": "2020-07", "index": 58.4},
    {"month": "2020-08", "index": 61.2},
    {"month": "2020-09", "index": 48.7},
    {"month": "2020-10", "index": 52.9},
    {"month": "2020-11", "index": 73.5},
    {"month": "2020-12", "index": 89.1},
    {"month": "2021-01", "index": 95.8},
    {"month": "2021-02", "index": 84.3},
    {"month": "2021-03", "index": 70.1},
    {"month": "2021-04", "index": 56.6},
    {"month": "2021-05", "index": 42.9},
    {"month": "2021-06", "index": 37.5},
    {"month": "2021-07", "index": 50.2},
    {"month": "2021-08", "index": 63.8},
    {"month": "2021-09", "index": 71.4},
    {"month": "2021-10", "index": 65.9},
    {"month": "2021-11", "index": 78.6},
    {"month": "2021-12", "index": 92.3},
    {"month": "2022-01", "index": 99.4},
    {"month": "2022-02", "index": 87.6},
    {"month": "2022-03", "index": 72.0},
    {"month": "2022-04", "index": 58.7},
    {"month": "2022-05", "index": 46.5},
    {"month": "2022-06", "index": 51.2},
    {"month": "2022-07", "index": 60.1},
    {"month": "2022-08", "index": 67.3},
    {"month": "2022-09", "index": 74.5},
    {"month": "2022-10", "index": 80.2},
    {"month": "2022-11", "index": 85.7},
    {"month": "2022-12", "index": 89.6},
    {"month": "2023-01", "index": 78.2},
    {"month": "2023-02", "index": 85.3},
    {"month": "2023-03", "index": 90.1},
    {"month": "2023-04", "index": 76.8},
    {"month": "2023-05", "index": 64.5},
    {"month": "2023-06", "index": 58.2},
    {"month": "2023-07", "index": 62.7},
    {"month": "2023-08", "index": 71.1},
    {"month": "2023-09", "index": 80.4},
    {"month": "2023-10", "index": 85.9},
    {"month": "2023-11", "index": 91.0},
    {"month": "2023-12", "index": 87.6},
    {"month": "2024-01", "index": 73.8},
    {"month": "2024-02", "index": 68.5},
    {"month": "2024-03", "index": 61.4},
    {"month": "2024-04", "index": 57.0},
    {"month": "2024-05", "index": 63.2},
    {"month": "2024-06", "index": 69.7},
    {"month": "2024-07", "index": 77.1},
    {"month": "2024-08", "index": 80.9},
    {"month": "2024-09", "index": 84.4},
    {"month": "2024-10", "index": 89.2},
    {"month": "2024-11", "index": 94.6},
    {"month": "2024-12", "index": 98.3},
    {"month": "2025-01", "index": 88.1},
    {"month": "2025-02", "index": 81.3},
    {"month": "2025-03", "index": 77.4},
    {"month": "2025-04", "index": 74.0},
    {"month": "2025-05", "index": 68.8},
    {"month": "2025-06", "index": 72.1},
    {"month": "2025-07", "index": 79.5}
]

# Load into DataFrame
df_wastewater = pd.DataFrame(wastewater_data)

# Convert month to datetime
df_wastewater["month"] = pd.to_datetime(df_wastewater["month"])

# Define extrapolation end date
end_date = pd.to_datetime("2026-12-01")

# Create full month range from earliest month to end_date
full_months = pd.date_range(start=df_wastewater["month"].min(), end=end_date, freq="MS")

# Extract 2024 months as template for extrapolation
template_2024 = df_wastewater[df_wastewater["month"].dt.year == 2024].set_index(df_wastewater[df_wastewater["month"].dt.year == 2024]["month"].dt.month)["index"]

# Build extended data including extrapolated months
extended_rows = []
for month in full_months:
    if month in df_wastewater["month"].values:
        index_val = df_wastewater.loc[df_wastewater["month"] == month, "index"].values[0]
    else:
        index_val = template_2024.loc[month.month]
    extended_rows.append({"month": month, "index": index_val})

df_extended = pd.DataFrame(extended_rows)

# Calculate estimated cases (1 index = 26000 cases)
df_extended["estimated_cases"] = df_extended["index"] * 26000

# Fixed number of households
households = 131_000_000

# Calculate cumulative estimated cases
df_extended["cumulative_cases"] = df_extended["estimated_cases"].cumsum()

# Calculate cumulative cases ratio (cumulative_cases / households)
df_extended["cumulative_ratio"] = df_extended["cumulative_cases"] / households

# Calculate unaffected fraction as 1 / (1 + cumulative_ratio)
df_extended["unaffected_fraction"] = 1 / (1 + df_extended["cumulative_ratio"])

# Calculate number of unaffected households
df_extended["unaffected_households"] = df_extended["unaffected_fraction"] * households

# Show last 12 months with all calculated columns
print(df_extended[[
    "month", "index", "estimated_cases", "cumulative_cases", "cumulative_ratio", 
    "unaffected_fraction", "unaffected_households"
]].tail(12))