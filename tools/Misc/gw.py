import numpy as np
import matplotlib.pyplot as plt

# Time axis (1980–2026)
t = np.linspace(0, 46, 600)  # years since 1980
year = 1980 + t

# -----------------------------
# 1. Transistor growth (Moore)
# -----------------------------
N0 = 1e4
N = N0 * 2 ** (t / 2)

# -----------------------------
# 2. Frequency (saturation + thermal wall)
# -----------------------------
f_max = 4.5
alpha = 0.25
beta = 0.08

f = f_max * (1 - np.exp(-alpha * t)) * np.exp(-beta * np.clip(t - 25, 0, None))

# -----------------------------
# 3. IPC (log growth)
# -----------------------------
IPC0 = 1.0
a = 0.5
IPC = IPC0 * (1 + a * np.log1p(t))

# -----------------------------
# 4. Memory/cache efficiency
# -----------------------------
mu = 0.10
nu = 0.12
eta = 1 / (1 + np.exp(-(nu - mu) * t))

# -----------------------------
# 5. Power/thermal constraint
# -----------------------------
kappa = 0.03
rho = 0.12
power_penalty = 1 / (1 + kappa * np.exp(rho * np.clip(t - 25, 0, None)))

# =========================================================
# 6. CHIPLET ERA (post-2020 system decomposition)
# =========================================================

t_chiplet_start = 40  # ~2020

chiplet_scale = np.ones_like(t)

# number of effective chiplets grows after 2020
chiplets = np.ones_like(t)

chiplet_growth_rate = 0.18  # system-level scaling (slow vs Moore)

chiplets = np.where(
    t < t_chiplet_start,
    1,
    1 + np.exp(chiplet_growth_rate * (t - t_chiplet_start)) - 1
)

# communication overhead between chiplets (interconnect penalty)
# grows with chiplet count (nonlinear bottleneck)
comm_penalty = 1 / (1 + 0.15 * (chiplets - 1))

# =========================================================
# 7. 3D STACKING EFFECT (post-2020 boost + thermal tradeoff)
# =========================================================

# stacking gives memory + bandwidth boost
stack_gain_rate = 0.25

stacking_gain = np.where(
    t < t_chiplet_start,
    1,
    1 + 0.6 * (1 - np.exp(-stack_gain_rate * (t - t_chiplet_start)))
)

# but introduces thermal density penalty
thermal_stack_penalty = np.where(
    t < t_chiplet_start,
    1,
    np.exp(-0.03 * (t - t_chiplet_start))
)

# combined 3D factor
stack_factor = stacking_gain * thermal_stack_penalty

# =========================================================
# 8. Effective performance model
# =========================================================

P = (
    N
    * f
    * IPC
    * eta
    * power_penalty
    * chiplets
    * comm_penalty
    * stack_factor
)

# normalize to early baseline (~1985)
P_norm = P / P[np.where(t >= 5)[0][0]]

# -----------------------------
# Plot
# -----------------------------
plt.figure()

plt.plot(year, P_norm, label="Extended CPU performance (chiplet + 3D era)")
plt.plot(year, N / N[np.where(t >= 5)[0][0]],
         linestyle="--", label="Transistor growth (Moore baseline)")

plt.axvline(2020, linestyle=":", label="Chiplet/3D transition (~2020)")

plt.xlabel("Year")
plt.ylabel("Relative performance")
plt.title("CPU Performance Model with Chiplets + 3D Stacking")
plt.legend()

plt.show()