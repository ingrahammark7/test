import random
import matplotlib.pyplot as plt

# ==============================
# CONFIG
# ==============================
N = 2000           # total samples
WINDOW = 50        # local window size
STEP = 5           # slide step
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
flip_series = []
prev_sign = 0
for start, ac1 in window_ac1:
    sign = 1 if ac1 > 0 else -1 if ac1 < 0 else 0
    flip_series.append(sign)
    if prev_sign != 0 and sign != prev_sign:
        flip_indices.append(start)
    prev_sign = sign

# ==============================
# FLIP AUTOCORRELATION
# ==============================
# Convert flip series to 0 for no-flip, 1 for flip event
flip_events = [1 if (i in flip_indices) else 0 for i, _ in enumerate(window_ac1)]

# Lag-1 autocorrelation of flip events
if len(flip_events) > 1:
    mu = sum(flip_events)/len(flip_events)
    num = sum((flip_events[i]-mu)*(flip_events[i-1]-mu) for i in range(1,len(flip_events)))
    den = sum((v-mu)**2 for v in flip_events)
    flip_ac1 = num/den if den != 0 else 0.0
else:
    flip_ac1 = 0.0

# ==============================
# FLIP INTERVALS
# ==============================
flip_periods = [j-i for i,j in zip(flip_indices[:-1], flip_indices[1:])]

# ==============================
# REPORT
# ==============================
print("Total windows        :", len(window_ac1))
print("Total flips          :", len(flip_indices))
print("Flip lag-1 autocorr  :", f"{flip_ac1:.3f}")
print("Mean flip interval   :", f"{sum(flip_periods)/len(flip_periods):.2f}" if flip_periods else "N/A")
print("First 20 flip periods:", flip_periods[:20])

# ==============================
# PLOTS
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

plt.figure(figsize=(8,4))
plt.hist(flip_periods, bins=20, color='orange', edgecolor='black')
plt.xlabel("Windows between flips")
plt.ylabel("Frequency")
plt.title("Histogram of Flip Intervals")
plt.show()