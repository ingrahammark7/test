import numpy as np
import matplotlib.pyplot as plt

# Gel depth
depth = np.linspace(0, 0.6, 200)
baseline = 500 * np.exp(-((depth - 0.30)/0.10)**2)
baseline_peak = baseline.max()

# Plate thickness and standoff
thicknesses = np.linspace(0.1, 1.5, 25)
standoffs = np.linspace(0, 0.6, 25)
limb_absorption = 0.5
peak_energy = np.zeros((len(thicknesses), len(standoffs)))

# Compute peak energy
for i, t in enumerate(thicknesses):
    perturbation_factor = np.exp(-t/0.5)
    peak_depth = 0.30 - 0.15*perturbation_factor
    width = 0.10 + 0.05*np.clip((t-0.8)/0.5,0,1)
    amplitude = 500 * (1 - np.clip((t-0.8)/0.5,0,1))
    curve = amplitude * np.exp(-((depth - peak_depth)/width)**2)
    for j, s in enumerate(standoffs):
        air_loss_factor = 1 / (1 + (s/0.3)**2)
        curve_standoff = curve * air_loss_factor * (1 - limb_absorption)
        peak_energy[i,j] = curve_standoff.max()

# Plot simple color map
plt.figure(figsize=(9,6))
X, Y = np.meshgrid(standoffs*100, thicknesses)
plt.pcolormesh(X, Y, peak_energy, shading='auto', cmap='viridis')
plt.colorbar(label='Peak energy in gel (J/m approx.)')

# Optional: single contour for baseline
plt.contour(X, Y, peak_energy, levels=[baseline_peak], colors='red', linewidths=1)

plt.xlabel("Standoff distance (cm)")
plt.ylabel("Plate thickness (HVL)")
plt.title("Peak Gel Energy vs Plate Thickness and Standoff")
plt.show()