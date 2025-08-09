import numpy as np
import matplotlib.pyplot as plt

# Time parameters
years = 5000  # simulate 5000 years
dt = 1       # time step in years
time = np.arange(0, years + dt, dt)

# Model parameters (example values, can be adjusted)
A = 1e14 # surface area affected (m²), e.g. 10 km x 10 km
R0 = 1e6  # baseline dissolution rate (m³/year)
k = 4.0   # human activity sensitivity coefficient
E0 = 0.001  # baseline erosion rate (m/year)
S0 = 0.05   # baseline slope (dimensionless)
alpha = 0.001 # slope change coefficient per m subsidence
beta = 1.5  # erosion slope exponent
c = 1   # isostatic response coefficient (m uplift per m surface mass loss)

# Human activity intensity over time (0 before agriculture, ramps up after 3000 years ago)
I = np.zeros_like(time)
start_human_activity = 20000  # years ago when significant human activity starts
for i, t in enumerate(time):
    if t >= years - start_human_activity:
        I[i] = min(1.0, (t - (years - start_human_activity)) / 1000)  # ramp from 0 to 1 over 1000 years

# Initialize arrays
V = np.zeros_like(time)  # void volume dissolved (m³)
D = np.zeros_like(time)  # subsidence depth (m)
M = np.ones_like(time) * 2500  # surface mass density (kg/m²), typical rock density * thickness

for i in range(1, len(time)):
    # Dissolution rate with human influence
    Hd = 1 + k * I[i]
    Rd = R0 * Hd  # m³/year

    # Increase void volume
    V[i] = V[i-1] +(Rd * dt)**2

    # Subsidence depth (volume / area)
    D[i] =V[i] / A

    # Slope changes with subsidence
    S = S0 + alpha * D[i]

    # Erosion rate depends on slope
    E = E0 * S**beta

    # Surface mass change due to erosion (assume 2700 kg/m³ density, convert m erosion to kg/m²)
    dM_dt = -2700 * E

    # Isostatic uplift proportional to mass loss
    U = c * abs(dM_dt)

    # Net subsidence rate adjusted for uplift
    dD_dt = (Rd / A) - U

    # Update subsidence depth with uplift effect
    D[i] = D[i-1] + dD_dt* dt

# Plot results
plt.figure(figsize=(10,6))
plt.plot(time, D, label='Subsidence Depth (m)')
plt.xlabel('Years (from present)')
plt.ylabel('Cumulative Surface Subsidence (m)')
plt.title('Simulated Karst Subsidence with Human Activity and Isostatic Response')
plt.gca().invert_xaxis()  # show years ago from left to right
plt.legend()
plt.grid(True)
plt.show()