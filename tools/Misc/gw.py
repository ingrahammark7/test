import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parameters (EDIT)
# -----------------------------

A = 0.015
rho = 1.0
k = 5e-5

eta = 0.2

# Thermal limit (fiberglass-like Tg region)
T_max = 450.0      # K (~177 C)
T_inf = 220.0

h = 80.0
sigma = 5.67e-8
epsilon = 0.8

# -----------------------------
# Compute cooling at limit
# -----------------------------

Q_loss = (
    h * A * (T_max - T_inf) +
    epsilon * sigma * A * (T_max**4 - T_inf**4)
)

# -----------------------------
# Sweep radar power
# -----------------------------

P_vals = np.linspace(0, 2000, 200)  # W
v_vals = []

for P in P_vals:
    Q_radar = eta * P
    
    if Q_radar >= Q_loss:
        v_vals.append(np.nan)  # no solution (overheats even at v=0)
    else:
        v = ((Q_loss - Q_radar) / (k * rho * A))**(1/3)
        v_vals.append(v)

# -----------------------------
# Plot isoquant
# -----------------------------

plt.plot(P_vals, v_vals)
plt.xlabel("Radar Power (W)")
plt.ylabel("Max Velocity before T_max (m/s)")
plt.title("Radome Thermal Limit Isoquant")
plt.grid()
plt.show()