import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Physical parameters
# -----------------------------

P0 = 3.0          # baseline chamber pressure (MPa)
sigma_c = 3000     # material strength (MPa)
d0 = 0.1        # mm reference defect scale

alpha = 0.35      # pressure scaling exponent
beta = 0.28       # wall thickness scaling exponent
k = 2.2           # Weibull fragility exponent

# -----------------------------
# Physical scaling laws
# -----------------------------

def pressure(M):
    return P0 * (M ** alpha)

def radius(M):
    return M ** (1/3)

def thickness(M):
    # weaker-than-geometric scaling (manufacturing constraint)
    return 0.01 * (M ** beta)

def stress(M):
    P = pressure(M)
    R = radius(M)
    t = thickness(M)
    return P * R / t   # thin-wall scaling

def max_defect(M):
    # extreme value scaling (log growth)
    return d0 * np.log(M + 1)

# -----------------------------
# Failure probability model
# -----------------------------

def failure_probability(M):
    sigma = stress(M)
    d = max_defect(M)

    hazard = (sigma / sigma_c) * (d / d0)

    return 1 - np.exp(-(hazard ** k))

# -----------------------------
# Sweep rocket mass
# -----------------------------

masses = np.logspace(-1, 2, 200)  # 0.1 kg to 100 kg
fail_probs = np.array([failure_probability(M) for M in masses])

# -----------------------------
# Plot
# -----------------------------

plt.figure()
plt.semilogx(masses, fail_probs)
plt.xlabel("Rocket Mass (kg)")
plt.ylabel("Failure Probability")
plt.title("Allometric Rocket Mass vs Failure Probability (Physics-Based Model)")
plt.grid(True)
plt.show()

# -----------------------------
# Sample outputs
# -----------------------------

for M in [0.2, 1, 5, 10, 25, 50, 100]:
    print(f"{M:>5} kg -> failure probability = {failure_probability(M):.3f}")