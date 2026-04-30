import numpy as np

# -----------------------------
# BASIC MODEL PARAMETERS
# -----------------------------

# compute cost per operation (seconds)
compute_latency = 1e-10  # 100 ps per op (abstract core)

# energy per operation (joules)
energy_per_op = 1e-12

# bandwidth limits (bits/sec)
B_chiplet = 1e12   # on-package
B_3d = 5e12        # vertical stack
B_dram = 2e11      # off-chip memory

# energy per bit moved
E_bit_chiplet = 1e-15
E_bit_3d = 5e-16
E_bit_dram = 1e-14

# -----------------------------
# COMPUTE GRAPH STRUCTURE
# -----------------------------

# nodes: (compute units + memory hierarchy)
nodes = [
    "core_A",
    "core_B",
    "chiplet_link",
    "stack_link",
    "L3_cache",
    "DRAM"
]

# edges: (src, dst, data_bits, link_type)
edges = [
    ("core_A", "L3_cache", 1e6, "on_die"),
    ("L3_cache", "core_B", 1e6, "on_die"),
    ("core_A", "chiplet_link", 5e6, "chiplet"),
    ("chiplet_link", "core_B", 5e6, "chiplet"),
    ("core_A", "stack_link", 1e6, "3d"),
    ("stack_link", "core_B", 1e6, "3d"),
    ("core_A", "DRAM", 1e7, "dram"),
]

# -----------------------------
# LINK COST MODELS
# -----------------------------

def link_latency(bits, link_type):
    if link_type == "chiplet":
        return bits / B_chiplet
    elif link_type == "3d":
        return bits / B_3d
    elif link_type == "dram":
        return bits / B_dram
    else:  # on-die cache
        return bits / 1e13  # very fast internal bandwidth

def link_energy(bits, link_type):
    if link_type == "chiplet":
        return bits * E_bit_chiplet
    elif link_type == "3d":
        return bits * E_bit_3d
    elif link_type == "dram":
        return bits * E_bit_dram
    else:
        return bits * 1e-16

# -----------------------------
# GRAPH EXECUTION MODEL
# -----------------------------

def simulate_graph(edges):
    total_latency = 0
    total_energy = 0

    for (src, dst, bits, link_type) in edges:

        # communication cost
        comm_latency = link_latency(bits, link_type)
        comm_energy = link_energy(bits, link_type)

        # compute cost (assume every transfer triggers compute)
        comp_latency = compute_latency
        comp_energy = energy_per_op

        total_latency += comm_latency + comp_latency
        total_energy += comm_energy + comp_energy

    return total_latency, total_energy

# -----------------------------
# RUN SIMULATION
# -----------------------------

lat, energy = simulate_graph(edges)

print("TOTAL SYSTEM LATENCY (s):", lat)
print("TOTAL SYSTEM ENERGY (J):", energy)

# normalize intuition metrics
print("\n--- Derived metrics ---")
print("Energy per second of execution:", energy / lat)
print("Effective throughput (ops/sec approx):", 1 / compute_latency)