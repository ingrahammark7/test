import numpy as np
import matplotlib.pyplot as plt

# water fraction from 0 to 0.6 (0% to 60%)
w = np.linspace(0, 0.6, 200)

# baseline fuel energy (normalized)
E_f = 1.0

def power_output(w, k):
    vapor_efficiency = np.exp(-k * w)
    return (1 - w) * E_f * vapor_efficiency

# two sensitivity cases
P_low_sens = power_output(w, k=2)
P_high_sens = power_output(w, k=5)

plt.plot(w, P_low_sens, label="Low sensitivity (k=2)")
plt.plot(w, P_high_sens, label="High sensitivity (k=5)")
plt.xlabel("Water fraction")
plt.ylabel("Normalized power output")
plt.title("Effect of Water Fraction on Effective Power (Evaporation-limited model)")
plt.legend()
plt.grid(True)
plt.show()