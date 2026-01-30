import random

# ==============================
# CONFIG
# ==============================
N = 2000          # total samples
WINDOW = 50       # local window size
STEP = 5          # sliding step
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
# MAP FLIPS TO INDIVIDUAL CALLS
# ==============================
flip_per_call = [0]*N  # 0=no flip, 1=flip

for fi in flip_indices:
    # Assign flip to all calls in the window
    for i in range(fi, min(fi+WINDOW, N)):
        flip_per_call[i] = 1

# ==============================
# COMPUTE FLIP PROBABILITY PER CALL
# ==============================
total_flips = sum(flip_per_call)
flip_probability_per_call = total_flips / N

# ==============================
# FLIP INTERVALS PER CALL
# ==============================
call_indices = [i for i,v in enumerate(flip_per_call) if v==1]
call_intervals = [j-i for i,j in zip(call_indices[:-1], call_indices[1:])]

# ==============================
# REPORT
# ==============================
print("Total RNG calls        :", N)
print("Calls inside flip windows:", total_flips)
print("Flip probability per call:", f"{flip_probability_per_call:.3f}")
print("Mean call interval between flips:", f"{sum(call_intervals)/len(call_intervals):.2f}" if call_intervals else "N/A")
print("First 20 call intervals between flips:", call_intervals[:20])