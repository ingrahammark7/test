import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# ----------------------------
# GAS MODEL
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
# SYSTEM
# ----------------------------
q_load = 5e4
DeltaT = 20
G_req = q_load / DeltaT
b = 2.0

P_min, P_max = 0.05, 5.0
d_min, d_max = 0.2e-6, 50e-6

Kn_min, Kn_max = 1e-3, 10

# ----------------------------
# GRID
# ----------------------------
P = np.logspace(np.log10(P_min), np.log10(P_max), 350)
d = np.logspace(np.log10(d_min), np.log10(d_max), 350)

P_grid, d_grid = np.meshgrid(P, d)

# ----------------------------
# STORAGE
# ----------------------------
F_stack = []
G_stack = []

# ----------------------------
# COMPUTE
# ----------------------------
for g in names:

    k = gases[g]["k"]
    lam0 = gases[g]["lambda_1atm"]

    lam = lam0 / P_grid
    Kn = lam / d_grid

    G = k / (d_grid + b * lam)

    feasible = (
        (G >= G_req) &
        (Kn >= Kn_min) &
        (Kn <= Kn_max)
    )

    F_stack.append(feasible)
    G_stack.append(G)

F_stack = np.array(F_stack)
G_stack = np.array(G_stack)

# ----------------------------
# GLOBAL FEASIBILITY
# ----------------------------
global_feasible = np.any(F_stack, axis=0)

# ----------------------------
# WINNER MAP (SAFE)
# ----------------------------
G_safe = G_stack.copy()
G_safe[~F_stack] = -1e20

winner = np.argmax(G_safe, axis=0)
winner[~global_feasible] = -1

# ----------------------------
# COLORS + LABELS
# ----------------------------
cmap = ListedColormap([
    "lightblue",   # He
    "orange",      # H2
    "green",       # Ne
    "purple",      # N2
    "red",         # Ar
    "black"        # infeasible / mixed
])

label_map = {i: names[i] for i in range(len(names))}
label_map[-1] = "Infeasible"

# ----------------------------
# PLOT
# ----------------------------
plt.figure(figsize=(13, 9))

img = plt.pcolormesh(
    P_grid,
    d_grid * 1e6,
    winner,
    shading="auto",
    cmap=cmap
)

# ----------------------------
# FEASIBILITY BOUNDARY
# ----------------------------
plt.contour(
    P_grid,
    d_grid * 1e6,
    global_feasible.astype(int),
    levels=[0.5],
    colors="black",
    linewidths=2
)

# ----------------------------
# KNUDSEN REGIME LABELS
# ----------------------------
P_line = np.logspace(np.log10(P_min), np.log10(P_max), 500)

for g in names:
    lam0 = gases[g]["lambda_1atm"]

    d_continuum = lam0 / (P_line * Kn_min)
    d_transition = lam0 / (P_line * Kn_max)

    plt.plot(P_line, d_continuum * 1e6, '--', alpha=0.3, color="gray")
    plt.plot(P_line, d_transition * 1e6, '--', alpha=0.3, color="gray")

# ----------------------------
# AXES + LABELS
# ----------------------------
plt.xscale("log")
plt.yscale("log")

plt.xlabel("Backside Pressure P (atm)", fontsize=12)
plt.ylabel("Gap d (µm)", fontsize=12)
plt.title("ESC PHASE DIAGRAM — FULLY LABELED & PHYSICALLY BOUNDED", fontsize=14)

# ----------------------------
# LEGEND (MANUAL, CLEAR)
# ----------------------------
from matplotlib.patches import Patch

legend_elements = [
    Patch(facecolor="lightblue", label="He"),
    Patch(facecolor="orange", label="H2"),
    Patch(facecolor="green", label="Ne"),
    Patch(facecolor="purple", label="N2"),
    Patch(facecolor="red", label="Ar"),
    Patch(facecolor="black", label="Infeasible"),
]

plt.legend(handles=legend_elements, loc="upper right")

plt.grid(True, which="both", linestyle="--", alpha=0.3)

plt.show()