import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Node sizes (silicon scaling axis)
# -----------------------------
nodes = np.logspace(-6, -8, 150)  # 1 µm → 10 nm

# -----------------------------
# 1. Intra-die logic delay
# -----------------------------
def transistor_delay(node):
    return 1e-12 * (node / 1e-6) ** 0.6

def contact_delay(node, rho=1.0):
    return rho / node * 1e-13

def interconnect_delay(node):
    return (1 / node**1.5) * 5e-13

def die_compute_delay(node, rho):
    return (
        transistor_delay(node) +
        contact_delay(node, rho) +
        interconnect_delay(node)
    )

# -----------------------------
# 2. Chiplet interconnect (package scale)
# -----------------------------
def chiplet_delay():
    # die-to-die communication on substrate (organic interposer / silicon interposer)
    # much slower than on-die wiring
    return 2e-10  # ~200 ps baseline (simplified)

# -----------------------------
# 3. 3D stacking (TSV / hybrid bonding)
# -----------------------------
def stack_delay():
    # vertical communication between stacked dies
    # better than chiplet, worse than on-die
    return 5e-11  # ~50 ps

# -----------------------------
# 4. Memory hierarchy
# -----------------------------
def l2_l3_cache_delay():
    return 1e-8  # ~10 ns

def dram_delay():
    return 8e-8  # ~80 ns

# -----------------------------
# Total system latency models
# -----------------------------

materials = {
    "Al contact": 2.5,
    "TiSi2 contact": 1.0,
    "NiSi contact": 0.7
}

def full_system_latency(node, rho):
    return (
        die_compute_delay(node, rho) +
        chiplet_delay() +
        stack_delay() +
        l2_l3_cache_delay() +
        dram_delay()
    )

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(10,6))

for name, rho in materials.items():
    y = full_system_latency(nodes, rho)
    plt.loglog(nodes * 1e9, y, label=name)

# reference floors
plt.loglog(nodes * 1e9, [dram_delay()]*len(nodes), '--', label="DRAM latency floor")
plt.loglog(nodes * 1e9, [l2_l3_cache_delay()]*len(nodes), '--', label="Cache hierarchy")

plt.xlabel("Feature size (nm)")
plt.ylabel("System latency (seconds, log scale)")
plt.title("Chiplet + 3D stacking full-system latency model")
plt.legend()
plt.grid(True, which="both", ls="--", alpha=0.3)

plt.show()

# -----------------------------
# Dominance analysis
# -----------------------------
for name, rho in materials.items():
    y = full_system_latency(nodes, rho)

    idx_cache = np.argmax(y > l2_l3_cache_delay())
    idx_dram = np.argmax(y > dram_delay())

    print(f"{name}:")
    print(f"  exceeds cache latency below ~{nodes[idx_cache]*1e9:.1f} nm")
    print(f"  exceeds DRAM latency below ~{nodes[idx_dram]*1e9:.1f} nm\n")