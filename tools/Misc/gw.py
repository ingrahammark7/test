import random
import time
import math

# Use hardware RNG
rng = random.SystemRandom()

# -----------------------------
# System info helpers
# -----------------------------

# Function to get memory info from /proc/meminfo (Android/Linux)
def get_memory():
    try:
        meminfo = {}
        with open("/proc/meminfo") as f:
            for line in f:
                parts = line.split()
                key = parts[0].rstrip(':')
                value = int(parts[1])
                meminfo[key] = value  # in kB

        total = meminfo.get("MemTotal", 0) / 1024  # MB
        free = meminfo.get("MemFree", 0) / 1024
        available = meminfo.get("MemAvailable", 0) / 1024
        used = total - free
        return total, used, available
    except Exception:
        return 0.0, 0.0, 0.0

# Function to get CPU usage from /proc/stat
def get_cpu():
    try:
        with open("/proc/stat") as f:
            line = f.readline()
        parts = line.split()
        if parts[0] != 'cpu':
            return None, None
        vals = list(map(int, parts[1:]))
        idle = vals[3] + vals[4]  # idle + iowait
        total = sum(vals)
        return idle, total
    except Exception:
        return None, None

# -----------------------------
# Online ML model
# -----------------------------

# Logistic regression with online SGD
# Features:
# [bias, rng_value, cpu_load, used_mem_ratio, avail_mem_ratio]
weights = [0.0, 0.1, 0.1, 0.1, 0.1]
learning_rate = 0.05

def sigmoid(x):
    # Numerically safe sigmoid
    if x < -60:
        return 0.0
    if x > 60:
        return 1.0
    return 1.0 / (1.0 + math.exp(-x))

def predict(features):
    z = sum(w * x for w, x in zip(weights, features))
    return sigmoid(z)

def update(features, target):
    global weights
    pred = predict(features)
    error = target - pred
    for i in range(len(weights)):
        weights[i] += learning_rate * error * features[i]
    return pred

# -----------------------------
# Simulation
# -----------------------------

iterations = 20
sleep_time = 0

prev_idle, prev_total = get_cpu()

print(f"Starting simulation: {iterations} iterations")

for i in range(1, iterations + 1):
    # RNG value
    val = rng.random()

    # Memory stats
    total_mem, used_mem, avail_mem = get_memory()

    # CPU usage calculation
    idle, total = get_cpu()
    cpu_percent = 0.0
    if (
        idle is not None and prev_idle is not None and
        total is not None and prev_total is not None and
        total != prev_total
    ):
        cpu_percent = 100.0 * (1.0 - (idle - prev_idle) / (total - prev_total))
        prev_idle, prev_total = idle, total

    # Feature engineering
    used_ratio = used_mem / total_mem if total_mem > 0 else 0.0
    avail_ratio = avail_mem / total_mem if total_mem > 0 else 0.0

    features = [
        1.0,                    # bias
        val,                    # RNG value
        cpu_percent / 100.0,    # CPU load
        used_ratio,             # memory pressure
        avail_ratio
    ]

    # Synthetic target:
    # "Win" if RNG > 0.5 (you can replace this with any reward signal)
    target = 1.0 if val > 0.5 else 0.0

    # ML prediction + online training
    win_prob = update(features, target)

    # Python memory placeholder (intentionally minimal)
    python_mem = 0.0

    # Log iteration
    print(
        f"[Iteration {i}/{iterations}] "
        f"CPU={cpu_percent:6.2f}% | "
        f"Mem(T/U/A)={total_mem:7.1f}/{used_mem:7.1f}/{avail_mem:7.1f} MB | "
        f"RNG={val:.6f} | "
        f"WinProb={win_prob:.4f}"
    )

    

print("\nFinal ML weights:")
for i, w in enumerate(weights):
    print(f"  w[{i}] = {w:.6f}")

print("\n[Program finished]")