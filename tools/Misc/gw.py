import random
import math

# ==============================
# CONFIG
# ==============================
N = 200_0
WINDOW = 200          # local window size
STEP = 5              # run every 5 samples
MAX_LAG = 8
BINS = 16

rng = random.SystemRandom()

# ==============================
# DATA
# ==============================
x = [rng.random() for _ in range(N)]

# ==============================
# CORE METRICS
# ==============================
def autocorr(seq, lag):
    n = len(seq)
    mu = sum(seq) / n
    num = sum((seq[i]-mu)*(seq[i-lag]-mu) for i in range(lag, n))
    den = sum((v-mu)**2 for v in seq)
    return num / den if den != 0 else 0.0

def mutual_info(seq, lag, bins):
    n = len(seq) - lag
    h = [[0]*bins for _ in range(bins)]
    for i in range(n):
        a = int(seq[i]*bins)
        b = int(seq[i+lag]*bins)
        h[a][b] += 1

    total = n
    px = [sum(row)/total for row in h]
    py = [sum(h[r][c] for r in range(bins))/total for c in range(bins)]

    mi = 0.0
    for i in range(bins):
        for j in range(bins):
            pxy = h[i][j] / total
            if pxy > 0:
                mi += pxy * math.log2(pxy / (px[i]*py[j]))
    return mi

def runs_z(seq):
    # up/down runs test (correct for continuous data)
    s = []
    for i in range(1, len(seq)):
        if seq[i] > seq[i-1]:
            s.append(1)
        elif seq[i] < seq[i-1]:
            s.append(0)

    if len(s) < 10:
        return 0.0

    runs = 1
    for i in range(1, len(s)):
        if s[i] != s[i-1]:
            runs += 1

    n1 = sum(s)
    n0 = len(s) - n1
    if n1 == 0 or n0 == 0:
        return 0.0

    exp = (2*n1*n0)/(n1+n0) + 1
    var = (2*n1*n0*(2*n1*n0 - n1 - n0)) / (((n1+n0)**2)*(n1+n0-1))
    return (runs - exp) / math.sqrt(var)

# ==============================
# GLOBAL TEST
# ==============================
global_ac = max(abs(autocorr(x, l)) for l in range(1, MAX_LAG+1))
global_mi = max(mutual_info(x, l, BINS) for l in range(1, MAX_LAG+1))
global_runs = runs_z(x)

# ==============================
# LOCAL WINDOW SCAN
# ==============================
violations = []

for i in range(WINDOW, N, STEP):
    w = x[i-WINDOW:i]

    ac = max(abs(autocorr(w, l)) for l in range(1, MAX_LAG+1))
    mi = max(mutual_info(w, l, BINS) for l in range(1, MAX_LAG+1))
    rz = abs(runs_z(w))

    if ac > 4/math.sqrt(WINDOW) or mi > 0.02 or rz > 4:
        violations.append((i, ac, mi, rz))

# ==============================
# REPORT
# ==============================
print("\n=== FINAL RNG STRUCTURE TEST ===\n")

print("GLOBAL METRICS")
print(f"Max |AC|      : {global_ac:.6e}")
print(f"Max MI        : {global_mi:.6e} bits")
print(f"Runs Z        : {global_runs:+.3f}")

print("\nLOCAL WINDOW SCAN")
print(f"Windows tested : {(N-WINDOW)//STEP}")
print(f"Violations     : {len(violations)}")

if violations:
    print("\nFirst 10 violations:")
    for v in violations[:10]:
        print(
            f"Index {v[0]:6d} | "
            f"AC={v[1]:.3e} MI={v[2]:.3e} RZ={v[3]:.2f}"
        )

print("\nVERDICT:")
if global_ac < 5/math.sqrt(N) and global_mi < 0.01 and abs(global_runs) < 5 and len(violations) == 0:
    print("NO DETECTABLE STRUCTURE ✅")
else:
    print("LOCAL OR GLOBAL STRUCTURE DETECTED ❌")