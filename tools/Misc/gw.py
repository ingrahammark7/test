import numpy as np
import pandas as pd
from scipy.stats import linregress

# ---------------------------------------------------
# Phase-based encoding (not single-year binary)
# value = geopolitical momentum
# +1 = expansion/advance
# -1 = retreat/collapse
# ---------------------------------------------------
segments = [
    ("Napoleonic aftermath expansion", 1812, 1815, +1),

    ("Crimean War defeat", 1853, 1856, -1),

    ("Russo-Japanese defeat", 1904, 1905, -1),

    ("WWI collapse", 1914, 1917, -1),

    ("Early Soviet reconsolidation", 1918, 1922, +1),

    ("Interwar instability", 1923, 1939, 0),

    ("WWII initial collapse", 1941, 1942, -1),

    ("WWII counter-advance", 1943, 1945, +1),

    ("Cold War expansion phase", 1946, 1975, +1),

    ("Late Soviet stagnation", 1976, 1991, -1),

    ("Post-Soviet contraction", 1991, 2007, -1),

    ("Post-2008 reassertion", 2008, 2024, +1),
]

df = pd.DataFrame(segments, columns=["event", "start", "end", "state"])

# ---------------------------------------------------
# 1. Duration-weighted cycle extraction
# ---------------------------------------------------
df["duration"] = df["end"] - df["start"]

# collapse neutral phases if desired
df_nonzero = df[df["state"] != 0].copy()

# detect sign changes = "cycles"
cycle_lengths = []
cycle_years = []

for i in range(1, len(df_nonzero)):
    if df_nonzero.iloc[i]["state"] != df_nonzero.iloc[i-1]["state"]:
        start = df_nonzero.iloc[i-1]["end"]
        end = df_nonzero.iloc[i]["start"]
        cycle_lengths.append(end - start)
        cycle_years.append(start)

cycle_lengths = np.array(cycle_lengths)

# ---------------------------------------------------
# 2. Autocorrelation on interpolated yearly series
# ---------------------------------------------------
years = np.arange(df["start"].min(), df["end"].max()+1)
series = np.zeros_like(years, dtype=float)

for _, r in df.iterrows():
    series[(years >= r["start"]) & (years < r["end"])] = r["state"]

def autocorr(x, lag=1):
    x = np.array(x)
    xm = x.mean()
    return np.sum((x[:-lag]-xm)*(x[lag:]-xm)) / np.sum((x-xm)**2)

lag1 = autocorr(series)

# ---------------------------------------------------
# 3. Trend in cycle duration
# ---------------------------------------------------
if len(cycle_lengths) > 1:
    slope, intercept, r, p, se = linregress(
        np.arange(len(cycle_lengths)),
        cycle_lengths
    )
else:
    slope = r = np.nan

# ---------------------------------------------------
# 4. Results
# ---------------------------------------------------
print("=== Phase-based Geopolitical Model ===")

print(f"Lag-1 autocorrelation: {lag1:.3f}")

print(f"\nCycle lengths (years between reversals): {cycle_lengths}")
print(f"Average cycle length: {np.mean(cycle_lengths):.2f}")

print("\nCycle trend:")
print(f"slope: {slope:.3f} years per cycle")
print(f"correlation: {r:.3f}")