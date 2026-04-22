import numpy as np
import pandas as pd
from scipy.stats import linregress

# ---------------------------------------------------
# Phase segments (simplified but consistent structure)
# state: +1 expansion, -1 contraction
# ---------------------------------------------------
segments = [
    (1812, 1815, +1),
    (1853, 1856, -1),
    (1904, 1905, -1),
    (1914, 1917, -1),
    (1918, 1922, +1),
    (1941, 1942, -1),
    (1943, 1945, +1),
    (1946, 1975, +1),
    (1976, 1991, -1),
    (1991, 2007, -1),
    (2008, 2024, +1),
]

df = pd.DataFrame(segments, columns=["start","end","state"])
df = df.sort_values("start").reset_index(drop=True)

# ---------------------------------------------------
# 1. Extract transition points
# ---------------------------------------------------
switches = []
for i in range(1, len(df)):
    if df.loc[i, "state"] != df.loc[i-1, "state"]:
        switches.append(df.loc[i, "start"])

# ---------------------------------------------------
# 2. Compute cycle lengths
# ---------------------------------------------------
cycle_lengths = np.diff(switches)

# ---------------------------------------------------
# 3. Trend in cycle duration
# ---------------------------------------------------
x = np.arange(len(cycle_lengths))

if len(cycle_lengths) > 1:
    slope, intercept, r, p, se = linregress(x, cycle_lengths)
else:
    slope = r = np.nan

# ---------------------------------------------------
# 4. Rolling local trend (detect acceleration vs slowdown)
# ---------------------------------------------------
window = 3
rolling_slopes = []

for i in range(len(cycle_lengths) - window + 1):
    y = cycle_lengths[i:i+window]
    xw = np.arange(window)
    s, _, _, _, _ = linregress(xw, y)
    rolling_slopes.append(s)

rolling_slopes = np.array(rolling_slopes)

# ---------------------------------------------------
# 5. Autocorrelation of cycle lengths
# ---------------------------------------------------
def autocorr(x):
    x = np.array(x)
    xm = x.mean()
    return np.sum((x[:-1]-xm)*(x[1:]-xm)) / np.sum((x-xm)**2)

ac = autocorr(cycle_lengths) if len(cycle_lengths) > 1 else np.nan

# ---------------------------------------------------
# Output
# ---------------------------------------------------
print("=== Cycle Time Dynamics ===")

print(f"Cycle lengths: {cycle_lengths}")
print(f"Average cycle length: {np.mean(cycle_lengths):.2f} years")

print("\nGlobal trend:")
print(f"slope: {slope:.3f} years per cycle")
print(f"correlation: {r:.3f}")

print("\nAutocorrelation of cycle lengths:")
print(ac)

print("\nRolling local trends (acceleration / slowdown):")
print(rolling_slopes)