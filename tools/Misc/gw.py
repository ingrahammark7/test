# Creating a day-by-day probabilistic forecast for the government shutdown ending (Oct 16–Oct 30, 2025).
# This is a heuristic model (not a formal statistical fit). It weights current facts:
#  - repeated Senate vote failures and current offers (low near-term probability today)
#  - Thune offer to provide a vote on ACA subsidies (increases chances next week)
#  - political/economic pressure rising week-to-week (increases hazard over time)
# The numbers are my best-effort judgmental probabilities based on current reporting.
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
dates = [datetime(2025,10,16) + timedelta(days=i) for i in range(15)]  # Oct16 - Oct30
# Daily resolution probabilities (probability the shutdown is resolved on that specific date)
# These are modelled to reflect a low chance today (vote failures), a higher chance next week as pressure mounts,
# and a strong chance cumulatively by Oct 30.
daily_probs = [
    0.05,  # Oct 16
    0.08,  # Oct 17
    0.10,  # Oct 18
    0.12,  # Oct 19
    0.12,  # Oct 20
    0.13,  # Oct 21
    0.10,  # Oct 22
    0.08,  # Oct 23
    0.07,  # Oct 24
    0.06,  # Oct 25
    0.04,  # Oct 26
    0.03,  # Oct 27
    0.01,  # Oct 28
    0.00,  # Oct 29 (negligible new resolution chance beyond Oct28 in this curve)
    0.00,  # Oct 30 (we'll interpret cumulative by Oct30)
]
# Normalize to ensure sum <= 1 (it currently sums to something <1). We'll leave remaining mass as "not resolved by Oct 30".
s = sum(daily_probs)
# compute cumulative
df = pd.DataFrame({
    "date": [d.strftime("%Y-%m-%d") for d in dates],
    "daily_resolution_prob": daily_probs
})
df["cumulative_prob_by_date"] = df["daily_resolution_prob"].cumsum()
df["cumulative_percent_by_date"] = (df["cumulative_prob_by_date"]*100).round(1)
# show table and plot cumulative probability
from caas_jupyter_tools import display_dataframe_to_user
display_dataframe_to_user("Shutdown resolution probabilities (Oct 16-30, 2025)", df)

plt.figure(figsize=(9,4))
plt.plot(df["date"], df["cumulative_prob_by_date"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Cumulative probability (0–1)")
plt.title("Heuristic forecast: probability shutdown resolved by each date (Oct 16–30, 2025)")
plt.tight_layout()
plt.show()

# Save CSV for download if the user wants it
df.to_csv("/mnt/data/shutdown_forecast_oct16-30-2025.csv", index=False)
print("\n[Download the CSV here](/mnt/data/shutdown_forecast_oct16-30-2025.csv)")