import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

# Dataset
data = np.array([
    ["9mm_NIJ", 0.008, 0.009, 1.0, 360, 860, 2.0],
    [".308_NIJ", 0.01, 0.00762, 1.0, 820, 860, 5.0],
    ["20mm_AP", 0.12, 0.02, 5.0, 1000, 860, 18.0],
    ["30mm_AP", 0.25, 0.03, 6.0, 1050, 860, 28.0],
    ["105mm_APDS", 8.0, 0.105, 20.0, 1400, 860, 72.0],
    ["M829_DU", 4.5, 0.025, 29.0, 1550, 863, 94.0]
])

def penetration_model(X, alpha, beta, delta, gamma, eta):
    mass, dia, ld, vel, sigma = X
    return alpha * (ld**beta) * (vel**delta) * (mass**gamma) * ((860/sigma)**eta)

# Prepare arrays
X = np.array(data[:,1:6], dtype=float).T
y = np.array(data[:,6], dtype=float)

# Fit parameters
popt, pcov = curve_fit(penetration_model, X, y, p0=[0.01, 0.5, 0.5, 0.5, 0.5])

# Predict and calculate errors
y_pred = penetration_model(X, *popt)
abs_error = y_pred - y
rel_error = abs_error / y * 100

# Build table
df = pd.DataFrame({
    "Round": data[:,0],
    "Empirical (cm)": y,
    "Model (cm)": y_pred,
    "Abs Error (cm)": abs_error,
    "Rel Error (%)": rel_error
})

print(df)
print("Fitted parameters: alpha, beta, delta, gamma, eta")
print(popt)