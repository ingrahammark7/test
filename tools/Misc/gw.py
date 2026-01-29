import random
import time
import math
import collections

# =========================================================
# RNG SOURCE (strongest userspace RNG)
# =========================================================

rng = random.SystemRandom()

# =========================================================
# BASIC STATS
# =========================================================

def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0

def variance(xs, mu=None):
    if not xs:
        return 0.0
    if mu is None:
        mu = mean(xs)
    return sum((x - mu) ** 2 for x in xs) / len(xs)

def autocorr(xs, lag=1):
    if len(xs) <= lag:
        return 0.0
    mu = mean(xs)
    num = sum((xs[i] - mu) * (xs[i - lag] - mu) for i in range(lag, len(xs)))
    den = sum((x - mu) ** 2 for x in xs)
    return num / den if den else 0.0

# =========================================================
# ENTROPY (rolling, quantized)
# =========================================================

class EntropyWindow:
    def __init__(self, size):
        self.buf = collections.deque(maxlen=size)

    def add(self, x):
        self.buf.append(int(x * 256))

    def entropy(self):
        if len(self.buf) < 2:
            return 0.0
        counts = collections.Counter(self.buf)
        n = len(self.buf)
        return -sum((c/n) * math.log2(c/n) for c in counts.values())

# =========================================================
# ONLINE AUTOREGRESSIVE MODEL
# =========================================================

class ARModel:
    def __init__(self, order, lr=0.05):
        self.order = order
        self.lr = lr
        self.w = [0.0] * order

    def predict(self, hist):
        if len(hist) < self.order:
            return 0.5
        return sum(self.w[i] * hist[-i-1] for i in range(self.order))

    def update(self, hist, y):
        if len(hist) < self.order:
            return None
        yhat = self.predict(hist)
        err = y - yhat
        for i in range(self.order):
            self.w[i] += self.lr * err * hist[-i-1]
        return abs(err)

# =========================================================
# REGIME DETECTOR (THIS IS THE KEY UPGRADE)
# =========================================================

class RegimeDetector:
    """
    Soft regime detection based on:
    - entropy slope
    - AR error variance
    - window saturation
    """
    def __init__(self):
        self.prev_entropy = None
        self.stable_count = 0
        self.regime = "WARMUP"

    def update(self, entropy, ar_err, window_full):
        # Warmup until window is full
        if not window_full:
            self.regime = "WARMUP"
            self.stable_count = 0
            self.prev_entropy = entropy
            return self.regime

        # Entropy slope
        slope = 0.0
        if self.prev_entropy is not None:
            slope = entropy - self.prev_entropy

        self.prev_entropy = entropy

        # Stability conditions
        stable = abs(slope) < 0.02 and (ar_err is None or ar_err > 0.15)

        if stable:
            self.stable_count += 1
        else:
            self.stable_count = max(0, self.stable_count - 1)

        # Regime transitions (soft)
        if self.stable_count < 5:
            self.regime = "TRANSIENT"
        elif self.stable_count < 15:
            self.regime = "STABILIZING"
        else:
            self.regime = "STEADY"

        return self.regime

# =========================================================
# PER-REGIME CONTAINERS
# =========================================================

class RegimeStats:
    def __init__(self):
        self.values = []
        self.ar1 = ARModel(1)
        self.ar2 = ARModel(2)

    def update(self, hist, x):
        self.values.append(x)
        e1 = self.ar1.update(hist, x)
        e2 = self.ar2.update(hist, x)
        return e1, e2

# =========================================================
# SETUP
# =========================================================

WINDOW = 64
entropy_win = EntropyWindow(WINDOW)
values = collections.deque(maxlen=WINDOW)
history = []

detector = RegimeDetector()

regimes = {
    "WARMUP": RegimeStats(),
    "TRANSIENT": RegimeStats(),
    "STABILIZING": RegimeStats(),
    "STEADY": RegimeStats()
}

iterations = 300

print("\n=== REGIME-AWARE RNG DOMINANCE LAB ===\n")

# =========================================================
# MAIN LOOP
# =========================================================

for i in range(1, iterations + 1):
    x = rng.random()
    history.append(x)
    values.append(x)
    entropy_win.add(x)

    ent = entropy_win.entropy()
    ac1 = autocorr(list(values), 1)

    # Use global AR(1) error as detector input
    global_ar = regimes["STEADY"].ar1
    ar_err = global_ar.update(history, x)

    regime = detector.update(
        entropy=ent,
        ar_err=ar_err,
        window_full=(len(values) == WINDOW)
    )

    # Update regime-specific models
    e1, e2 = regimes[regime].update(history, x)

    print(
        f"[{i:03d}] "
        f"x={x:.5f} "
        f"ENT={ent:4.2f} "
        f"AC1={ac1:+.3f} "
        f"R={regime:<11} "
        f"AR1e={e1 if e1 else 0:.3f} "
        f"AR2e={e2 if e2 else 0:.3f}"
    )

    

# =========================================================
# RESULTS
# =========================================================

print("\n--- PER-REGIME SUMMARY ---")
for name, rs in regimes.items():
    if rs.values:
        mu = mean(rs.values)
        var = variance(rs.values, mu)
        print(
            f"{name:11} | n={len(rs.values):4d} "
            f"μ={mu:.3f} σ²={var:.4f} "
            f"AR1={rs.ar1.w} AR2={rs.ar2.w}"
        )

print("\n[FINISHED]")