import time
import secrets
import psutil
import numpy as np
import traceback

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# ===============================
# Feature collection (safe)
# ===============================
def safe(fn, default=0.0):
    try:
        return fn()
    except Exception:
        return default


def get_features():
    cpu = safe(lambda: psutil.cpu_percent(interval=None))
    mem = safe(lambda: psutil.virtual_memory().percent)
    proc = safe(lambda: len(psutil.pids()))
    ts = time.time_ns()
    return [cpu, mem, proc, ts]


# ===============================
# Data collection
# ===============================
def collect(samples=600, delay=0.001):
    X, y = [], []

    print("[*] Collecting samples...")
    for i in range(samples):
        X.append(get_features())
        y.append(secrets.randbits(1))
        time.sleep(delay)

    return np.array(X), np.array(y)


# ===============================
# Trivial AR predictor
# ===============================
def ar_predict(y_test):
    """
    Predicts next bit = previous bit
    """
    preds = [0]
    for i in range(1, len(y_test)):
        preds.append(y_test[i - 1])
    return np.array(preds)


# ===============================
# Time-based heuristic
# ===============================
def time_predict(X_test):
    """
    Uses timestamp parity as a guess
    """
    ts = X_test[:, -1]
    return (ts % 2).astype(int)


# ===============================
# Main experiment
# ===============================
def main():
    try:
        X, y = collect()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.30, random_state=42
        )

        # ML models
        rf = RandomForestClassifier(n_estimators=300, n_jobs=-1)
        lr = LogisticRegression(max_iter=2000)

        print("[*] Training ML models...")
        rf.fit(X_train, y_train)
        lr.fit(X_train, y_train)

        rf_pred = rf.predict(X_test)
        lr_pred = lr.predict(X_test)
        ar_pred = ar_predict(y_test)
        time_pred = time_predict(X_test)

        # Individual accuracies
        print("\nModel accuracies:")
        print("RandomForest :", accuracy_score(y_test, rf_pred))
        print("LogisticReg  :", accuracy_score(y_test, lr_pred))
        print("AR trivial   :", accuracy_score(y_test, ar_pred))
        print("Time parity  :", accuracy_score(y_test, time_pred))

        # Ensemble majority vote
        ensemble = (
            rf_pred + lr_pred + ar_pred + time_pred
        ) >= 2

        ensemble = ensemble.astype(int)

        print("\nEnsemble accuracy:")
        print(accuracy_score(y_test, ensemble))

        print("\nExpected theoretical limit: 0.500")

    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()