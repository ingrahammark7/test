import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# GAS CONSTANTS (RELATIVE MODEL)
# ----------------------------

# normalized helium baseline = 1
k_He = 0.15
k_Ar = 0.018

lambda_He0 = 200e-9   # effective reference (order)
lambda_Ar0 = 68e-9

P0 = 101325

# ----------------------------
# TARGET EQUIVALENCE PARAMETERS
# ----------------------------

# we enforce "He-like regime preservation"
Kn_target = 0.05  # mid-slip regime

G_min = 1e5  # stability threshold (arbitrary ESC baseline)

b = 2.0

# ----------------------------
# PRESSURE DOMAIN
# ----------------------------
P = np.logspace(3, 7, 1000)

# ----------------------------
# HELIUM REFERENCE BEHAVIOR
# ----------------------------
lambda_He = lambda_He0 * (P0 / P)

d_He_equiv = lambda_He / Kn_target

# ----------------------------
# ARGON REAL BEHAVIOR
# ----------------------------
lambda_Ar = lambda_Ar0 * (P0 / P)

d_Ar_kn_equiv = lambda_Ar / Kn_target

# ----------------------------
# THERMAL EQUIVALENCE CONDITION
# ----------------------------
# match He conductance envelope
G_He = k_He / (d_He_equiv + b * lambda_He)

# Ar must satisfy same G threshold
d_Ar_thermal = (k_Ar / G_min) - b * lambda_Ar

# ----------------------------
# PHYSICAL LIMITS
# ----------------------------
d_min = 2e-6
d_max = 100e-6

# ----------------------------
# FEASIBILITY (TRUE REPLACEMENT REGION)
# ----------------------------
lower = np.maximum(d_min, np.maximum(d_Ar_kn_equiv, d_Ar_thermal))
upper = np.minimum(d_max, d_Ar_kn_equiv * 2.0)  # allow transition margin

valid = upper > lower

# ----------------------------
# PLOT
# ----------------------------
plt.figure(figsize=(10, 7))

plt.fill_between(P[valid],
                 lower[valid] * 1e6,
                 upper[valid] * 1e6,
                 color="green",
                 alpha=0.5,
                 label="Argon ≈ Helium ESC-equivalent region")

# ----------------------------
# BOUNDARIES
# ----------------------------
plt.plot(P, d_He_equiv * 1e6, "blue", label="Helium ideal ESC regime")
plt.plot(P, d_Ar_kn_equiv * 1e6, "purple", label="Argon Kn equivalent")
plt.plot(P, d_Ar_thermal * 1e6, "red", label="Argon thermal limit")

plt.axhline(d_min * 1e6, color="black", linestyle="--", label="Mechanical min gap")

# ----------------------------
# AXES
# ----------------------------
plt.xscale("log")
plt.yscale("log")

plt.xlabel("Pressure (Pa)")
plt.ylabel("Gap (µm)")
plt.title("Helium → Argon ESC Replacement Feasibility Envelope")

plt.grid(True, which="both", alpha=0.3)
plt.legend()

plt.savefig("he_to_ar_esc_replacement.png", dpi=300, bbox_inches="tight")
plt.show()

print("Saved: he_to_ar_esc_replacement.png")