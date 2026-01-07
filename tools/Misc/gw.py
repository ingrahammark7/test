import numpy as np
from sklearn.ensemble import RandomForestRegressor

# ------------------------------
# Step 1: Generate SecureRandom-style sequence
# ------------------------------
secure_rng = np.random.default_rng()  # Secure RNG
num_samples = 10000
seq_len = 5
rng_data = secure_rng.random(num_samples + seq_len)

# ------------------------------
# Step 2: Feature engineering (vectorized)
# ------------------------------
# Previous sequences
X_seq = np.array([rng_data[i:i+seq_len] for i in range(num_samples)])

# AR(1) differences
X_diff = np.diff(X_seq, axis=1)

# Regime / quantiles
X_quant = np.digitize(X_seq, bins=[0.33, 0.66])

# Rolling statistics
X_mean = np.mean(X_seq, axis=1).reshape(-1, 1)
X_std = np.std(X_seq, axis=1).reshape(-1, 1)

# Combine all features
X = np.hstack([X_seq, X_diff, X_quant, X_mean, X_std])
y = rng_data[seq_len:]

# ------------------------------
# Step 3: Train-test split
# ------------------------------
X_train, X_test = X[:8000], X[8000:]
y_train, y_test = y[:8000], y[8000:]

# ------------------------------
# Step 4: Train optimized Random Forest
# ------------------------------
rf = RandomForestRegressor(
    n_estimators=150,   # fewer trees for speed
    max_depth=12,       # shallower trees
    random_state=42,
    n_jobs=-1           # use all CPU cores
)
rf.fit(X_train, y_train)

# ------------------------------
# Step 5: Predict & compute R and R²
# ------------------------------
y_pred = rf.predict(X_test)

# Pearson correlation R
R = np.corrcoef(y_test, y_pred)[0, 1]

# R² as the square of R (always non-negative)
R_squared = R ** 2

print(f"Fast model R: {R:.6f}")
print(f"Fast model R² (square of R): {R_squared:.6f}")

# ------------------------------
# Step 6: Predict next RNG value
# ------------------------------
last_seq = rng_data[-seq_len:]
diffs = np.diff(last_seq)
quantiles = np.digitize(last_seq, bins=[0.33, 0.66])
mean = np.mean(last_seq)
std = np.std(last_seq)
features = np.concatenate([last_seq, diffs, quantiles, [mean, std]])
next_val = rf.predict([features])[0]
print(f"Predicted next RNG value: {next_val:.6f}")