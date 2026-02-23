import math

# ---------- INPUT PARAMETERS ----------

H = 800000          # magnetizing field strength (A/m)
mu_r = 500          # steel relative permeability
gap = 0.002         # air gap in meters (2 mm)
steel_length = 0.05 # magnetic path length in steel (5 cm)
area = 0.01         # contact area m²
B_sat = 1.6         # steel saturation limit (Tesla)

# ---------- CONSTANT ----------
mu0 = 4 * math.pi * 1e-7

# ---------- STARTING (IDEAL) FIELD ----------
B_initial = mu0 * mu_r * H

# starting force before losses
F_initial = (B_initial**2 * area) / (2 * mu0)

# ---------- FIELD CALCULATION ----------
B = (mu0 * mu_r * H) / (1 + (gap * mu_r / steel_length))

# apply saturation limit
if B > B_sat:
    B = B_sat

# ---------- FORCE ----------
F = (B**2 * area) / (2 * mu0)

# ---------- OUTPUT ----------
print("Starting ideal field B:", round(B_initial,3), "T")
print("Starting ideal force:", round(F_initial,1), "N")
print("Starting ideal force:", round(F_initial/9.81,1), "kgf")
print()

print("Effective field B:", round(B,3), "T")
print("Force:", round(F,1), "N")
print("Equivalent mass:", round(F/9.81,1), "kg")