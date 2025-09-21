import numpy as np
import matplotlib.pyplot as plt

# ------------------------
# Simulation Parameters
# ------------------------

# Ideal scenario (atomic-scale collapse)
rho_ideal = 1e34  # J/m^3, single pulse equivalent
pulses_ideal = 1e9  # hypothetical, atomic-scale tries
time_total = 1e6  # s, total experiment time (for realistic case)

# Realistic ablative lab scenario
rho_pulse = 5e34      # J/m^3 per pulse (ablative hotspot)
f_pulse = 1000        # Hz, pulse frequency
epsilon = 1e-3        # fraction of pulse energy that accumulates
timestep = 1          # s, simulation step

# Generate time array
time_array = np.arange(0, time_total, timestep)

# Calculate cumulative energy density over time
rho_realistic = []
cumulative = 0
for t in time_array:
    # pulses per timestep
    pulses = f_pulse * timestep
    cumulative += rho_pulse * pulses * epsilon
    rho_realistic.append(cumulative)

rho_realistic = np.array(rho_realistic)

# Ideal case: constant max (atomic-scale, instantaneous)
rho_ideal_array = np.full_like(time_array, rho_ideal * pulses_ideal)

# ------------------------
# Plot results
# ------------------------
plt.figure(figsize=(10,6))
plt.plot(time_array/3600, rho_realistic, label='Realistic Ablative Lab', color='red')
plt.plot(time_array/3600, rho_ideal_array, label='Ideal / Atomic-Scale', color='blue', linestyle='--')
plt.yscale('log')
plt.xlabel('Time (hours)')
plt.ylabel('Cumulative Energy Density (J/m³)')
plt.title('Time-Integrated Energy Density: Realistic vs Ideal')
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()