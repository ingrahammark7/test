import pandas as pd
from sklearn.linear_model import LinearRegression

# Dataset
data = {
    "Gun": [
        "7.62 NATO", "5.56 M16", "30mm Oerlikon", "40mm Bofors",
        "Panzer IV 75mm", "Pak 40 75mm", "5-inch early", "5-inch 51cal",
        "Dora 800mm", "APCR Tungsten", "Squeeze-bore 75mm"
    ],
    "Caliber_mm": [7.62, 5.56, 30, 40, 75, 75, 127, 127, 800, 75, 75],
    "Barrel_m": [0.61, 0.508, 1.5, 2.0, 3.61, 3.71, 5.0, 6.48, 32.5, 3.71, 3.15],
    "Shell_m": [0.051, 0.045, 0.15, 0.18, 0.495, 0.495, 0.7, 0.65, 7.1, 0.28, 0.25],
    "Fire_rate": [60, 700, 600, 120, 5, 5, 10, 10, 1, 5, 5],  # rounds/min
    "Material": ["Steel","Steel","Steel","Steel","Steel","Steel","Steel","Steel","Steel","Tungsten","Tungsten"]
}

df = pd.DataFrame(data)
df["Ratio"] = df["Shell_m"] / df["Barrel_m"]

# Encode material
df["Material_num"] = df["Material"].map({"Steel":0, "Tungsten":1})

# Features and target
X = df[["Caliber_mm","Fire_rate","Material_num"]]
y = df["Ratio"]

# Fit linear regression
model = LinearRegression()
model.fit(X, y)

# Coefficients and intercept
print("Intercept:", model.intercept_)
print("Coefficients (Caliber, Fire_rate, Material):", model.coef_)

# R²
r2 = model.score(X, y)
print("R²:", r2)

# Predicted ratios
df["Predicted_Ratio"] = model.predict(X)
print(df[["Gun","Ratio","Predicted_Ratio"]])