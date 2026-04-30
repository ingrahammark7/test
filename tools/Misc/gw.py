import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Node sizes (meters)
# 1 µm → 10 nm
# -----------------------------
nodes = np.logspace(-6, -8, 100)

# -----------------------------
# Material parameters (relative units)
# These are NOT real resistivities,
# just normalized comparison factors.
# -----------------------------
materials = {
    "Al (Aluminum contact)": 2.8,
    "TiSi2 (Titanium silicide)": 1.0,
    "NiSi (Nickel silicide)": 0.7
}

# -----------------------------
# Scaling model:
# We assume:
#   - contact area ~ node^2
#   - interconnect/fringe penalty ~ 1/node
# So effective delay scales ~ rho * (1/node)
# -----------------------------
def delay(rho, node):
    return rho / node

# -----------------------------
# Compute curves
# -----------------------------
plt.figure(figsize=(8,5))

for name, rho in materials.items():
    delays = delay(rho, nodes)
    plt.loglog(nodes * 1e9, delays, label=name)

# -----------------------------
# Plot formatting
# -----------------------------
plt.xlabel("Feature size (nm)")
plt.ylabel("Relative delay (arbitrary units)")
plt.title("Scaling limit model: contact/interconnect delay vs node size")
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.3)

plt.show()

# -----------------------------
# Find crossover points
# -----------------------------
al = delay(materials["Al (Aluminum contact)"], nodes)
nisi = delay(materials["NiSi (Nickel silicide)"], nodes)

ratio = al / nisi

# first point where Al is >2× worse than NiSi
idx = np.argmax(ratio > 2)

print("Node where Al becomes >2× worse than NiSi (nm):",
      nodes[idx] * 1e9)