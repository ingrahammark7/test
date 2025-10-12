import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score

# --- Step 1: Input fully quantified data ---
data = {
    "Nation": ["Poland", "Egypt", "Iraq", "Afghanistan", "Italy", "France", "Germany", "Greece", "China", "India"],
    "GEO": [80, 30, 20, 40, 50, 60, 40, 50, 20, 30],  # % territory <200m
    "RES": [0.6, 0.9, 0.7, 0.3, 0.8, 0.85, 0.8, 0.6, 1.0, 0.9],  # normalized wealth
    "POL": [0.7, 0.5, 0.6, 0.7, 0.9, 0.6, 0.7, 0.8, 0.5, 0.6],  # fragmentation
    "CUL": [17, 32, 10, 5, 54, 45, 40, 20, 55, 50],  # heritage sites / cultural score
    "MIL": [0.03, 0.15, 0.10, 0.20, 0.25, 0.30, 0.35, 0.30, 0.40, 0.35],  # % natural defenses
    "LON": [1000, 3000, 4000, 2500, 3000, 2000, 2000, 3000, 4000, 4000],  # years of civilization
    "PROX": [500, 300, 200, 100, 200, 150, 100, 100, 100, 150],  # km to nearest major power
    "Historical_Conquests": [10, 12, 12, 9, 10, 9, 8, 8, 10, 10]  # actual recorded conquests
}

df = pd.DataFrame(data)

# --- Step 2: Normalize numeric metrics to 0-1 scale ---
scaler = MinMaxScaler()
metrics = ["GEO", "RES", "POL", "CUL", "MIL", "LON", "PROX"]
df_norm = df.copy()
df_norm[metrics] = scaler.fit_transform(df[metrics])

# --- Step 3: Apply weights and calculate CPI ---
weights = {"GEO":0.2, "RES":0.15, "POL":0.15, "CUL":0.1, "MIL":0.15, "LON":0.1, "PROX":0.15}

df_norm["CPI"] = (
    df_norm["GEO"] * weights["GEO"] +
    df_norm["RES"] * weights["RES"] +
    df_norm["POL"] * weights["POL"] +
    df_norm["CUL"] * weights["CUL"] +
    df_norm["MIL"] * weights["MIL"] +
    df_norm["LON"] * weights["LON"] +
    df_norm["PROX"] * weights["PROX"]
)

df_norm["CPI_Percentage"] = df_norm["CPI"] * 100

# --- Step 4: Linear regression vs historical conquests and R² ---
X = df_norm[metrics]
y = df_norm["Historical_Conquests"]

model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)
r2 = r2_score(y, y_pred)

# --- Step 5: Output final ranked table ---
df_norm["Predicted_Conquests"] = y_pred
df_final = df_norm[["Nation", "CPI_Percentage", "Historical_Conquests", "Predicted_Conquests"]].sort_values(by="CPI_Percentage", ascending=False)

print(df_final)
print(f"\nR² between CPI characteristics and historical conquest counts: {r2:.3f}")