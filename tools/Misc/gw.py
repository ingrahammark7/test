import random
import math

# ==============================
# CONFIG
# ==============================
N = 200_000
WINDOW = 500
STEP = 500            # NO OVERLAP
MAX_LAG = 8
BINS = 16

rng = random.SystemRandom()
x = [rng.random() for _ in range(N)]

# ==============================
# STAT FUNCTIONS
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
        h[int(seq[i]*bins)][int(seq[i+lag]*bins)] += 1

    total = n
    px = [sum(r)/total for r in h]
    py = [sum(h[r][c] for r in range(bins))/total for c in range(bins)]

    mi = 0.0
    for i in range(bins):
        for j in range(bins):
            pxy = h[i][j]/total
            if pxy > 0:
                mi += pxy * math.log2(pxy/(px[i]*py[j]))
    return mi

def mi_bias(bins, n):
    return ((bins-1)**2)/(2*n*math.log(2))

# ==============================
# GLOBAL TEST
# ==============================
global_ac = max(abs(autocorr(x, l)) for l in range(1, MAX_LAG+1))
global_mi = max(mutual_info(x, l, BINS) - mi_bias(BINS, N) for l in range(1, MAX_LAG+1))

# ==============================
# LOCAL WINDOWS
# ==============================
violations = []

for i in range(0, N-WINDOW, STEP):
    w = x[i:i+WINDOW]

    ac = max(abs(autocorr(w, l)) for l in range(1, MAX_LAG+1))
    mi = max(mutual_info(w, l, BINS) - mi_bias(BINS, WINDOW) for l in range(1, MAX_LAG+1))

    ac_thresh = math.sqrt(2*math.log(MAX_LAG)/WINDOW)
    mi_thresh = 0.05   # bias-corrected, empirical safe bound

    if ac > ac_thresh or mi > mi_thresh:
        violations.append((i, ac, mi))

# ==============================
# REPORT
# ==============================
print("\n=== FINAL RNG STRUCTURE TEST (CORRECTED) ===\n")
print(f"Global max |AC| : {global_ac:.4e}")
print(f"Global max MI   : {global_mi:.4e}")
print(f"Local windows   : {len(range(0, N-WINDOW, STEP))}")
print(f"Violations      : {len(violations)}")

if violations:
    print("First violations:")
    for v in violations[:5]:
        print(f"Index {v[0]:6d} AC={v[1]:.3e} MI={v[2]:.3e}")
else:
    print("No local violations detected")

print("\nVERDICT:",
      "STRUCTURE DETECTED ❌" if violations or global_mi > 0.02 else
      "NO DETECTABLE STRUCTURE ✅")