import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# ARGON PARAMETERS
# ----------------------------
lambda_0 = 68e-9
P0 = 101325
k_Ar = 0.018
b = 2.0

Kn_min = 0.01
Kn_max = 0.1

# ----------------------------
# GRID (START BROAD, THEN CLIP)
# ----------------------------
P = np.logspace(3, 7, 500)
d = np.logspace(-7, -4, 500)

P_grid, d_grid = np.meshgrid(P, d)

# ----------------------------
# KNUDSEN BOUNDS (EXACT ENVELOPE)
# ----------------------------
P_kn_min = (lambda_0 * P0) / (Kn_max * d_grid)
P_kn_max = (lambda_0 * P0) / (Kn_min * d_grid)

# ----------------------------
# GAP BOUNDS (THIS FIXES YOUR REQUEST)
# ----------------------------

d_min = 2e-6  # mechanical lower bound

# upper gap bound derived from Kn constraint
d_max_kn = (lambda_0 * P0) / (Kn_min * P_grid)

gap_ok = (d_grid >= d_min) & (d_grid <= d_max_kn)

# ----------------------------
# MEAN FREE PATH + THERMAL MODEL
# ----------------------------
lambda_g = lambda_0 * (P0 / P_grid)
G = k_Ar / (d_grid + b * lambda_g)

G_min = 1e5
thermal_ok = G >= G_min

# ----------------------------
# PRESSURE WINDOW (ALSO BOUNDED)
# ----------------------------
pressure_ok = (P_grid >= P_kn_min) & (P_grid <= P_kn_max)

# ----------------------------
# FULL FEASIBILITY
# ----------------------------
feasible = pressure_ok & thermal_ok & gap_ok

# ----------------------------
# PLOT
# ----------------------------
plt.figure(figsize=(10, 7))

# feasible region
plt.contourf(P_grid, d_grid * 1e6, feasible,
             levels=[0.5, 1], colors=["#4CAF50"], alpha=0.65)

# explicit gap bounds (THIS IS THE NEW PART)
plt.contour(P_grid, d_grid * 1e6, d_grid - d_min,
            levels=[0], colors="black", linestyles="--")

plt.contour(P_grid, d_grid * 1e6, d_grid - d_max_kn,
            levels=[0], colors="purple", linestyles="--")

# Knudsen pressure bounds
plt.contour(P_grid, d_grid * 1e6, P_grid - P_kn_min,
            levels=[0], colors="blue", linestyles="--")

plt.contour(P_grid, d_grid * 1e6, P_grid - P_kn_max,
            levels=[0], colors="blue", linestyles="--")

# thermal boundary
plt.contour(P_grid, d_grid * 1e6, G,
            levels=[G_min], colors="red")

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Pressure (Pa)")
plt.ylabel("Gap (µm)")
plt.title("Fully Bounded Argon ESC Feasibility Envelope (Closed Domain)")

plt.grid(True, which="both", alpha=0.2)

plt.show()