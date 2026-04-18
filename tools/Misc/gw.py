import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PARAMETERS (generic system)
# -----------------------------
m = 0.001          # 1 g = 0.001 kg
cp = 1000          # J/kg-K (generic solid)
C = m * cp

T_env = 300        # ambient K

# Heating power (parameter you vary)
P = 5.0            # Watts (electrical input)

# Cooling
h = 0.02           # W/K

# Kinetics (generic Arrhenius system)
A = 1e5            # 1/s
Ea = 80000         # J/mol
R = 8.314          # gas constant
n = 1.0

# Time setup
dt = 0.01
t_max = 200

# -----------------------------
# SIMULATION FUNCTION
# -----------------------------
def simulate(P):

    T = T_env
    alpha = 0.0

    T_hist = []
    a_hist = []
    t_hist = []

    for i in range(int(t_max/dt)):

        # reaction rate
        rate = A * np.exp(-Ea / (R * T)) * (1 - alpha)**n

        d_alpha = rate * dt

        # heat balance
        dT = (P - h * (T - T_env)) / C * dt

        # optional coupling (exothermic feedback)
        dT -= 2000 * d_alpha   # reaction heat term (scaled generic)

        T += dT
        alpha += d_alpha

        t_hist.append(i * dt)
        T_hist.append(T)
        a_hist.append(alpha)

        if alpha >= 1.0:
            break

    return np.array(t_hist), np.array(T_hist), np.array(a_hist)

# -----------------------------
# RUN SWEEP OVER POWER LEVELS
# -----------------------------
powers = [1, 2, 5, 10]

plt.figure()

for P in powers:
    t, T, a = simulate(P)
    plt.plot(t, T, label=f"{P} W")

plt.xlabel("Time (s)")
plt.ylabel("Temperature (K)")
plt.title("Thermal + Arrhenius Kinetics System")
plt.legend()
plt.grid()
plt.show()