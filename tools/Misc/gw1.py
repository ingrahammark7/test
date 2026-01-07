import numpy as np

# Parameters
P = 1.0                   # Power in W
E_photon = 1.602e-19      # Photon energy in J
N_photons = P / E_photon  # photons/sec
initial_radius = 1e-6     # meters
target_radius = 1e-12     # meters
shrink_factor = 0.8       # per iteration
dt = 1e-9                  # time per iteration (s)

# Initialize
nc = initial_radius
time_elapsed = 0.0
iterations = 0

# Iterate until target radius is reached
while nc > target_radius:
    nc *= shrink_factor
    time_elapsed += dt
    iterations += 1

print(f"Photon flux: {N_photons:.2e} photons/sec")
print(f"Iterations needed: {iterations}")
print(f"Time to reach {target_radius} m: {time_elapsed:.3e} s")
print(f"Final effective cloud radius: {nc:.3e} m")