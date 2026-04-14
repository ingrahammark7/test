import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# GAS DATA (fully explicit)
# ----------------------------
gases = {
    "He": {"k": 0.151, "lambda_1atm": 180e-9, "color": "blue"},
    "H2": {"k": 0.180, "lambda_1atm": 110e-9, "color": "green"},
    "Ne": {"k": 0.049, "lambda_1atm": 65e-9,  "color": "orange"},
    "N2": {"k": 0.025, "lambda_1atm": 65e-9,  "color": "purple"},
    "Ar": {"k": 0.018, "lambda_1atm": 70e-9,  "color": "red"},
}

# ----------------------------
# PHYSICS PARAMETERS (NO MAGIC NUMBERS)
# ----------------------------
q_load = 5e4
DeltaT = 20
G_req = q_load / DeltaT

b = 2.0

# ----------------------------
# HARD SYSTEM BOUNDS
# ----------------------------
P_min, P_max = 0.05, 5.0
d_min, d_max = 0.2e-6, 50e-6

# ----------------------------
# GRID
# ----------------------------
P = np.logspace(np.log10(P_min), np.log10(P_max), 500)
d = np.logspace(np.log10(d_min), np.log10(d_max), 500)

P_grid, d_grid = np.meshgrid(P, d)

plt.figure(figsize=(12, 8))

# ----------------------------
# STORE GLOBAL FEASIBILITY
# ----------------------------
feasible_stack = []

# ----------------------------
# MAIN LOOP (FULL CONSISTENCY)
# ----------------------------
for name, g in gases.items():

    k = g["k"]
    lam0 = g["lambda_1atm"]

    lam = lam0 / P_grid
    Kn = lam / d_grid

    # full governing equation
    G = k / (d_grid + b * lam)

    # ----------------------------
    # constraints (ALL INCLUDED HERE)
    # ----------------------------
    thermal_ok = G >= G_req
    kn_ok = (Kn >= 1e-3) & (Kn <= 10)
    bounds_ok = (
        (P_grid >= P_min) & (P_grid <= P_max) &
        (d_grid >= d_min) & (d_grid <= d_max)
    )

    feasible = thermal_ok & kn_ok & bounds_ok
    feasible_stack.append(feasible)

    # ----------------------------
    # PLOT TRUE THERMAL BOUNDARY
    # Solve G = G_req → d(P)
    # ----------------------------
    d_boundary = k / G_req - b * lam0 / P

    valid = (d_boundary > 0)

    plt.plot(
        P[valid],
        d_boundary[valid] * 1e6,
        color=g["color"],
        linewidth=2,
        label=f"{name} thermal boundary"
    )

# ----------------------------
# KNUDSEN BOUNDARIES (GLOBAL CORRECT FORM)
# ----------------------------
for kn in [1e-3, 10]:

    # use representative gas (He) only for boundary shape
    lam0 = gases["He"]["lambda_1atm"]

    d_kn = lam0 / (P * kn)

    plt.plot(
        P,
        d_kn * 1e6,
        "k--",
        linewidth=1,
        label=f"Kn = {kn}"
    )

# ----------------------------
# SYSTEM BOUNDS BOX
# ----------------------------
plt.axvline(P_min, color="gray", linewidth=1)
plt.axvline(P_max, color="gray", linewidth=1)
plt.axhline(d_min * 1e6, color="gray", linewidth=1)
plt.axhline(d_max * 1e6, color="gray", linewidth=1)

# ----------------------------
# FORMATTING
# ----------------------------
plt.xscale("log")
plt.yscale("log")

plt.xlabel("Backside Pressure P (atm)")
plt.ylabel("Gap d (µm)")
plt.title("ESC Gas Phase Diagram (Fully Consistent Constraint System)")

plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.4)

plt.show()