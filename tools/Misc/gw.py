import numpy as np
import matplotlib.pyplot as plt

# Time parameters
years = 15000  # simulate 15,000 years ago to present
dt = 1        # time step in years
time = np.arange(years, -1, -dt)  # from 15,000 years ago down to 0 (present)

# Rates (m/year)
s1 = 0.001   # PGIA rapid phase subsidence (1 mm/yr) 15,000-4,000 ya
s2 = 0.0005  # PGIA slow phase subsidence (0.5 mm/yr) 4,000-0 ya
cs = 0.0007  # Sediment compaction subsidence (0.7 mm/yr) from 8,000 ya
ch = 0.004   # Human-induced subsidence (4 mm/yr) last 500 years

# Initialize subsidence array
D_PGIA = np.zeros_like(time, dtype=float)
D_sediment = np.zeros_like(time, dtype=float)
D_human = np.zeros_like(time, dtype=float)

T0 = 15000

for i, t in enumerate(time):
    # PGIA subsidence
    if t > 4000:
        D_PGIA[i] = s1 * (T0 - t)
    else:
        D_PGIA[i] = s1 * (T0 - 4000) + s2 * (4000 - t)

    # Sediment compaction subsidence
    if t <= 8000:
        D_sediment[i] = cs * (8000 - t)
    else:
        D_sediment[i] = 0

    # Human-induced subsidence
    if t <= 500:
        D_human[i] = ch * (500 - t)
    else:
        D_human[i] = 0

# Total subsidence
D_total = D_PGIA + D_sediment + D_human

# Plotting
plt.figure(figsize=(12, 7))
plt.plot(time, D_PGIA, label='PGIA Subsidence (Natural)')
plt.plot(time, D_sediment, label='Sediment Compaction')
plt.plot(time, D_human, label='Human-Induced Subsidence')
plt.plot(time, D_total, label='Total Subsidence', linewidth=2, color='black')

plt.xlabel('Years Ago')
plt.ylabel('Cumulative Subsidence (m)')
plt.title('Baltic Region Recent Subsidence Model Including Human Impact')
plt.gca().invert_xaxis()  # Show time from past (left) to present (right)
plt.legend()
plt.grid(True)
plt.show()