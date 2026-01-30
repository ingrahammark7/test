import random
import math
import time

# ==============================
# CONFIG
# ==============================
N = 500
WINDOW = 5
MAX_LAG = 1

rng = random.SystemRandom()

# ==============================
# STORAGE
# ==============================
x = []
phi_hist = []
ac1_hist = []

# ==============================
# STATS
# ==============================
def autocorr(seq, lag):
    n = len(seq)
    if n <= lag:
        return 0.0
    mu = sum(seq) / n
    num = sum((seq[i] - mu) * (seq[i-lag] - mu) for i in range(lag, n))
    den = sum((v - mu) ** 2 for v in seq)
    return num / den if den != 0 else 0.0

def estimate_phi(seq):
    """Least-squares AR(1) estimator"""
    if len(seq) < 2:
        return 0.0
    num = sum(seq[i] * seq[i-1] for i in range(1, len(seq)))
    den = sum(seq[i-1] ** 2 for i in range(1, len(seq)))
    return num / den if den != 0 else 0.0

# ==============================
# MAIN LOOP
# ==============================
print("\n=== AR(1) FALSIFICATION TEST ===\n")

for i in range(N):
    x.append(rng.random())

    if len(x) >= WINDOW:
        w = x[-WINDOW:]

        ac1 = autocorr(w, 1)
        phi = estimate_phi(w)

        ac1_hist.append(ac1)
        phi_hist.append(phi)

        if i % 5_000 == 0:
            print(
                f"[{i:06d}] "
                f"AC1={ac1:+.5f} "
                f"phî={phi:+.5f}"
            )

        # OPTIONAL: break alignment artifacts
        if i % 997 == 0:
            time.sleep(0.0005)

# ==============================
# SUMMARY
# ==============================
def stats(v):
    mu = sum(v) / len(v)
    var = sum((x - mu) ** 2 for x in v) / len(v)
    return mu, math.sqrt(var)

ac_mu, ac_sd = stats(ac1_hist)
phi_mu, phi_sd = stats(phi_hist)

print("\n=== SUMMARY ===")
print(f"AC1 mean ± sd  : {ac_mu:+.6f} ± {ac_sd:.6f}")
print(f"phî mean ± sd : {phi_mu:+.6f} ± {phi_sd:.6f}")