import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# GAS PROPERTIES
# ----------------------------
gases = {
    "He": {"k": 0.151, "lambda_1atm": 180e-9, "color": "blue"},
    "H2": {"k": 0.180, "lambda_1atm": 110e-9, "color": "green"},
    "Ne": {"k": 0.049, "lambda_1atm": 65e-9,  "color": "orange"},
    "N2": {"k": 0.025, "lambda_1atm": 65e-9,  "color": "purple"},
    "Ar": {"k": 0.018, "lambda_1atm": 70e-9,  "color": "red"},
}

# ----------------------------
# PHYSICS
# ----------------------------
q_load = 5e4
DeltaT = 20
G_req = q_load / DeltaT
b = 2.0

# ----------------------------
# SYSTEM BOUNDS (EXPLICIT)
# ----------------------------
P_min, P_max = 0.05, 5.0      # atm
d_min, d_max = 0.2e-6, 50e-6  # m

# Knudsen acceptable range
Kn_min, Kn_max = 1e-3, 10

# ----------------------------
# GRID
# ----------------------------
P = np.logspace(np.log10(P_min), np.log10(P_max), 500)
d = np.logspace(np.log10(d_min), np.log10(d_max), 500)

P_grid, d_grid = np.meshgrid(P, d)

plt.figure(figsize=(12,8))

# ----------------------------
# DRAW GAS FEASIBILITY BOUNDARIES
# ----------------------------
for name, g in gases.items():

    k = g["k"]
    lam0 = g["lambda_1atm"]

    lam = lam0 / P_grid
    Kn = lam / d_grid

    G = k / (d_grid + b * lam)

    feasible = (G >= G_req) & (Kn >= Kn_min) & (Kn <= Kn_max)

    # thermal boundary (G = G_req)
    d_boundary = k / G_req - b * lam0 / P
    valid = d_boundary > 0

    plt.plot(
        P[valid],
        d_boundary[valid] * 1e6,
        color=g["color"],
        linewidth=2,
        label=f"{name} thermal boundary"
    )

# ----------------------------
# DRAW ACCEPTABLE REGIONS (GLOBAL CONSTRAINTS)
# ----------------------------

# Pressure bounds
plt.axvline(P_min, color="black", linestyle="--")
plt.axvline(P_max, color="black", linestyle="--")
plt.text(P_min, 30, "P min", rotation=90)
plt.text(P_max, 30, "P max", rotation=90)

# Gap bounds
plt.axhline(d_min*1e6, color="black", linestyle="--")
plt.axhline(d_max*1e6, color="black", linestyle="--")
plt.text(0.06, d_min*1e6, "d min", rotation=0)
plt.text(0.06, d_max*1e6, "d max", rotation=0)

# ----------------------------
# KNUDSEN REGIME BOUNDARIES (LABELED)
# ----------------------------
for kn, style in [(Kn_min, ":"), (Kn_max, ":")]:

    lam_ref = gases["He"]["lambda_1atm"]

    d_kn = lam_ref / (P * kn)

    plt.plot(
        P,
        d_kn * 1e6,
        "k" + style,
        linewidth=1.5,
        label=f"Kn = {kn}"
    )

# ----------------------------
# REGION ANNOTATIONS
# ----------------------------
plt.text(0.07, 25, "Thermal failure region", fontsize=10)
plt.text(0.3, 5, "Feasible ESC operating window", fontsize=10)
plt.text(1.5, 0.5, "Free-molecular / invalid region", fontsize=10)

# ----------------------------
# AXES + TITLE
# ----------------------------
plt.xscale("log")
plt.yscale("log")

plt.xlabel("Backside Pressure P (atm)")
plt.ylabel("Gap d (µm)")

plt.title(
    "ESC Phase Diagram with Explicit Acceptable Ranges\n"
    "(Pressure, Gap, and Knudsen Regimes Fully Labeled)"
)

plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.4)

plt.show()