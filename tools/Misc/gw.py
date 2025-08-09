import numpy as np
import matplotlib.pyplot as plt

# Time parameters
years = 500
dt = 1
time = np.arange(0, years + dt, dt)  # from 0 to 500 years (present)

# Parameters
c_s = 0.0007       # natural compaction rate (m/yr)
c_h_max = 0.004    # max human compaction rate (m/yr)

# Human activity intensity: ramp from 0 to 1 over 400 years, plateau last 100 years
I_h = np.piecewise(time, 
                   [time < 100, (time >= 100) & (time <= 400), time > 400], 
                   [0, lambda t: (t - 100) / 300, 1])

# Subsidence rate at each time step
S = c_s + c_h_max * I_h

# Cumulative subsidence over time
D = np.cumsum(S) * dt  # cumulative meters

# Initial amber layer depth
A0 = 10  # meters below surface initially

# Amber layer depth over time
A = A0 + D

# Plot results
plt.figure(figsize=(10,6))
plt.plot(time, D * 100, label='Cumulative Subsidence (cm)')
plt.plot(time, A, label='Amber Layer Depth (m)')
plt.xlabel('Years Ago (0 = start of model)')
plt.ylabel('Depth / Subsidence')
plt.title('Coupled Natural + Human-Induced Subsidence and Amber Layer Depth')
plt.legend()
plt.grid(True)
plt.show()