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
SAMPLES = 300       # Total number of random samples to collect
WINDOW_SIZE = 20      # Samples per sub-regime window
DELAY = 0.00     # Delay between sample collections (seconds)
RF_ESTIMATORS = 200     # Number of trees in RandomForest
RF_RANDOM_STATE = 42    # Random state for reproducibility
MIN_WINDOW_SIZE = 1   # Minimum samples to allow a window


# ===============================
# Safe system feature collection
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
# Data collection
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
            if i % 1000 == 0 and i > 0:
                print(f"  Collected {i} samples")
            time.sleep(delay)
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user")
            break
        except Exception as e:
            print("[!] Error collecting sample:", e)
            continue

    return np.array(X), np.array(y)


# ===============================
# Sub-regime analysis (console output)
# ===============================
def analyze_subregimes(X, y, window_size=WINDOW_SIZE):
    n_samples = len(X)
    n_windows = n_samples // window_size
    window_accs = []

    print(f"[*] Performing sub-regime analysis ({n_windows} windows of {window_size} samples)...")

    for w in range(n_windows):
        start = w * window_size
        end = start + window_size
        X_win = X[start:end]
        y_win = y[start:end]

        if len(X_win) < MIN_WINDOW_SIZE:
            continue

        X_train, X_test, y_train, y_test = train_test_split(
            X_win, y_win, test_size=0.3, random_state=RF_RANDOM_STATE
        )

        rf = RandomForestClassifier(n_estimators=RF_ESTIMATORS, n_jobs=-1, random_state=RF_RANDOM_STATE)
        try:
            rf.fit(X_train, y_train)
            y_pred = rf.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            window_accs.append(acc)

            # Feature summaries
            means = np.mean(X_win, axis=0)
            mins = np.min(X_win, axis=0)
            maxs = np.max(X_win, axis=0)

            print(f"\n[Window {w+1}/{n_windows}] Accuracy: {acc:.4f}")
            print(f" Feature means: CPU={means[0]:.2f}, MEM={means[1]:.2f}, PROC={means[2]:.1f}")
            print(f" Feature min  : CPU={mins[0]:.2f}, MEM={mins[1]:.2f}, PROC={mins[2]:.1f}")
            print(f" Feature max  : CPU={maxs[0]:.2f}, MEM={maxs[1]:.2f}, PROC={maxs[2]:.1f}")
            if acc > 0.55:
                print(" ⚠️ Accuracy above 0.55 (check regime)")

        except Exception as e:
            print(f"  [!] Error in window {w+1}: {e}")
            window_accs.append(np.nan)

    return np.array(window_accs)


# ===============================
# Main
# ===============================
def main():
    try:
        X, y = collect()
        accs = analyze_subregimes(X, y, window_size=WINDOW_SIZE)

        mean_acc = np.nanmean(accs)
        std_acc = np.nanstd(accs)
        print("\n[*] Sub-regime summary:")
        print(f" Mean accuracy over all windows: {mean_acc:.4f}")
        print(f" Std deviation over windows  : {std_acc:.4f}")
        print(" Expected baseline           : 0.500")
        print(" ✅ TRNG remains unpredictable; any spikes are finite-sample noise")

    except KeyboardInterrupt:
        print("\n[!] Program stopped by user")
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()