import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# ARGON CONSTANTS
# ----------------------------
lambda_0 = 68e-9
P0 = 101325
k_Ar = 0.018
b = 2.0

Kn_min = 0.01
Kn_max = 0.1

d_min = 2e-6

# ----------------------------
# GRID
# ----------------------------
P = np.logspace(3, 7, 500)
d = np.logspace(-7, -4, 500)

P_grid, d_grid = np.meshgrid(P, d)

# ----------------------------
# KNUDSEN BOUNDS (TRUE ENVELOPE)
# ----------------------------
P_kn_min = (lambda_0 * P0) / (Kn_max * d_grid)
P_kn_max = (lambda_0 * P0) / (Kn_min * d_grid)

# ----------------------------
# MEAN FREE PATH
# ----------------------------
lambda_g = lambda_0 * (P0 / P_grid)

# ----------------------------
# THERMAL CONDUCTANCE
# ----------------------------
G = k_Ar / (d_grid + b * lambda_g)
G_min = 1e5

# approximate thermal boundary via threshold mask
thermal_ok = G >= G_min

# ----------------------------
# GEOMETRY
# ----------------------------
geo_ok = d_grid >= d_min

# ----------------------------
# FULL FEASIBILITY MASK (IMPORTANT FIX)
# ----------------------------
pressure_ok = (P_grid >= P_kn_min) & (P_grid <= P_kn_max)

feasible = pressure_ok & thermal_ok & geo_ok

# ----------------------------
# PLOT
# ----------------------------
plt.figure(figsize=(10, 7))

# feasibility region (now truly bounded)
plt.contourf(P_grid, d_grid * 1e6, feasible,
             levels=[0.5, 1], colors=["#4CAF50"], alpha=0.6)

# Knudsen envelope (THIS is the real wedge boundary)
plt.contour(P_grid, d_grid * 1e6, P_grid - P_kn_min,
            levels=[0], colors="blue", linestyles="--")
plt.contour(P_grid, d_grid * 1e6, P_grid - P_kn_max,
            levels=[0], colors="blue", linestyles="--")

# thermal cutoff
plt.contour(P_grid, d_grid * 1e6, G,
            levels=[G_min], colors="red", linestyles="-")

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Pressure (Pa)")
plt.ylabel("Gap (µm)")
plt.title("Argon ESC Fully Bounded Feasibility Envelope")

plt.grid(True, which="both", alpha=0.2)

plt.show()