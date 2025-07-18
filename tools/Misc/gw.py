import numpy as np
import matplotlib.pyplot as plt

# Example baseline monthly cloud fraction (12 months)
baseline_monthly = np.array([
    0.60, 0.62, 0.65, 0.70, 0.75, 0.80,
    0.78, 0.74, 0.70, 0.65, 0.62, 0.60
])

# Expand to daily values (assuming 365 days/year)
days = np.arange(365)
months = (days / 365 * 12).astype(int)
baseline_daily = baseline_monthly[months]

# Example daily ion molarity time series (simulate seasonal injection)
daily_molarity = 1e-9 + 5e-10 * np.sin(2 * np.pi * days / 365)  # oscillates seasonally

# Use your earlier CCN efficiency function (example parameters)
def ccn_efficiency(M, eta_0=1.0, M_crit=1e-9, alpha=1e10):
    excess = np.maximum(0, M - M_crit)
    return eta_0 * np.exp(-alpha * excess)

eta_daily = ccn_efficiency(daily_molarity)

# Sensitivity parameter: how strongly CCN efficiency changes cloud fraction
k = 0.3  # 30% maximum increase/decrease from baseline

# Modified daily cloud fraction combining baseline and intervention
modified_cloud = baseline_daily * (1 + k * (eta_daily - 1))

# Plot results
plt.plot(days, baseline_daily, label='Baseline Cloud Fraction')
plt.plot(days, modified_cloud, label='Modified Cloud Fraction')
plt.xlabel('Day of Year')
plt.ylabel('Cloud Fraction')
plt.legend()
plt.title('Seasonal Cloud Fraction Modification from Weather Control')
plt.grid(True)
plt.show()