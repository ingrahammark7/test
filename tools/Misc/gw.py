import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
years = 5000
dt = 1
time = np.arange(0, years + dt, dt)

# Model parameters
A = 1e8          # Surface area affected (m^2), e.g. 10 km x 10 km
H = 50           # Compressible sediment thickness (m)
Mv = 1e7         # Sediment constrained modulus (Pa)
kd = 1e-5        # Karst dissolution rate coefficient (m/year)
c = 0.1          # Isostatic uplift coefficient (m uplift per kg/m^2 mass loss)
rock_density = 2700  # kg/m^3

# Human activity function I(t), ramps from 0 to 1 starting 3000 years ago
I = np.zeros_like(time)
start_activity = 3000
I[years - start_activity:] = np.linspace(0, 1, start_activity + 1)

# Initialize arrays
subsidence_compaction = np.zeros_like(time)
subsidence_karst = np.zeros_like(time)
isostatic_uplift = np.zeros_like(time)
mass_loss = np.zeros_like(time)
net_subsidence = np.zeros_like(time)

# Assume hydraulic head drop proportional to human activity (scaled to 10 m max)
hydraulic_head_drop = I * 10  # meters

for i in range(1, len(time)):
    # Change in effective stress from hydraulic head change (Pa)
    d_sigma_prime_dt = (hydraulic_head_drop[i] - hydraulic_head_drop[i - 1]) * 9800  # Pa (approx. 9.8 kN/m^3)

    # Volumetric strain rate due to compaction
    d_epsilon_v_dt = d_sigma_prime_dt / Mv

    # Compaction subsidence rate (m/year)
    dD_s_dt = -d_epsilon_v_dt * H

    # Karst dissolution volume rate (m^3/year), scaled by human activity intensity
    Rd = kd * A * (0.1 + 0.9 * I[i])  # Base rate + human-enhanced dissolution

    # Increment karst subsidence (m)
    subsidence_karst[i] = subsidence_karst[i - 1] + (Rd / A) * dt

    # Mass loss rate (kg/m^2/year)
    dM_dt = (dD_s_dt + (Rd / A)) * rock_density

    # Isostatic uplift (m/year)
    U = c * abs(dM_dt)
    isostatic_uplift[i] = U

    # Update compaction subsidence
    subsidence_compaction[i] = subsidence_compaction[i - 1] + dD_s_dt * dt

    # Calculate net subsidence = compaction + karst - uplift
    net_subsidence[i] = net_subsidence[i - 1] + (dD_s_dt + (Rd / A) - U) * dt

# Plot results
plt.figure(figsize=(12, 8))
plt.plot(time, subsidence_compaction, label='Compaction Subsidence (m)')
plt.plot(time, subsidence_karst, label='Karst Dissolution Subsidence (m)')
plt.plot(time, isostatic_uplift.cumsum(), label='Cumulative Isostatic Uplift (m)')
plt.plot(time, net_subsidence, label='Net Subsidence (m)', linewidth=2, color='black')
plt.gca().invert_xaxis()  # Show years ago from left to right
plt.title('Simulated Subsidence over 5000 Years with Human Activity Influence')
plt.xlabel('Years Before Present')
plt.ylabel('Cumulative Vertical Displacement (m)')
plt.legend()
plt.grid(True)
plt.show()