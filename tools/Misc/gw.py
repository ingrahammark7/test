import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11        # m^3 kg^-1 s^-2
c = 3e8                # m/s
eV_to_J = 1.602176634e-19  # J/eV

# Simulation parameters
N = 10000              # Initial number of photons
E_eV = 1               # Photon energy
initial_spread = 1.0   # Initial polarization spread (radians)
filter_sharpness = 0.9 # Fraction of photons surviving each filter pass (0-1)
iterations = 200       # Max number of filter passes
initial_radius = 1e-6  # Initial effective cloud radius (meters)
target_radius = 1e-12  # Target small radius to stop simulation
dt = 1e-9              # Time per filter pass (seconds)
radius_shrink_base = 0.8 # Base shrink factor per iteration

# Initialize cloud
polarizations = np.random.uniform(-initial_spread/2, initial_spread/2, N)
nc = initial_radius
time_elapsed = 0.0

time_history = []
radius_history = []
gravity_time_history = []

for i in range(iterations):
    if len(polarizations) == 0 or nc <= target_radius:
        break
    
    # Apply polarizing filter: only photons within a fraction survive
    survival_threshold = np.max(polarizations) * filter_sharpness
    surviving = np.abs(polarizations) <= survival_threshold
    polarizations = polarizations[surviving]
    
    # Shrink effective cloud radius proportional to polarization alignment and survival fraction
    survival_fraction = len(polarizations) / N if N > 0 else 0
    shrink_factor = radius_shrink_base * survival_fraction**(1/2)
    nc *= shrink_factor
    
    # Update time
    time_elapsed += dt
    
    # Compute total mass and gravitational free-fall time
    total_energy = len(polarizations) * E_eV * eV_to_J
    M = total_energy / c**2
    if M > 0:
        t_grav = np.sqrt(nc**3 / (G * M))
    else:
        t_grav = np.nan
    
    # Record
    time_history.append(time_elapsed)
    radius_history.append(nc)
    gravity_time_history.append(t_grav)

# Plot effective radius vs time and gravitational timescale
plt.figure(figsize=(6,4))
plt.plot(time_history, radius_history, marker='o', label='Effective cloud radius')
plt.plot(time_history, gravity_time_history, marker='x', label='Gravitational collapse time')
plt.xlabel("Time (s)")
plt.ylabel("Radius / Collapse Time (m / s)")
plt.yscale('log')
plt.grid(True, which='both', ls='--')
plt.title("Photon Cloud Shrinking and Gravity Timescale")
plt.legend()
plt.show()

print(f"Final surviving photons: {len(polarizations)}")
print(f"Final effective cloud radius: {nc:.3e} m")
print(f"Time elapsed: {time_elapsed:.3e} s")
print(f"Cumulative Schwarzschild radius: {2*G*(total_energy/c**2)/c**2:.3e} m")