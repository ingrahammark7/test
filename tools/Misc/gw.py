import pandas as pd
import numpy as np


# --- Wastewater data ---
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
df = pd.DataFrame(wastewater_data)
df['month'] = pd.to_datetime(df['month'])

# Constants for margin calculation
cases_per_index = 195215
households = 132_216_000
gross_margin = 0.154
baseline_loss = 0.073
difficulty_rate = 0.085*0.23*1.12*1.2
#long civid times diff rate times 65 plus card balance times 65 plus share
loss_per_case = 1.0

# Calculate estimated cases and cumulative ratio
df['estimated_cases'] = df['index'] * cases_per_index
df['cumulative_cases'] = df['estimated_cases'].cumsum()
df['cumulative_ratio'] = df['cumulative_cases'] / households

# Calculate loss provision and net margin
df['loss_provision'] = baseline_loss + loss_per_case * df['cumulative_ratio'] * difficulty_rate
df['net_margin'] = gross_margin - df['loss_provision']

# --- Reset and extrapolate to zero after 2023-12 ---

reset_date = pd.Timestamp('2023-09-01')
reset_idx = df.index[df['month'] == reset_date][0]

# Reset baseline margin (e.g. original margin minus baseline loss)
M0 = gross_margin - baseline_loss

# Calculate pre-reset slope (monthly change in net margin)
start_margin = df.loc[0, 'net_margin']
months_before_reset = reset_idx
slope = (df.loc[reset_idx, 'net_margin'] - start_margin) / months_before_reset

# Calculate months to zero margin from reset baseline at the same decline rate
months_to_zero = int(np.ceil(M0 / abs(slope)))

# Create post-reset months timeline
post_reset_months = pd.date_range(start=reset_date + pd.offsets.MonthBegin(1), periods=months_to_zero, freq='MS')

# Linear decline from M0 to 0 over months_to_zero months
post_reset_margins = np.linspace(M0, 0, months_to_zero)

# Build DataFrame for post-reset extrapolation
df_post_reset = pd.DataFrame({
    'month': post_reset_months,
    'net_margin': post_reset_margins
})

# Combine pre-reset data and post-reset extrapolation
df_final = pd.concat([df.loc[:reset_idx, ['month', 'net_margin']], df_post_reset], ignore_index=True)



print(f"Net margin reaches zero approximately in {df_final}")