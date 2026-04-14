import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# ARGON + SYSTEM PARAMETERS
# ----------------------------
lambda_0 = 68e-9      # reference mean free path
P0 = 101325           # atmospheric pressure
k_Ar = 0.018          # thermal coefficient proxy
b = 2.0               # coupling factor

Kn_min = 0.02
Kn_max = 0.08

G_min = 1e5           # minimum thermal conductance threshold

# ----------------------------
# PRESSURE DOMAIN
# ----------------------------
P = np.logspace(3, 7, 800).astype(float)

# ----------------------------
# MEAN FREE PATH
# ----------------------------
lambda_g = lambda_0 * (P0 / P)
lambda_g = np.asarray(lambda_g, dtype=float)

# ----------------------------
# KNUDSEN-BASED GAP LIMITS
# ----------------------------
d_kn_low = lambda_g / Kn_max
d_kn_high = lambda_g / Kn_min

# ----------------------------
# THERMAL CONSTRAINT (CLEAN + SAFE)
# ----------------------------
d_thermal_raw = (k_Ar / G_min) - b * lambda_g

# enforce physical validity (no negative gaps)
d_thermal = np.where(d_thermal_raw > 0, d_thermal_raw, np.nan)

# ----------------------------
# MANUFACTURING LIMITS
# ----------------------------
d_min_mfg = 1e-6
d_max_mfg = 30e-6

d_min_arr = np.full_like(P, d_min_mfg)
d_max_arr = np.full_like(P, d_max_mfg)

# ----------------------------
# BUILD CLOSED ENVELOPE
# ----------------------------
d_lower = np.maximum.reduce([
    d_kn_low,
    d_thermal,
    d_min_arr
])

d_upper = np.minimum.reduce([
    d_kn_high,
    d_max_arr
])

# ----------------------------
# VALID REGION MASK
# ----------------------------
valid = np.isfinite(d_lower) & np.isfinite(d_upper) & (d_upper > d_lower)

# ----------------------------
# PLOT
# ----------------------------
plt.figure(figsize=(10, 7))

# feasible closed envelope
plt.fill_between(
    P[valid],
    d_lower[valid] * 1e6,
    d_upper[valid] * 1e6,
    color="green",
    alpha=0.55,
    label="Manufacturing-Realistic ESC Envelope"
)

# ----------------------------
# BOUNDARY CURVES
# ----------------------------
plt.plot(P, d_kn_low * 1e6, color="blue", label="Kn upper limit")
plt.plot(P, d_kn_high * 1e6, color="purple", linestyle="--", label="Kn lower limit")

plt.plot(P, d_thermal * 1e6, color="red", label="Thermal limit (clipped)")

plt.axhline(d_min_mfg * 1e6, color="black", linestyle="--", label="Min manufacturable gap")
plt.axhline(d_max_mfg * 1e6, color="gray", linestyle="--", label="Max manufacturable gap")

# ----------------------------
# AXES + FORMATTING
# ----------------------------
plt.xscale("log")
plt.yscale("log")

plt.xlabel("Pressure (Pa)")
plt.ylabel("Gap (µm)")
plt.title("Closed Manufacturing-Realistic ESC Operating Envelope (Stable Model)")

plt.grid(True, which="both", alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()