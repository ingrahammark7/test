import random
from collections import deque

# ==============================
# CONFIG
# ==============================
N = 2000             # total samples (adjust for testing)
WINDOW = 50          # local window size
STEP = 5             # compute every 5 samples
MAX_LAG = 4          # compute autocorr up to lag 4

rng = random.SystemRandom()

# ==============================
# DATA
# ==============================
x = [rng.random() for _ in range(N)]

# ==============================
# AUTOCORRELATION FUNCTION
# ==============================
def autocorr(seq, lag):
    n = len(seq)
    mu = sum(seq)/n
    num = sum((seq[i]-mu)*(seq[i-lag]-mu) for i in range(lag, n))
    den = sum((v-mu)**2 for v in seq)
    return num/den if den != 0 else 0.0

# ==============================
# LOCAL WINDOW AC
# ==============================
window_ac = []

for start in range(0, N-WINDOW+1, STEP):
    w = x[start:start+WINDOW]
    ac_lags = [autocorr(w, lag) for lag in range(1, MAX_LAG+1)]
    window_ac.append((start, ac_lags))

# ==============================
# REPORT
# ==============================
print("Index | " + " | ".join([f"AC{l}" for l in range(1, MAX_LAG+1)]))
print("-"*50)
for start, ac in window_ac[:50]:  # show first 50 windows for brevity
    ac_str = " | ".join([f"{v:+.3f}" for v in ac])
    print(f"{start:5d} | {ac_str}")

# ==============================
# SIMPLE FLIP DETECTION (optional)
# ==============================
# Check if AC1 changes sign every ~10 calls
flip_indices = []
prev_sign = 0
for start, ac in window_ac:
    sign = 1 if ac[0] > 0 else -1 if ac[0] < 0 else 0
    if prev_sign != 0 and sign != prev_sign:
        flip_indices.append(start)
    prev_sign = sign

print("\nDetected AC1 flips at windows starting at indices (first 20):")
print(flip_indices[:20])
print(f"Total flips detected: {len(flip_indices)}")