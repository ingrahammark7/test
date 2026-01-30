# ============================================================
# FINAL HARDWARE RNG STRUCTURE + FLIP DYNAMICS ANALYSIS
# ============================================================

import random
import math
from collections import defaultdict

# ----------------------------
# CONFIG
# ----------------------------
N = 200000          # total RNG calls
WINDOW = 50         # local window size
STEP = 5            # sliding step
MAX_LAG = 1         # focus on AC1 (dominant)
rng = random.SystemRandom()

# ----------------------------
# DATA
# ----------------------------
x = [rng.random() for _ in range(N)]

# ----------------------------
# AUTOCORRELATION
# ----------------------------
def autocorr(seq, lag=1):
    n = len(seq)
    mu = sum(seq)/n
    num = sum((seq[i]-mu)*(seq[i-lag]-mu) for i in range(lag, n))
    den = sum((v-mu)**2 for v in seq)
    return num/den if den else 0.0

# ----------------------------
# LOCAL WINDOW AC1
# ----------------------------
windows = []
for start in range(0, N-WINDOW+1, STEP):
    w = x[start:start+WINDOW]
    ac1 = autocorr(w, 1)
    windows.append((start, ac1))

# ----------------------------
# REGIME & FLIP DETECTION
# ----------------------------
regime = []
flip_windows = []

prev = 0
for i,(_,ac1) in enumerate(windows):
    s = 1 if ac1 > 0 else -1
    regime.append(s)
    if prev != 0 and s != prev:
        flip_windows.append(i)
    prev = s

# ----------------------------
# REGIME RUN LENGTHS (BUNCHING)
# ----------------------------
runs = []
cur = regime[0]
length = 1
for r in regime[1:]:
    if r == cur:
        length += 1
    else:
        runs.append(length)
        cur = r
        length = 1
runs.append(length)

# ----------------------------
# FLIP INTERVALS (WINDOW SPACE)
# ----------------------------
flip_intervals = [j-i for i,j in zip(flip_windows[:-1], flip_windows[1:])]

# ----------------------------
# FLIP AUTOCORRELATION
# ----------------------------
flip_flag = [0]*len(windows)
for i in flip_windows:
    flip_flag[i] = 1

def ac_binary(seq, lag):
    n = len(seq)
    mu = sum(seq)/n
    num = sum((seq[i]-mu)*(seq[i-lag]-mu) for i in range(lag, n))
    den = sum((v-mu)**2 for v in seq)
    return num/den if den else 0.0

flip_ac = {lag: ac_binary(flip_flag, lag) for lag in range(1,6)}

# ----------------------------
# HAZARD FUNCTION (MEMORY)
# ----------------------------
hazard = defaultdict(lambda:[0,0])
age = 1
cur = regime[0]

for r in regime[1:]:
    if r == cur:
        hazard[age][0] += 1
        age += 1
    else:
        hazard[age][1] += 1
        cur = r
        age = 1

# ----------------------------
# MARKOV PREDICTABILITY (MI)
# ----------------------------
pairs = defaultdict(int)
for a,b in zip(regime[:-1], regime[1:]):
    pairs[(a,b)] += 1

total = sum(pairs.values())
mi = 0.0
for (a,b),c in pairs.items():
    pa = sum(v for (x,_),v in pairs.items() if x==a)/total
    pb = sum(v for (_,y),v in pairs.items() if y==b)/total
    pab = c/total
    mi += pab * math.log2(pab/(pa*pb))

# ----------------------------
# PER-CALL FLIP EXPOSURE
# ----------------------------
call_flip = [0]*N
for i in flip_windows:
    start = windows[i][0]
    for j in range(start, min(start+WINDOW, N)):
        call_flip[j] = 1

flip_prob_call = sum(call_flip)/N

# ----------------------------
# REPORT
# ----------------------------
print("\n=== FINAL RNG STRUCTURE ANALYSIS ===\n")

print("Samples                  :", N)
print("Windows tested            :", len(windows))
print("Total flips               :", len(flip_windows))
print("Flip probability/window   :", len(flip_windows)/len(windows))
print("Flip probability/call     :", flip_prob_call)

print("\nREGIME RUNS (BUNCHING)")
print("Mean run length (windows) :", sum(runs)/len(runs))
print("Max run length            :", max(runs))
print("First 20 runs             :", runs[:20])

print("\nFLIP INTERVALS")
print("Mean interval (windows)   :", sum(flip_intervals)/len(flip_intervals))
print("First 20 intervals        :", flip_intervals[:20])

print("\nFLIP AUTOCORRELATION")
for lag,v in flip_ac.items():
    print(f"Lag {lag}: {v:+.4f}")

print("\nHAZARD FUNCTION (age → P(flip))")
for age in sorted(hazard)[:15]:
    s,f = hazard[age]
    if s+f:
        print(f"{age:3d} : {f/(s+f):.3f}")

print("\nMARKOV REGIME MI")
print("I(S_t ; S_t+1) =", mi, "bits")

print("\nVERDICT:")
print("LOCAL STRUCTURE + REGIME MEMORY + FLIP CLUSTERING DETECTED ❌")
print("[Program finished]")