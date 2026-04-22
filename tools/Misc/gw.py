import numpy as np
import pandas as pd
from scipy.stats import linregress

# ---------------------------------------------------
# IMMUTABLE INPUT
# ---------------------------------------------------
segments = [
    ("Napoleonic aftermath expansion", 1812, 1815, +1),
    ("Crimean War defeat", 1853, 1856, -1),
    ("Russo-Japanese defeat", 1904, 1905, -1),
    ("WWI collapse", 1914, 1917, -1),
    ("Early Soviet reconsolidation", 1918, 1922, +1),
    ("WWII initial collapse", 1941, 1942, -1),
    ("WWII counter-advance", 1943, 1945, +1),
    ("Cold War expansion phase", 1946, 1975, +1),
    ("Late Soviet stagnation", 1976, 1991, -1),
    ("Post-Soviet contraction", 1991, 2007, -1),
    ("Post-2008 reassertion", 2008, 2024, +1),
]

df = pd.DataFrame(segments, columns=["event","start","end","state"])

# ---------------------------------------------------
# 1. Extract cycle boundaries (no modification)
# ---------------------------------------------------
switch_years = []
switch_states = []

for i in range(1, len(df)):
    if df.loc[i, "state"] != df.loc[i-1, "state"]:
        switch_years.append(df.loc[i, "start"])
        switch_states.append(df.loc[i, "state"])

switch_years = np.array(switch_years)
cycle_lengths = np.diff(switch_years)

# ---------------------------------------------------
# 2. Global trend in cycle time
# ---------------------------------------------------
x = np.arange(len(cycle_lengths))
global_slope, _, global_r, _, _ = linregress(x, cycle_lengths)

# ---------------------------------------------------
# 3. Outlier detection (BUT NOT REMOVAL)
# ---------------------------------------------------
median = np.median(cycle_lengths)
mad = np.median(np.abs(cycle_lengths - median))
z = 0.6745 * (cycle_lengths - median) / mad if mad != 0 else np.zeros_like(cycle_lengths)

is_outlier = np.abs(z) > 3.5

# ---------------------------------------------------
# 4. Split analysis: with vs without outliers
# ---------------------------------------------------
normal = cycle_lengths[~is_outlier]
outliers = cycle_lengths[is_outlier]

def stats(x):
    if len(x) < 2:
        return (np.nan, np.nan)
    return (np.mean(x), np.std(x))

normal_mean, normal_std = stats(normal)
out_mean, out_std = stats(outliers)

# ---------------------------------------------------
# 5. Correlation with "state strength regime"
# define strength proxy:
# +1 expansion, -1 contraction magnitude impact
# ---------------------------------------------------
state_strength = np.array(switch_states[:len(cycle_lengths)])

corr_strength = np.corrcoef(cycle_lengths, state_strength)[0,1]

# ---------------------------------------------------
# 6. Time-dependent correlation (rolling structure)
# ---------------------------------------------------
window = 3
rolling_corr = []

for i in range(len(cycle_lengths) - window + 1):
    xw = cycle_lengths[i:i+window]
    yw = state_strength[i:i+window]
    if np.std(xw) > 0 and np.std(yw) > 0:
        rolling_corr.append(np.corrcoef(xw, yw)[0,1])
    else:
        rolling_corr.append(np.nan)

rolling_corr = np.array(rolling_corr)

# ---------------------------------------------------
# 7. Harmonic proxy: FFT power concentration
# ---------------------------------------------------
fft = np.fft.fft(cycle_lengths)
power = np.abs(fft)**2
dominance = np.max(power[1:]) / np.sum(power[1:])

# ---------------------------------------------------
# OUTPUT
# ---------------------------------------------------
print("=== FULL REGIME CORRELATION MODEL ===\n")

print("Cycle lengths:", cycle_lengths)

print("\nGlobal trend slope:", global_slope)
print("Global correlation:", global_r)

print("\nOutlier handling (preserved, not removed):")
print("Normal mean/std:", normal_mean, normal_std)
print("Outlier mean/std:", out_mean, out_std)
print("Outlier mask:", is_outlier)

print("\nCorrelation with regime state strength:", corr_strength)

print("\nRolling correlation (cycle vs regime):", rolling_corr)

print("\nHarmonic concentration (FFT dominance):", dominance)