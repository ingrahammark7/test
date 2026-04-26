import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parameters
# -----------------------------

A = 0.015
rho_air = 1.225

eta = 0.2

T_max = 450.0
T_inf = 220.0

h = 80.0
sigma = 5.67e-8
epsilon = 0.8

# aerodynamic heating coefficient (effective)
C_aero = 1e-4  # tune this

# -----------------------------
# Cooling capacity at limit
# -----------------------------

Q_cool = (
    h * A * (T_max - T_inf) +
    epsilon * sigma * A * (T_max**4 - T_inf**4)
)

# -----------------------------
# Sweep radar power
# -----------------------------

P_vals = np.linspace(0, 2000, 200)
v_max = []

for P in P_vals:
    Q_radar = eta * P

    available = Q_cool - Q_radar

    if available <= 0:
        v_max.append(np.nan)
        continue

    # Solve for velocity limit:
    # C rho v^3 A = available
    v = (available / (C_aero * rho_air * A))**(1/3)
    v_max.append(v)

# -----------------------------
# Plot
# -----------------------------

plt.plot(P_vals, v_max)
plt.xlabel("Radar Power (W)")
plt.ylabel("Max Velocity before T_max (m/s)")
plt.title("Thermal + Aerodynamic Radome Limit Isoquant")
plt.grid()
plt.show()