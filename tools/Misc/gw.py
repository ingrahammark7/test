import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Constants
# -----------------------------

A = 0.015
eta = 0.2

gamma = 1.4
R = 287.0
g = 9.81

T0 = 288.15
rho0 = 1.225
L = 6.5e-3  # K/m

C_aero = 1e-4
beta = 0.3

T_max = 450.0

h_conv = 80.0
sigma = 5.67e-8
epsilon = 0.8

# -----------------------------
# ISA atmosphere functions
# -----------------------------

def T_isa(h):
    return T0 - L * h

def rho_isa(h):
    T = T_isa(h)
    return rho0 * (T / T0) ** (g / (R * L))

def speed_of_sound(h):
    return np.sqrt(gamma * R * T_isa(h))

# -----------------------------
# Grid
# -----------------------------

Mach = np.linspace(0.2, 6.0, 120)
P = np.linspace(0, 2000, 120)
Alt = np.linspace(0, 10000, 60)  # 0–10 km slice

M, Pgrid, H = np.meshgrid(Mach, P, Alt, indexing="ij")

T = T_isa(H)
rho = rho_isa(H)
a = speed_of_sound(H)

v = M * a

# -----------------------------
# Heating terms
# -----------------------------

Q_aero = C_aero * rho * (v**3) * A * (1 + beta * M)
Q_radar = eta * Pgrid

Q_cool = (
    h_conv * A * (T_max - T) +
    epsilon * sigma * A * (T_max**4 - T**4)
)

Q_total = Q_aero + Q_radar

feasible = Q_total <= Q_cool

# -----------------------------
# Slice visualization (mid-altitude)
# -----------------------------

mid = len(Alt) // 2

plt.figure()
plt.contourf(Mach, P, feasible[:, :, mid].T, levels=[-0.5, 0.5, 1.5])
plt.xlabel("Mach")
plt.ylabel("Radar Power (W)")
plt.title("ISA Flight Envelope (Mid-Altitude Slice)")
plt.grid(True)
plt.show()