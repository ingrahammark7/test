import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 1. Define the Hubbert mathematical model
def hubbert_curve(t, L, k, t0):
    """
    Calculates the Hubbert curve production rate for a given time 't'.
    """
    numerator = L * k * np.exp(-k * (t - t0))
    denominator = (1 + np.exp(-k * (t - t0)))**2
    return numerator / denominator

# 2. Input your sample data
# For this example, we are using generic years and production volumes (e.g., millions of barrels)
years = np.array([1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020])
production = np.array([10, 15, 25, 40, 55, 60, 52, 45, 30])

# 3. Fit the curve to the data
# We provide initial guesses [L, k, t0] to help the optimizer converge faster
initial_guesses = [2000, 0.1, 2005]

# curve_fit returns the optimal parameters (popt) and the covariance matrix (pcov)
popt, pcov = curve_fit(hubbert_curve, years, production, p0=initial_guesses)

# Extract the fitted parameters
L_fit, k_fit, t0_fit = popt

print("--- Fitted Parameters ---")
print(f"Total Ultimate Resource (L): {L_fit:.2f}")
print(f"Growth Rate (k): {k_fit:.4f}")
print(f"Peak Year (t0): {t0_fit:.1f}")

# 4. Generate smooth data points to draw the fitted curve
years_smooth = np.linspace(1975, 2030, 200)
production_fit = hubbert_curve(years_smooth, L_fit, k_fit, t0_fit)

# 5. Plot the original data and the fitted Hubbert curve
plt.figure(figsize=(10, 6))

# Plot actual data points
plt.scatter(years, production, color='red', label='Actual Sample Data', zorder=5)

# Plot the fitted curve
plt.plot(years_smooth, production_fit, color='blue', label='Fitted Hubbert Curve', linewidth=2.5)

# Add a vertical line to indicate the peak year
plt.axvline(x=t0_fit, color='gray', linestyle='--', label=f'Peak Year ({t0_fit:.0f})')

# Formatting the chart
plt.title('Hubbert Curve Fit to Production Data', fontsize=14, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Production Rate', fontsize=12)
plt.legend(loc='upper right')
plt.grid(True, linestyle=':', alpha=0.7)
plt.tight_layout()

# Display the plot
plt.show()