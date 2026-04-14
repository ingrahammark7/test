import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# GAS DATA (physical, consistent)
# ----------------------------
gases = {
    "He": {"k": 0.151, "lambda_1atm": 180e-9},
    "H2": {"k": 0.180, "lambda_1atm": 110e-9},
    "Ne": {"k": 0.049, "lambda_1atm": 65e-9},
    "N2": {"k": 0.025, "lambda_1atm": 65e-9},
    "Ar": {"k": 0.018, "lambda_1atm": 70e-9},
}

names = list(gases.keys())

# ----------------------------
# PHYSICS
# ----------------------------
q_load = 5e4
DeltaT = 20
G_req = q_load / DeltaT
b = 2.0

# ----------------------------
# SYSTEM BOUNDS
# ----------------------------
P_min, P_max = 0.05, 5.0
d_min, d_max = 0.2e-6, 50e-6

Kn_min, Kn_max = 1e-3, 10

# ----------------------------
# GRID
# ----------------------------
P = np.logspace(np.log10(P_min), np.log10(P_max), 450)
d = np.logspace(np.log10(d_min), np.log10(d_max), 450)

P_grid, d_grid = np.meshgrid(P, d)

# ----------------------------
# STORAGE
# ----------------------------
feasible_stack = []

plt.figure(figsize=(12,8))

# ----------------------------
# COMPUTE PER GAS
# ----------------------------
for g in names:

    k = gases[g]["k"]
    lam0 = gases[g]["lambda_1atm"]

    lam = lam0 / P_grid
    Kn = lam / d_grid

    G = k / (d_grid + b * lam)

    feasible = (
        (G >= G_req) &
        (Kn >= Kn_min) & (Kn <= Kn_max) &
        (P_grid >= P_min) & (P_grid <= P_max) &
        (d_grid >= d_min) & (d_grid <= d_max)
    )

    feasible_stack.append(feasible)

feasible_stack = np.array(feasible_stack)

# ----------------------------
# GLOBAL FEASIBLE REGION
# ----------------------------
global_feasible = np.any(feasible_stack, axis=0)

plt.contourf(
    P_grid,
    d_grid*1e6,
    global_feasible,
    levels=[0.5, 1],
    colors=["lightgreen"],
    alpha=0.3
)

# ----------------------------
# WINNER MAP (ONLY WHERE FEASIBLE)
# ----------------------------
sum_feasible = np.sum(feasible_stack, axis=0)

winner = np.full(P_grid.shape, -1)

for i in range(len(names)):
    only = feasible_stack[i] & (sum_feasible == 1)
    winner[only] = i

mix = sum_feasible > 1
winner[mix] = len(names)

plt.imshow(
    winner,
    origin="lower",
    extent=[P_min, P_max, d_min*1e6, d_max*1e6],
    aspect="auto",
    cmap="tab10",
    alpha=0.35
)

# ----------------------------
# TRUE KNUDSEN BOUNDARIES (PER GAS)
# ----------------------------
for g in names:

    lam0 = gases[g]["lambda_1atm"]

    d_kn_low = lam0 / (P * Kn_max)
    d_kn_high = lam0 / (P * Kn_min)

    plt.plot(P, d_kn_low*1e6, 'k--', alpha=0.3)
    plt.plot(P, d_kn_high*1e6, 'k--', alpha=0.3)

# ----------------------------
# SYSTEM BOUNDS
# ----------------------------
plt.axvline(P_min, color="black", linewidth=1)
plt.axvline(P_max, color="black", linewidth=1)
plt.axhline(d_min*1e6, color="black", linewidth=1)
plt.axhline(d_max*1e6, color="black", linewidth=1)

# ----------------------------
# GAS BOUNDARY LABELS (THERMAL)
# ----------------------------
for g in names:

    k = gases[g]["k"]
    lam0 = gases[g]["lambda_1atm"]

    d_boundary = k / G_req - b * lam0 / P
    valid = d_boundary > 0

    plt.plot(
        P[valid],
        d_boundary[valid]*1e6,
        linewidth=2,
        label=f"{g} thermal boundary"
    )

# ----------------------------
# FORMATTING
# ----------------------------
plt.xscale("log")
plt.yscale("log")

plt.xlabel("Backside Pressure P (atm)")
plt.ylabel("Gap d (µm)")
plt.title("FULL ESC PHASE DIAGRAM (Correctly Closed Constraint System)")

plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.4)

plt.show()