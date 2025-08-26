import numpy as np
from scipy.optimize import curve_fit

# Extended dataset: [Diameter_cm, L/D, Velocity_m_s, Mass_kg, Target_MPa, Empirical_penetration_cm]
data = np.array([
    [0.9, 1.2, 360, 0.008, 400, 2.5],
    [1.0, 1.5, 400, 0.009, 400, 3.0],
    [2.0, 2.0, 900, 0.02, 500, 5.0],
    [2.54, 1.8, 850, 0.043, 400, 7.5],
    [25.0, 29.0, 1550, 48.7, 863, 94.35],
    [25.0, 29.0, 1675, 48.7, 863, 101.0],
    [30.0, 30.0, 1500, 60.0, 900, 110.0],
    [38.1, 12.0, 760, 1200, 500, 180.0],
    [40.6, 12.0, 800, 1250, 500, 200.0],
    [35.6, 10.0, 900, 1100, 500, 175.0],
])

# Extract variables
diameter, L_D, velocity, mass, sigma, pen_empirical = data.T

# Compute kinetic energy in J
E = 0.5 * mass * velocity**2

# Define power-law penetration function
def penetration_model(X, k, alpha, beta, gamma):
    E, L, sigma = X
    return k * (E**alpha) * (L**beta) / (sigma**gamma)

# Fit model using curve_fit
popt, pcov = curve_fit(
    penetration_model, 
    (E, L_D, sigma), 
    pen_empirical, 
    p0=[1e-6, 0.5, 0.5, 0.5],  # initial guess
    maxfev=10000
)

k_fit, alpha_fit, beta_fit, gamma_fit = popt
print(f"Fitted parameters: k={k_fit:.4e}, alpha={alpha_fit:.4f}, beta={beta_fit:.4f}, gamma={gamma_fit:.4f}")

# Compute predicted penetrations and errors
pen_pred = penetration_model((E, L_D, sigma), *popt)
errors = pen_pred - pen_empirical
percent_errors = errors / pen_empirical * 100

# Print table of results
print("\nRound results:")
print(f"{'Empirical (cm)':>15} {'Predicted (cm)':>15} {'Error (cm)':>12} {'% Error':>10}")
for emp, pred, err, perc in zip(pen_empirical, pen_pred, errors, percent_errors):
    print(f"{emp:15.2f} {pred:15.2f} {err:12.2f} {perc:10.2f}")