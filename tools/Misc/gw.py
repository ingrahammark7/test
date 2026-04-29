import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Synthetic but realistic node samples
# (nm-scale feature approximations)
# -----------------------------
nodes = [
    {"name": "22nm planar", "contact_nm": 60, "via_nm": 70},
    {"name": "14nm FinFET", "contact_nm": 50, "via_nm": 55},
    {"name": "7nm EUV", "contact_nm": 40, "via_nm": 40},
    {"name": "5nm EUV", "contact_nm": 32, "via_nm": 35},
    {"name": "3nm GAAFET", "contact_nm": 28, "via_nm": 32},
    {"name": "2nm class", "contact_nm": 25, "via_nm": 30},
]

# -----------------------------
# Compute dimensionless ratio
# chi = Ac / Av
# using area ~ (feature size)^2
# -----------------------------
data = []

for n in nodes:
    Ac = n["contact_nm"] ** 2
    Av = n["via_nm"] ** 2
    chi = Ac / Av

    # regime classification
    if chi > 1.2:
        regime = "BEOL-limited"
    elif chi < 0.8:
        regime = "FEOL-limited"
    else:
        regime = "Balanced"

    data.append([n["name"], Ac, Av, chi, regime])

df = pd.DataFrame(data, columns=["Node", "Contact Area", "Via Area", "chi", "Regime"])

print("\nChip Scaling Coupling Model\n")
print(df)

# -----------------------------
# Visualization
# -----------------------------
plt.figure(figsize=(8,5))
plt.plot(df["Node"], df["chi"], marker="o")
plt.axhline(1.0, linestyle="--", label="Critical coupling (χ = 1)")

plt.xticks(rotation=45)
plt.ylabel("χ = Contact Area / Via Area")
plt.title("FEOL–BEOL Coupling Ratio Across Process Nodes")
plt.legend()
plt.tight_layout()
plt.show()