import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Node sizes (meters)
# -----------------------------
nodes = np.logspace(-6, -8, 150)  # 1 µm → 10 nm

# -----------------------------
# MATERIAL / PROCESS LAYERS
# -----------------------------

# 1) transistor switching delay
# scales roughly with capacitance + drive strength improvements
def transistor_delay(node):
    # improves with scaling, but saturates
    return 1e-12 * (node / 1e-6) ** 0.6


# 2) contact delay (silicide vs metal contact)
def contact_delay(node, rho=1.0):
    # resistance increases as area shrinks
    return rho / node * 1e-13


# 3) interconnect delay (dominant scaling bottleneck)
def interconnect_delay(node):
    # RC + wire length penalty grows sharply
    return (1 / node**1.5) * 5e-13


# 4) memory latency (effectively independent of node scaling)
def memory_delay():
    # DRAM + hierarchy bottleneck (fixed physics + architecture)
    return 8e-8  # ~80 ns typical DRAM latency


# -----------------------------
# MATERIAL variants (contact layer)
# -----------------------------
materials = {
    "Al contact": 2.5,
    "TiSi2 contact": 1.0,
    "NiSi contact": 0.7
}

# -----------------------------
# Compute total system latency
# -----------------------------
def total_latency(node, rho):
    return (
        transistor_delay(node) +
        contact_delay(node, rho) +
        interconnect_delay(node) +
        memory_delay()
    )

# -----------------------------
# Plot results
# -----------------------------
plt.figure(figsize=(10,6))

for name, rho in materials.items():
    total = total_latency(nodes, rho)
    plt.loglog(nodes * 1e9, total, label=name)

# -----------------------------
# Add component reference curves
# -----------------------------
plt.loglog(nodes * 1e9, interconnect_delay(nodes), '--', label="Interconnect (dominant trend)")
plt.loglog(nodes * 1e9, [memory_delay()]*len(nodes), '--', label="Memory latency floor")

plt.xlabel("Feature size (nm)")
plt.ylabel("Latency (seconds, log scale)")
plt.title("Full-chip scaling model: transistor + contact + interconnect + memory")
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.3)

plt.show()


# -----------------------------
# Find where memory dominates
# -----------------------------
for name, rho in materials.items():
    total = total_latency(nodes, rho)
    idx = np.argmax(total > memory_delay())
    print(f"{name}: memory dominates below ~{nodes[idx]*1e9:.1f} nm")