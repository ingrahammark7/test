import json
import matplotlib.pyplot as plt
import numpy as np

# Load JSON
with open("rockets.json") as f:
    rockets = json.load(f)

# Extract data
masses = np.array([r["mass_kg"] for r in rockets])
payloads = np.array([r["payload_kg"] for r in rockets])
ranges = np.array([r["range_km"] for r in rockets])
names = [r["name"] for r in rockets]
types = [r["type"] for r in rockets]

# Compute payload fraction and mass efficiency
payload_fraction = payloads / masses
mass_efficiency = masses / ranges  # kg per km

# Set up figure with 2 subplots
fig, axes = plt.subplots(1, 2, figsize=(14,6))

# Panel 1: log-log mass vs range
ax = axes[0]
ax.scatter(masses, ranges, c='blue')
for i, name in enumerate(names):
    ax.text(masses[i]*1.05, ranges[i]*1.05, name, fontsize=9)
ax.plot([10, 3e6], [1, 1e5], 'r--', label='10 kg/km rule')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel("Launch mass (kg)")
ax.set_ylabel("Range (km)")
ax.set_title("Rocket mass vs range")
ax.grid(True, which="both", ls="--", alpha=0.5)
ax.legend()

# Panel 2: mass efficiency vs payload fraction
ax = axes[1]
ax.scatter(payload_fraction, mass_efficiency, c='green')
for i, name in enumerate(names):
    ax.text(payload_fraction[i]*1.05, mass_efficiency[i]*1.05, name, fontsize=9)
ax.set_xlabel("Payload fraction (payload/mass)")
ax.set_ylabel("Mass efficiency (kg/km)")
ax.set_title("Mass efficiency vs payload fraction")
ax.grid(True, ls="--", alpha=0.5)
ax.set_yscale('log')
plt.tight_layout()
plt.show()