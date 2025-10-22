import os
import numpy as np
from secrets import token_bytes
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import random

def get_bytes(source, n=50):
    if source == "getrandom":
        return np.frombuffer(os.getrandom(n), dtype=np.uint8)
    elif source == "secrets":
        return np.frombuffer(token_bytes(n), dtype=np.uint8)
    elif source == "mersenne":
        return np.array([int(random.random()) for _ in range(n)], dtype=np.uint8)

def ar1_forest(data):
    # Lag-1 features: x[t] predicts x[t+1]
    X = data[:-1].reshape(-1, 1)
    y = data[1:]
    split = int(len(X)*.5)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    clf = RandomForestClassifier(n_estimators=50, n_jobs=-1)
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    acc = accuracy_score(y_test, pred)
    return acc

# --- Test each source ---
nbytes = 50
sources = ["getrandom", "secrets", "mersenne"]

for s in sources:
    data = get_bytes(s, nbytes)
    acc = ar1_forest(data)
    print(f"{s} AR(1) Random Forest accuracy: {acc:.5f}")