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
L = 6.5e-3

C_aero = 1e-4
beta = 0.3

T_max = 450.0

h_conv = 80.0
sigma = 5.67e-8
epsilon = 0.8

# -----------------------------
# ISA functions
# -----------------------------

def T_isa(h):
    return T0 - L * h

def rho_isa(h):
    T = T_isa(h)
    return rho0 * (T / T0) ** (g / (R * L))

def a_sound(h):
    return np.sqrt(gamma * R * T_isa(h))

# -----------------------------
# Grids
# -----------------------------

altitudes = np.linspace(0, 10000, 40)
Mach = np.linspace(0.2, 6.0, 120)
Power = np.linspace(0, 2000, 120)

# weights (tunable mission preference)
w_mach = 1.0
w_power = 0.0005
w_margin = 2.0

corridor_M = []
corridor_P = []
corridor_H = []

# -----------------------------
# Optimization loop
# -----------------------------

for h in altitudes:

    T = T_isa(h)
    rho = rho_isa(h)
    a = a_sound(h)

    best_score = -1e18
    best_m = np.nan
    best_p = np.nan

    for M in Mach:
        v = M * a

        Q_aero = C_aero * rho * (v**3) * A * (1 + beta * M)

        for P in Power:
            Q_radar = eta * P

            Q_cool = (
                h_conv * A * (T_max - T) +
                epsilon * sigma * A * (T_max**4 - T**4)
            )

            if Q_aero + Q_radar > Q_cool:
                continue

            margin = Q_cool - (Q_aero + Q_radar)

            score = (
                w_mach * M
                - w_power * P
                - w_margin / (margin + 1e-6)
            )

            if score > best_score:
                best_score = score
                best_m = M
                best_p = P

    corridor_M.append(best_m)
    corridor_P.append(best_p)
    corridor_H.append(h)

# -----------------------------
# Plot corridor projections
# -----------------------------

plt.figure()
plt.plot(corridor_M, corridor_H)
plt.xlabel("Mach")
plt.ylabel("Altitude (m)")
plt.title("Operational Corridor: Mach vs Altitude")
plt.grid()
plt.show()

plt.figure()
plt.plot(corridor_P, corridor_H)
plt.xlabel("Radar Power (W)")
plt.ylabel("Altitude (m)")
plt.title("Operational Corridor: Power vs Altitude")
plt.grid()
plt.show()

plt.figure()
plt.plot(corridor_M, corridor_P)
plt.xlabel("Mach")
plt.ylabel("Radar Power (W)")
plt.title("Operational Corridor: Mach vs Radar Power")
plt.grid()
plt.show()