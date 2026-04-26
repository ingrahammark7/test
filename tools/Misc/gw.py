import numpy as np
import matplotlib.pyplot as plt

# loss range
loss = np.linspace(0, 0.9, 300)
P0 = 1.0

# base power
P = P0 * (1 - loss)

# combustion stability function
Lc = 0.45   # critical breakdown point
k = 25      # sharpness of failure

S = 1 / (1 + np.exp(k * (loss - Lc)))

# effective power after stability constraint
P_eff = P * S

# aerodynamic max speed
v = (P_eff) ** (1/3)

# normalize to km/h baseline (210 km/h)
v_kmh = 210 * v

plt.plot(loss * 100, 210 * (P ** (1/3)), '--', label="Ideal (no combustion limits)")
plt.plot(loss * 100, v_kmh, label="With combustion stability constraint")
plt.xlabel("Power loss (%)")
plt.ylabel("Max speed (km/h)")
plt.title("Max Speed with Combustion Stability Threshold")
plt.legend()
plt.grid(True)
plt.show()