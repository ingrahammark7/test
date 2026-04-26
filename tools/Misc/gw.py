import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Atmosphere (simple ISA-like)
# -----------------------------

def rho(h):
    return 1.225 * np.exp(-h / 8500)

def speed_of_sound(h):
    return 340.0  # simplified constant for clarity

# -----------------------------
# Model parameters
# -----------------------------

A = 0.015
eta = 0.2

C_aero = 1.2e-4     # aero heating coefficient
beta = 0.25         # Mach amplification

h = 5000  # fixed altitude (you can sweep later)

T_limit = 450.0
T_inf = 220.0

h_conv = 80.0
sigma = 5.67e-8
epsilon = 0.8

# -----------------------------
# Heat model
# -----------------------------

def Q_aero(M):
    v = M * speed_of_sound(h)
    return C_aero * rho(h) * (v**3) * A * (1 + beta * M)

def Q_rf(P):
    return eta * P

def Q_out(T):
    return h_conv * A * (T - T_inf) + epsilon * sigma * A * (T**4 - T_inf**4)

# -----------------------------
# Feasibility grid
# -----------------------------

M_vals = np.linspace(0.5, 6.0, 120)
P_vals = np.linspace(0, 2000, 120)

feasible = np.zeros((len(M_vals), len(P_vals)))

# quasi-steady assumption: solve T implicitly by checking balance
T_guess = T_limit

for i, M in enumerate(M_vals):
    for j, P in enumerate(P_vals):

        Qin = Q_aero(M) + Q_rf(P)
        Qout = Q_out(T_limit)

        # feasibility condition
        if Qin <= Qout:
            feasible[i, j] = 1
        else:
            feasible[i, j] = 0

# -----------------------------
# Plot
# -----------------------------

plt.figure(figsize=(8,6))
plt.contourf(P_vals, M_vals, feasible, levels=[-0.5,0.5,1.5], cmap="coolwarm")
plt.xlabel("RF Power (W)")
plt.ylabel("Mach")
plt.title("Thermal Feasibility Map (Mach vs RF Power)")
plt.colorbar(label="Feasible (1=yes, 0=no)")
plt.show()