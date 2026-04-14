import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# DOMAIN
# ============================================================
lambda_0 = 68e-9
P0 = 101325
Kn_target = 0.05

d_min = 1e-6
d_max = 50e-6

P_min = 2e3
P_max = 5e6

P = np.logspace(np.log10(P_min), np.log10(P_max), 700)

# ============================================================
# GAS PROPERTIES
# ============================================================
gas = {
    "He": {"thermal": 1.0, "control": 1.0, "noise": 0.15},
    "Ar": {"thermal": 0.28, "control": 0.65, "noise": 0.45}
}

# ============================================================
# MODEL
# ============================================================
def esc_score(g):
    lambda_g = lambda_0 * (P0 / P)
    d_eq = lambda_g / Kn_target

    # --- HARD FEASIBILITY ---
    geom = (d_eq > d_min) & (d_eq < d_max)
    electro = g["control"] / (d_eq + 1e-9) > 1.0
    thermal = g["thermal"] / (d_eq + 1e-9) > 1e3
    leak = (P * d_eq) / (1e5 * d_max) < 1.0

    feasible = geom & electro & thermal & leak

    # --- STABILITY ---
    stability = np.clip(
        1.0 - np.abs(d_eq - 20e-6) / (20e-6),
        0, 1
    )

    # --- CONTROL QUALITY ---
    control = g["control"] / (1 + g["noise"] * P / P_max)

    # --- YIELD FACTOR ---
    yield_factor = np.exp(-g["noise"] * (P / P_max))

    # --- FINAL SCORE ---
    score = feasible.astype(float) * stability * control * yield_factor

    return d_eq, score

# ============================================================
# RUN
# ============================================================
d_he, score_he = esc_score(gas["He"])
d_ar, score_ar = esc_score(gas["Ar"])

# ============================================================
# PLOT
# ============================================================
plt.figure(figsize=(10, 7))

# Helium
plt.scatter(P, d_he*1e6, c=score_he, s=5, cmap="Blues")

# Argon
plt.scatter(P, d_ar*1e6, c=score_ar, s=5, cmap="Oranges")

# curves
plt.plot(P, d_he*1e6, color="blue", linewidth=1, label="He")
plt.plot(P, d_ar*1e6, color="orange", linewidth=1, label="Ar")

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Pressure (Pa)")
plt.ylabel("Gap (µm)")
plt.title("ESC Manufacturing Qualification Score (He vs Ar)")

plt.colorbar(label="Score (0–1)")

plt.grid(True, which="both", alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()