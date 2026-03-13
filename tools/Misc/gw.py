import json
import matplotlib.pyplot as plt
import numpy as np

# Load JSON
with open("rockets.json") as f:
    rockets = json.load(f)

# Extract data
masses = np.array([r["mass_kg"] for r in rockets])
ranges = np.array([r["range_km"] for r in rockets])
names = [r["name"] for r in rockets]
types = [r["type"] for r in rockets]

# Fit power law: log(R) = log(a) + alpha*log(M)
log_m = np.log10(masses)
log_r = np.log10(ranges)
alpha, log_a = np.polyfit(log_m, log_r, 1)
a = 10**log_a

print(f"Fitted power law: R = {a:.2f} * M^{alpha:.2f}")

# Plot
plt.figure(figsize=(10,6))
plt.scatter(masses, ranges, c='blue')

# Annotate each point
for i, name in enumerate(names):
    plt.text(masses[i]*1.05, ranges[i]*1.05, name, fontsize=9)

# Plot fitted line
mass_fit = np.logspace(np.log10(min(masses)), np.log10(max(masses)), 100)
range_fit = a * mass_fit**alpha
plt.plot(mass_fit, range_fit, 'r--', label=f'Fit: R = {a:.2f} * M^{alpha:.2f}')

plt.xscale('log')
plt.yscale('log')
plt.xlabel("Launch mass (kg, log scale)")
plt.ylabel("Ballistic/Effective range (km, log scale)")
plt.title("Allometric scaling: Rocket mass vs ballistic/slant range")
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.show()