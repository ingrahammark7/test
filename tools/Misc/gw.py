import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def get_getrandom_bytes(n):
    """Generate n bytes from OS CSPRNG."""
    return np.frombuffer(os.getrandom(n), dtype=np.uint8)

def prepare_features(data, lag=1):
    """Prepare X, y arrays for lag-n prediction."""
    X = np.array([data[i:i+lag] for i in range(len(data)-lag)])
    y = data[lag:]
    return X, y

def ar_n_forest(data, lag_max=10):
    """Compute AR(n) Random Forest accuracies for lags 1..lag_max."""
    results = {}
    for lag in range(1, lag_max+1):
        X, y = prepare_features(data, lag)
        split = int(0.8*len(X))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        clf = RandomForestClassifier(n_estimators=30, n_jobs=-1)
        clf.fit(X_train, y_train)
        pred = clf.predict(X_test)
        acc = accuracy_score(y_test, pred)
        # Compute chance baseline = 1 / len(y_test)
        chance = 1 / len(y_test)
        results[lag] = (acc, chance)
    return results

# --- Parameters ---
N = 6000  # number of bytes
data = get_getrandom_bytes(N)

# --- Run AR(n) Random Forest ---
results = ar_n_forest(data, lag_max=10)

# --- Display results relative to 1/N chance ---
print(f"AR(n) Random Forest accuracy for getrandom() across lags 1-10 (chance = 1/N):")
for lag, (acc, chance) in results.items():
    print(f"Lag {lag}: Accuracy = {acc:.6f}, Chance = {chance:.6f}")