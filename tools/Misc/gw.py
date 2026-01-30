import random
import matplotlib.pyplot as plt

# ==============================
# CONFIG
# ==============================
N = 2000           # total samples
WINDOW = 50        # local window size
STEP = 5           # sliding step
MAX_LAG = 1        # focus on AC1
rng = random.SystemRandom()

# ==============================
# GENERATE DATA
# ==============================
x = [rng.random() for _ in range(N)]

# ==============================
# AUTOCORRELATION FUNCTION
# ==============================
def autocorr(seq, lag=1):
    n = len(seq)
    mu = sum(seq)/n
    num = sum((seq[i]-mu)*(seq[i-lag]-mu) for i in range(lag, n))
    den = sum((v-mu)**2 for v in seq)
    return num/den if den != 0 else 0.0

# ==============================
# COMPUTE LOCAL AC1
# ==============================
window_ac1 = []
for start in range(0, N-WINDOW+1, STEP):
    w = x[start:start+WINDOW]
    ac1 = autocorr(w, lag=1)
    window_ac1.append((start, ac1))

# ==============================
# DETECT FLIPS
# ==============================
flip_indices = []
prev_sign = 0
for start, ac1 in window_ac1:
    sign = 1 if ac1 > 0 else -1 if ac1 < 0 else 0
    if prev_sign != 0 and sign != prev_sign:
        flip_indices.append(start)
    prev_sign = sign

# ==============================
# FLIP PERIODS
# ==============================
flip_periods = [j-i for i,j in zip(flip_indices[:-1], flip_indices[1:])]
flip_probability = len(flip_indices) / len(window_ac1)

# ==============================
# REPORT
# ==============================
print("Total windows      :", len(window_ac1))
print("Total flips        :", len(flip_indices))
print("Flip probability   :", f"{flip_probability:.3f} per window")
print("Flip periods       :", flip_periods[:20], "...")
print("Average flip period:", f"{sum(flip_periods)/len(flip_periods):.2f} windows" if flip_periods else "N/A")

# ==============================
# PLOT AC1 AND FLIPS
# ==============================
plt.figure(figsize=(12,4))
indices, ac_vals = zip(*window_ac1)
plt.plot(indices, ac_vals, label="AC1 per window")
for f in flip_indices:
    plt.axvline(f, color='red', linestyle='--', alpha=0.6)
plt.xlabel("Sample index")
plt.ylabel("AC1")
plt.title("Local AC1 with Detected Flips")
plt.legend()
plt.show()