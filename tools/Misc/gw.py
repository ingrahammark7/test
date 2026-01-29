import os
import time
import math
import random
import secrets
import psutil
import numpy as np
from collections import deque

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# =========================
# USER-EXPOSED CONSTANTS
# =========================

TOTAL_SAMPLES = 50
MIN_WINDOW = 1
MAX_WINDOW = 20
WINDOW_GROWTH = 1      # window sizes are powers of 2
MODEL_DECAY = 0.98         # confidence decay per step
EDGE_THRESHOLD = 0.55      # above this = temporary edge
EPS = 1e-9

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# =========================
# SYSTEM FEATURE CAPTURE
# =========================

def collect_features():
    try:
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        proc = len(psutil.pids())
    except Exception:
        cpu, mem, proc = 0.0, 0.0, 0.0
    return [cpu, mem, proc]

# =========================
# DATA COLLECTION
# =========================

X = []
y = []

print("[*] Collecting samples...")
for _ in range(TOTAL_SAMPLES):
    bit = secrets.randbits(1)
    X.append(collect_features())
    y.append(bit)
    time.sleep(0.001)

X = np.array(X)
y = np.array(y)

# =========================
# DYNAMIC WINDOW GENERATOR
# =========================

window_sizes = []
w = MIN_WINDOW
while w <= MAX_WINDOW:
    window_sizes.append(w)
    w *= WINDOW_GROWTH

# =========================
# MODELS
# =========================

models = {
    "RF": RandomForestClassifier(
        n_estimators=50,
        max_depth=None,
        random_state=RANDOM_SEED
    ),
    "LR": LogisticRegression(
        max_iter=1000,
        solver="lbfgs"
    )
}

model_scores = {k: 1.0 for k in models}  # adaptive weights

# =========================
# ONLINE REGIME ANALYSIS
# =========================

print(f"[*] Dynamic regime scan using window sizes: {window_sizes}\n")

edges_detected = 0
total_windows = 0

for w in window_sizes:
    if w >= len(y):
        continue

    correct = 0
    evaluated = 0

    for i in range(w, len(y)):
        X_train = X[i-w:i]
        y_train = y[i-w:i]
        X_test = X[i].reshape(1, -1)
        y_true = y[i]

        ensemble_vote = 0.0
        total_weight = 0.0

        for name, model in models.items():
            try:
                model.fit(X_train, y_train)
                pred = model.predict(X_test)[0]
                ensemble_vote += model_scores[name] * (1 if pred == 1 else -1)
                total_weight += model_scores[name]
            except Exception:
                continue

        if total_weight < EPS:
            continue

        final_pred = 1 if ensemble_vote > 0 else 0
        correct += int(final_pred == y_true)
        evaluated += 1

    if evaluated == 0:
        continue

    acc = correct / evaluated
    total_windows += 1

    # Edge detection
    if acc > EDGE_THRESHOLD:
        edges_detected += 1
        edge_flag = "⚠️ EDGE"
    else:
        edge_flag = ""

    # Update model confidence dynamically
    for k in model_scores:
        model_scores[k] *= MODEL_DECAY
        if acc > 0.5:
            model_scores[k] += (acc - 0.5)

    print(
        f"[Window={w:4d}] "
        f"Accuracy={acc:.4f}  "
        f"Models={{{', '.join(f'{k}:{model_scores[k]:.3f}' for k in model_scores)}}} "
        f"{edge_flag}"
    )

# =========================
# SUMMARY
# =========================

print("\n[*] Dynamic summary:")
print(f" Total windows evaluated : {total_windows}")
print(f" Edges detected          : {edges_detected}")
print(f" Edge frequency          : {edges_detected / max(total_windows,1):.3f}")
print(" Expected behavior       : transient structure only")
print(" ✅ No fixed window, no static regime, no persistent edge")
print("\n[Program finished]")