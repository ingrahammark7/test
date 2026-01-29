import random
import math
from collections import deque

# ==============================
# CONFIG
# ==============================
N = 200
WINDOWS = [4]       # rolling windows for stats
REGIME_WIN = 4      # window for regime detection
AR_REGIMES = ['WARMUP','LOW-ENT','META-AR','STABLE']

rng = random.SystemRandom()

# ==============================
# STATE
# ==============================
x_hist = []
entropy_hist = []
ac_hist = []
regime_hist = []

ar_coeffs = {r: {'ar1':0.0, 'ar2':[0.0,0.0]} for r in AR_REGIMES}

var_hist = []
kurt_hist = []
mutual_info_hist = []
adv_err_hist = []

# rolling windows (deque for efficiency)
WINDOW_MAX = max(WINDOWS)
x_window = deque(maxlen=WINDOW_MAX)
ac_window = deque(maxlen=REGIME_WIN)
ent_window = deque(maxlen=REGIME_WIN)

# ==============================
# UTILITIES
# ==============================
def shannon_entropy(seq, bins=16):
    if len(seq)<2: return 0.0
    counts = [0]*bins
    for v in seq:
        counts[int(v*bins)%bins] += 1
    total = sum(counts)
    ent = 0.0
    for c in counts:
        if c>0:
            p = c/total
            ent -= p * math.log2(p)
    return ent

def autocorr(seq, lag=1):
    if len(seq)<=lag: return 0.0
    mu = sum(seq)/len(seq)
    num = sum((seq[i]-mu)*(seq[i-lag]-mu) for i in range(lag,len(seq)))
    den = sum((v-mu)**2 for v in seq)
    return num/den if den!=0 else 0.0

def compute_ac_lags(seq, max_lag=4):
    return [autocorr(seq, lag) for lag in range(1,max_lag+1)]

def rolling_variance(seq):
    if len(seq)<2: return 0.0
    mu = sum(seq)/len(seq)
    return sum((x-mu)**2 for x in seq)/len(seq)

def rolling_kurtosis(seq):
    if len(seq)<2: return 0.0
    mu = sum(seq)/len(seq)
    var = rolling_variance(seq)
    if var==0: return 0.0
    return sum((x-mu)**4 for x in seq)/(len(seq)*var**2)

def mutual_info(seq):
    if len(seq)<2: return 0.0
    mid = len(seq)//2
    x = seq[:mid]
    y = seq[mid:]
    bins = 8
    hist2d = [[0]*bins for _ in range(bins)]
    for xi, yi in zip(x, y):
        hist2d[int(xi*bins)%bins][int(yi*bins)%bins] += 1
    total = sum(sum(r) for r in hist2d)
    mi = 0.0
    for i in range(bins):
        for j in range(bins):
            pxy = hist2d[i][j]/total if total>0 else 0
            if pxy>0:
                px = sum(hist2d[i])/total
                py = sum(hist2d[r][j] for r in range(bins))/total
                mi += pxy * math.log2(pxy / max(px*py, 1e-12))
    return mi

# ==============================
# REGIME DETECTION (safe, no indexing)
# ==============================
def detect_regime(ent_hist, ac_hist):
    if len(ent_hist) < 1 or len(ac_hist) < 1:
        return 'WARMUP'

    # --- mean entropy ---
    ent_sum = 0.0
    for e in ent_hist:
        ent_sum += e
    ent_mu = ent_sum / len(ent_hist)

    # --- mean autocorr across all lags ---
    total_lags = 0.0
    total_count = 0
    for ac_list in ac_hist:
        for lag in ac_list:
            total_lags += abs(lag)
            total_count += 1
    ac_mu = total_lags / total_count if total_count > 0 else 0.0

    # thresholds
    if ent_mu < 0.7:  # low entropy
        return 'LOW-ENT'
    if ac_mu > 0.25:  # high autocorr
        return 'META-AR'
    return 'STABLE'

# ==============================
# MAIN LOOP
# ==============================
print("\n=== RNG META-DOMINANCE LAB (REGIME-ADAPTIVE AR, IMPROVED) ===\n")

for i in range(1, N+1):
    x = rng.random()
    x_hist.append(x)
    x_window.append(x)

    # --- rolling entropy ---
    ent = shannon_entropy(list(x_window))
    entropy_hist.append(ent)
    ent_window.append(ent)

    # --- autocorrelation ---
    ac_lags = compute_ac_lags(list(x_window), max_lag=4)
    ac_hist.append(ac_lags)
    ac_window.append(ac_lags)

    # --- regime detection ---
    regime = detect_regime(ent_window, ac_window)
    regime_hist.append(regime)

    # --- AR coefficient updates ---
    ar_state = ar_coeffs[regime]
    if len(x_hist)>=2:
        ar_state['ar1'] = 0.7*ar_state['ar1'] + 0.3*x_hist[-2]
    if len(x_hist)>=3:
        ar_state['ar2'][0] = 0.6*ar_state['ar2'][0] + 0.4*x_hist[-2]
        ar_state['ar2'][1] = 0.6*ar_state['ar2'][1] + 0.4*x_hist[-3]

    # --- rolling stats ---
    var_hist.append(rolling_variance(list(x_window)))
    kurt_hist.append(rolling_kurtosis(list(x_window)))
    mutual_info_hist.append(mutual_info(list(x_window)))

    # --- mixed model prediction & advanced error ---
    mix_pred = (
        0.50*x +
        0.25*ar_state['ar1'] +
        0.15*sum(ar_state['ar2']) +
        0.10*(ent/5.0)
    )
    adv_err = abs(x - mix_pred)
    adv_err_hist.append(adv_err)

    # --- print state ---
    print(
        f"[{i:03d}] "
        f"x={x:.5f} "
        f"ENT={ent:.2f} "
        f"AC1={ac_lags[0]:+.3f} "
        f"AC2={ac_lags[1]:+.3f} "
        f"AC3={ac_lags[2]:+.3f} "
        f"AC4={ac_lags[3]:+.3f} "
        f"AR1e={ar_state['ar1']:.3f} "
        f"AR2e={sum(ar_state['ar2']):.3f} "
        f"VAR={var_hist[-1]:.3f} "
        f"KURT={kurt_hist[-1]:.3f} "
        f"MI={mutual_info_hist[-1]:.3f} "
        f"REG={regime:<8} "
        f"ADVerr={adv_err:.4f}"
    )

# ==============================
# THEORETICAL MAX ERROR
# ==============================
theoretical_max = max(adv_err_hist) if adv_err_hist else 0.0
print(f"\n[FINISHED — REGIME-ADAPTIVE AR, ALL FEATURES ACTIVE]")
print(f"[THEORETICAL MAX ADVERR: {theoretical_max:.4f}]")