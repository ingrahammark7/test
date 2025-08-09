import random
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

def prepare_data(data, p):
    X, Y = [], []
    for i in range(p, len(data)):
        X.append(data[i-p:i])
        Y.append(data[i])
    return np.array(X), np.array(Y)

def main():
    n = 1000
    p = 10
    data = [random.random() for _ in range(n)]

    X, Y = prepare_data(data, p)

    model = RandomForestRegressor(n_estimators=50, max_depth=10, n_jobs=-1)
    model.fit(X, Y)

    Y_pred = model.predict(X)
    r2 = r2_score(Y, Y_pred)
    print(f"Random Forest nonlinear model R²: {r2:.10f}")

if __name__ == "__main__":
    main()