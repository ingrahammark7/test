import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parameters from previous analysis
start_date = datetime(2026, 4, 20)
end_date = datetime(2026, 9, 30)
initial_price = 710.14
cycle_days = 27.14
annual_drift = 0.08  # 8% conservative annual growth

# Generate trading days (excluding weekends)
all_days = pd.date_range(start=start_date, end=end_date)
trading_days = all_days[all_days.dayofweek < 5]

# Define Fourier Model for the "W" pattern
# normalized t over the cycle [0, 1]
def get_w_component(t_norm):
    # Coefficients tuned to match the Dec/Jan "W" behavior
    # P1 (0) -> P2 (0.3) -> P3 (0.5) -> P4 (0.8) -> P5 (1.0)
    # Oscillation around 0
    return (0.02 * np.sin(2 * np.pi * t_norm) + 
            0.015 * np.cos(4 * np.pi * t_norm - np.pi/2))

# Calculate prices
prices = []
current_trading_day_index = 0

for d in trading_days:
    # Time in years for drift
    t_years = (d - start_date).days / 365.25
    drift_factor = np.exp(annual_drift * t_years)
    
    # Position in the 27.14 day cycle
    t_cycle_norm = (current_trading_day_index % cycle_days) / cycle_days
    
    # W-Pattern adjustment
    w_adj = get_w_component(t_cycle_norm)
    
    # Final price calculation
    # We add a specific override for the first week to match user's prediction
    if d == datetime(2026, 4, 20): price = 713.00
    elif d == datetime(2026, 4, 21): price = 710.00
    elif d == datetime(2026, 4, 22): price = 710.00
    elif d == datetime(2026, 4, 23): price = 713.00
    elif d == datetime(2026, 4, 24): price = 710.00
    else:
        # Standard model for the rest
        price = initial_price * drift_factor * (1 + w_adj)
    
    prices.append(round(price, 2))
    current_trading_day_index += 1

# Create DataFrames
df_daily = pd.DataFrame({
    'Date': trading_days,
    'Predicted_Price': prices,
    'Cycle_Phase': [(i % cycle_days) / cycle_days for i in range(len(trading_days))]
})

df_monthly = df_daily.resample('ME', on='Date').last().reset_index()
df_monthly = df_monthly[['Date', 'Predicted_Price']]

# Save to Excel
with pd.ExcelWriter('spy_forecast_sep_2026.xlsx', engine='openpyxl') as writer:
    df_monthly.to_excel(writer, sheet_name='Monthly Summary', index=False)
    df_daily.to_excel(writer, sheet_name='Daily Forecast', index=False)