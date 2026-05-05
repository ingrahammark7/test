import numpy as np
import pandas as pd

data = [
    ("F-14 Tomcat", 115, 33, 1),
    ("F/A-18 Hornet", 120, 15, 1),
    ("F-35C", 120, 17, 1),
    ("Su-33", 115, 22, 1),

    ("F-16", 125, 12, 0),
    ("F-15", 130, 20, 0),
    ("MiG-21", 145, 9, 0),
    ("MiG-29", 120, 15, 0),
    ("Su-27", 120, 22, 0),

    ("Tu-95", 125, 188, 0),
    ("Tu-22M", 135, 112, 0),
]

df = pd.DataFrame(data, columns=["aircraft", "stall_speed", "weight", "carrier"])

# Correlations
corr_stall = df["stall_speed"].corr(df["carrier"])
corr_weight = df["weight"].corr(df["carrier"])

# Linear regression (simple OLS)
X = df[["stall_speed", "weight"]].values
y = df["carrier"].values

X_design = np.column_stack([np.ones(len(X)), X])
beta = np.linalg.lstsq(X_design, y, rcond=None)[0]

print(df)
print("\nCorrelation (stall_speed vs carrier):", corr_stall)
print("Correlation (weight vs carrier):", corr_weight)
print("\nLinear model coefficients [bias, stall, weight]:", beta)