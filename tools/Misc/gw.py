import random
import math

# ==============================
# CONFIG
# ==============================
N = 200_000
MAX_LAG = 32
BINS = 32

rng = random.SystemRandom()

# ==============================
# DATA
# ==============================
x = [rng.random() for _ in range(N)]

# ==============================
# LINEAR AUTOCORRELATION
# ==============================
def autocorr(seq, lag):
    n = len(seq)
    mu = sum(seq) / n
    num = sum((seq[i]-mu)*(seq[i-lag]-mu) for i in range(lag, n))
    den = sum((v-mu)**2 for v in seq)
    return num / den if den != 0 else 0.0

ac = [autocorr(x, lag) for lag in range(1, MAX_LAG+1)]

# ==============================
# MUTUAL INFORMATION (NONLINEAR)
# ==============================
def mutual_info_lag(seq, lag, bins):
    n = len(seq) - lag
    h = [[0]*bins for _ in range(bins)]
    for i in range(n):
        a = int(seq[i]*bins) % bins
        b = int(seq[i+lag]*bins) % bins
        h[a][b] += 1

    total = n
    px = [sum(row) / total for row in h]
    py = [sum(h[r][c] for r in range(bins)) / total for c in range(bins)]

    mi = 0.0
    for i in range(bins):
        for j in range(bins):
            pxy = h[i][j] / total
            if pxy > 0 and px[i] > 0 and py[j] > 0:
                mi += pxy * math.log2(pxy / (px[i]*py[j]))
    return mi

mi = [mutual_info_lag(x, lag, BINS) for lag in range(1, MAX_LAG+1)]

# ==============================
# RUNS TEST (SIGN DEPENDENCE)
# ==============================
median = sorted(x)[len(x)//2]
signs = [1 if v > median else 0 for v in x]

runs = 1
for i in range(1, len(signs)):
    if signs[i] != signs[i-1]:
        runs += 1

expected_runs = (2*len(x)-1)/3
runs_z = (runs - expected_runs) / math.sqrt((16*len(x)-29)/90)

# ==============================
# VERDICT
# ==============================
ac_max = max(abs(v) for v in ac)
mi_max = max(mi)

print("\n=== FINAL RNG DEPENDENCE TEST ===\n")
print(f"Samples              : {N}")
print(f"Max |autocorr| (lags) : {ac_max:.6e}")
print(f"Max mutual info       : {mi_max:.6e} bits")
print(f"Runs test z-score     : {runs_z:+.3f}")

# Thresholds derived from IID asymptotics
FAIL = False
if ac_max > 5 / math.sqrt(N):
    FAIL = True
if mi_max > 0.01:
    FAIL = True
if abs(runs_z) > 5:
    FAIL = True

print("\nVERDICT:", "DEPENDENCE DETECTED ❌" if FAIL else "NO DEPENDENCE DETECTED ✅")