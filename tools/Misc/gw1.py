# Fine-structure constant sensitivity analysis for biological processes
# Author: ChatGPT
# Purpose: Estimate how different biological energy scales (H-bonds, covalent bonds, ATP, etc.)
# shift if the fine-structure constant α changes.

import math
import pandas as pd

# constants
alpha0 = 1/137.035999084  # CODATA reference value for α
kT_300K = 0.02585  # eV, thermal energy at 300 K

# Baseline biological energy values (approximate, eV)
items = [
    {"name": "Hydrogen bond (DNA & proteins)", "E0": 0.20, "low_ratio_kT": 5, "high_ratio_kT": 200},
    {"name": "Base stacking (DNA)", "E0": 0.50, "low_ratio_kT": 10, "high_ratio_kT": 300},
    {"name": "Covalent bond (C–C / C–N)", "E0": 3.50, "low_ratio_kT": 40, "high_ratio_kT": 2000},
    {"name": "ATP hydrolysis (usable energy)", "E0": 0.50, "low_abs": 0.25, "high_abs": 1.00},
    {"name": "Photosynthetic transition (chlorophyll)", "E0": 2.00, "low_abs": 0.50, "high_abs": 3.50},
    {"name": "Water H-bond (solvent)", "E0": 0.20, "low_abs": 0.08, "high_abs": 0.35},
]

rows = []

for it in items:
    name = it["name"]
    E0 = it["E0"]

    # Decide whether to use ratio-to-kT or absolute energy bounds
    if "low_ratio_kT" in it:
        low = it["low_ratio_kT"] * kT_300K
        high = it["high_ratio_kT"] * kT_300K
    else:
        low = it["low_abs"]
        high = it["high_abs"]

    # Energy scaling rule: E ~ E0 * (α/α0)^2
    s_low = low / E0
    s_high = high / E0

    # Ensure order
    s_min, s_max = min(s_low, s_high), max(s_low, s_high)

    # Convert to α ranges
    alpha_ratio_min = math.sqrt(s_min) if s_min > 0 else 0.0
    alpha_ratio_max = math.sqrt(s_max)
    alpha_min = alpha0 * alpha_ratio_min
    alpha_max = alpha0 * alpha_ratio_max

    rows.append({
        "Process": name,
        "E0 (eV)": round(E0, 3),
        "Allowed E range (eV)": f"{round(low,3)} – {round(high,3)}",
        "Allowed (α/α0)": f"{round(alpha_ratio_min,4)} – {round(alpha_ratio_max,4)}",
        "Allowed α range": f"{alpha_min:.6e} – {alpha_max:.6e}",
    })

# Build DataFrame
df = pd.DataFrame(rows)

# Show table
print("\n=== Alpha Sensitivity Ranges (Coarse Estimates) ===\n")
print(df.to_string(index=False))

# Optionally, save to CSV
df.to_csv("alpha_ranges.csv", index=False)
print("\nSaved results to alpha_ranges.csv")