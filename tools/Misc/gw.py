import time
import secrets
import psutil
import numpy as np
import traceback

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ===============================
# CONFIGURABLE CONSTANTS
# ===============================
SAMPLES = 300             # Total number of random samples to collect
DELAY = 0.00              # Delay between sample collections (seconds)
RF_ESTIMATORS = 200       # Number of trees in RandomForest
RF_RANDOM_STATE = 42      # Random state for reproducibility
MIN_WINDOW_SIZE = 5       # Minimum samples to allow a window
MAX_WINDOW_SIZE = 50      # Maximum window size
WINDOW_GROWTH = 2         # Exponential growth factor for dynamic windows
EDGE_THRESHOLD = 0.55     # Accuracy above this is flagged as temporary edge
MODEL_DECAY = 0.98        # Decay factor for model confidence per window

# ===============================
# SAFE SYSTEM FEATURE COLLECTION
# ===============================
def safe(fn, default=0.0):
    try:
        return fn()
    except Exception:
        return default

def get_system_features(prev_features=None):
    cpu = safe(lambda: psutil.cpu_percent(interval=None))
    mem = safe(lambda: psutil.virtual_memory().percent)
    proc = safe(lambda: len(psutil.pids()))
    ts = time.time_ns()

    if prev_features:
        cpu_diff = cpu - prev_features[0]
        mem_diff = mem - prev_features[1]
        proc_diff = proc - prev_features[2]
        ts_diff = ts - prev_features[3]
    else:
        cpu_diff = mem_diff = proc_diff = ts_diff = 0.0

    features = [cpu, mem, proc, ts, cpu_diff, mem_diff, proc_diff, ts_diff]
    return features

# ===============================
# DATA COLLECTION
# ===============================
def collect(samples=SAMPLES, delay=DELAY):
    X, y = [], []
    prev_features = None

    print("[*] Collecting samples...")
    for i in range(samples):
        try:
            features = get_system_features(prev_features)
            prev_features = features[:4]
            target = secrets.randbits(1)
            X.append(features)
            y.append(target)
            time.sleep(delay)
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user")
            break
        except Exception as e:
            print("[!] Error collecting sample:", e)
            continue

    return np.array(X), np.array(y)

# ===============================
# DYNAMIC WINDOW ANALYSIS
# ===============================
def analyze_dynamic_windows(X, y):
    # Generate dynamic window sizes
    window_sizes = []
    w = MIN_WINDOW_SIZE
    while w <= MAX_WINDOW_SIZE:
        window_sizes.append(w)
        w *= WINDOW_GROWTH

    model_confidence = 1.0
    total_windows = 0
    edges_detected = 0

    print(f"[*] Performing dynamic window analysis: {window_sizes}")

    for w in window_sizes:
        n_windows = len(X) // w
        for i in range(n_windows):
            start = i * w
            end = start + w
            X_win = X[start:end]
            y_win = y[start:end]

            if len(X_win) < MIN_WINDOW_SIZE:
                continue

            try:
                X_train, X_test, y_train, y_test = train_test_split(
                    X_win, y_win, test_size=0.3, random_state=RF_RANDOM_STATE
                )

                rf = RandomForestClassifier(n_estimators=RF_ESTIMATORS,
                                            n_jobs=-1,
                                            random_state=RF_RANDOM_STATE)
                rf.fit(X_train, y_train)
                y_pred = rf.predict(X_test)
                acc = accuracy_score(y_test, y_pred)

                # Update model confidence dynamically
                model_confidence *= MODEL_DECAY
                if acc > 0.5:
                    model_confidence += (acc - 0.5)

                total_windows += 1
                edge_flag = ""
                if acc > EDGE_THRESHOLD:
                    edges_detected += 1
                    edge_flag = "⚠️ EDGE"

                # Feature summaries
                means = np.mean(X_win, axis=0)
                mins = np.min(X_win, axis=0)
                maxs = np.max(X_win, axis=0)

                print(f"[Window {i+1}/{n_windows}, Size={w}] "
                      f"Accuracy={acc:.4f} "
                      f"Confidence={model_confidence:.3f} "
                      f"{edge_flag}")
                print(f" Feature means: CPU={means[0]:.2f}, MEM={means[1]:.2f}, PROC={means[2]:.1f}")
                print(f" Feature min  : CPU={mins[0]:.2f}, MEM={mins[1]:.2f}, PROC={mins[2]:.1f}")
                print(f" Feature max  : CPU={maxs[0]:.2f}, MEM={maxs[1]:.2f}, PROC={maxs[2]:.1f}")

            except Exception as e:
                print(f"  [!] Error in window size {w}, window {i+1}: {e}")
                continue

    print("\n[*] Dynamic summary:")
    print(f" Total windows evaluated : {total_windows}")
    print(f" Edges detected          : {edges_detected}")
    print(f" Edge frequency          : {edges_detected / max(total_windows,1):.3f}")
    print(" Expected behavior       : transient structure only")
    print(" ✅ Fully dynamic; no fixed window, no static regime")
    print("\n[Program finished]")

# ===============================
# MAIN
# ===============================
def main():
    try:
        X, y = collect()
        analyze_dynamic_windows(X, y)
    except KeyboardInterrupt:
        print("\n[!] Program stopped by user")
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    main()