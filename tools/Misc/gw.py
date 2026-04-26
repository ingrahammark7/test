import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Simple environment model
# -----------------------------

h = 5000  # altitude fixed
rho = 0.6  # simplified constant density
A = 0.015

eta = 0.2
C_aero = 1.2e-4
beta = 0.25

def speed_of_sound():
    return 340.0

# Aero heating
def Q_aero(M):
    v = M * speed_of_sound()
    return C_aero * rho * (v**3) * A * (1 + beta * M)

# RF heating
def Q_rf(P):
    return eta * P

# -----------------------------
# Grid
# -----------------------------

M_vals = np.linspace(0.5, 6, 200)
P_vals = np.linspace(0, 2000, 200)

M_grid, P_grid = np.meshgrid(M_vals, P_vals)

Qa = Q_aero(M_grid)
Qr = Q_rf(P_grid)

# -----------------------------
# Dominance condition
# RF dominant when RF > aero
# -----------------------------

rf_dominant = Qr > Qa

# -----------------------------
# Plot
# -----------------------------

plt.figure(figsize=(8,6))

plt.contourf(P_grid, M_grid, rf_dominant, levels=[-0.5,0.5,1.5], cmap="coolwarm")
plt.colorbar(label="RF dominant (1=yes)")

plt.xlabel("RF Power (W)")
plt.ylabel("Mach")
plt.title("RF Dominance Boundary: Q_RF > Q_aero")

plt.show()