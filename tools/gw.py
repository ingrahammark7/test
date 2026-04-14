import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# SYSTEM PARAMETERS (REALISTIC)
# ----------------------------
lambda_0 = 68e-9
P0 = 101325

k_Ar = 0.018
b = 2.0

Kn_target = 0.05  # design point, not a range

# practical engineering limits (NOT ideal physics)
P_min = 2e3       # pump + control stability floor (~0.02 atm)
P_max = 5e6       # upper ESC regime before stiffness issues

d_min = 1e-6      # dielectric + safety floor
d_max = 50e-6     # manufacturable ESC gap ceiling

# stability margins (human-tuned systems are not razor thin)
stability_margin = 0.35

# ----------------------------
# PRESSURE DOMAIN
# ----------------------------
P = np.logspace(np.log10(P_min), np.log10(P_max), 600)

# ----------------------------
# PHYSICS CORE
# ----------------------------
lambda_g = lambda_0 * (P0 / P)

# equilibrium gap (NOT free choice)
d_eq = lambda_g / Kn_target

# ----------------------------
# STABILITY BAND (REALISTIC HUMAN CONTROL)
# ----------------------------
d_low_stable = d_eq * (1 - stability_margin)
d_high_stable = d_eq * (1 + stability_margin)

# ----------------------------
# APPLY MANUFACTURING LIMITS
# ----------------------------
d_low_stable = np.maximum(d_low_stable, d_min)
d_high_stable = np.minimum(d_high_stable, d_max)

# validity mask
valid = d_high_stable > d_low_stable

# ----------------------------
# FAILURE ZONES (IMPORTANT REALISM)
# ----------------------------
# too low pressure → control instability
fail_lowP = P < 3e3

# too high pressure → thermal stiffening / loss of sensitivity
fail_highP = P > 3e6

# ----------------------------
# PLOT
# ----------------------------
plt.figure(figsize=(10, 7))

# stable operating band
plt.fill_between(
    P[valid],
    d_low_stable[valid] * 1e6,
    d_high_stable[valid] * 1e6,
    color="green",
    alpha=0.6,
    label="Practical ESC operating corridor"
)

# equilibrium curve (what system naturally wants)
plt.plot(
    P,
    d_eq * 1e6,
    color="blue",
    linewidth=2,
    label="Equilibrium gap (natural operating point)"
)

# boundaries
plt.plot(P, d_low_stable * 1e6, "r--", label="Lower stability limit")
plt.plot(P, d_high_stable * 1e6, "purple", linestyle="--", label="Upper stability limit")

# failure zones
plt.axvspan(P_min, 3e3, color="gray", alpha=0.2, label="Low-pressure instability")
plt.axvspan(3e6, P_max, color="orange", alpha=0.15, label="High-pressure stiffness limit")

# ----------------------------
# AXES
# ----------------------------
plt.xscale("log")
plt.yscale("log")

plt.xlabel("Pressure (Pa)")
plt.ylabel("Gap (µm)")
plt.title("Realistic Human-Operable ESC Equilibrium Envelope")

plt.grid(True, which="both", alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()