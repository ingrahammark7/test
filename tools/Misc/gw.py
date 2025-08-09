import numpy as np
import matplotlib.pyplot as plt

# Time parameters
years_total = 20000
dt = 10
time = np.arange(0, years_total + dt, dt)  # from 0 (20,000 years ago) to present

# 1) Post-glacial sea-level rise (meters)
# Approximate rise: 0 at 20k years ago to 120 m now
sea_level_rise = 120 * (1 - (time / years_total))  # decreasing with time, 0 at start, 120 at present
sea_level_rise = np.flip(sea_level_rise)  # flip to have time zero as 20k years ago

# 2) Sediment accumulation (meters) and compaction subsidence (meters)
# Assume sediment thickness accumulates linearly, max thickness ~1000 m at present
max_sediment_thickness = 1000  # meters
sediment_thickness = max_sediment_thickness * (time / years_total)
sediment_thickness = np.flip(sediment_thickness)

# Sediment compaction subsidence formula (simplified)
rho_s = 2300  # sediment density kg/m3
rho_c = 2700  # crust density kg/m3
rho_w = 1000  # water density kg/m3

sediment_subsidence = (rho_s / (rho_c - rho_w)) * sediment_thickness

# 3) Tectonic subsidence (flexural bending) modeled as sigmoid increasing over time
# Starting near zero 20k years ago, reaching ~150 m today
def sigmoid(x, L=150, x0=10000, k=0.0005):
    return L / (1 + np.exp(-k * (x - x0)))

tectonic_subsidence = sigmoid(time)
tectonic_subsidence = np.flip(tectonic_subsidence)

# 4) Karst/human subsidence: negligible before 10k years ago, increasing linearly to 50 m now
karst_subsidence = np.zeros_like(time)
for i, t in enumerate(time):
    if t <= 10000:
        karst_subsidence[i] = 0
    else:
        karst_subsidence[i] = 50 * ((t - 10000) / 10000)
karst_subsidence = np.flip(karst_subsidence)

# Total subsidence + sea level rise (depth below initial ground level)
total_subsidence = sediment_subsidence + tectonic_subsidence + karst_subsidence + sea_level_rise

# Plotting
plt.figure(figsize=(12, 7))
plt.plot(time, sea_level_rise, label='Post-Glacial Sea Level Rise (m)', linestyle='--')
plt.plot(time, sediment_subsidence, label='Sediment Compaction Subsidence (m)')
plt.plot(time, tectonic_subsidence, label='Tectonic Flexural Subsidence (m)')
plt.plot(time, karst_subsidence, label='Karst & Human Subsidence (m)')
plt.plot(time, total_subsidence, label='Total Relative Submergence (m)', linewidth=2, color='black')
plt.gca().invert_xaxis()
plt.xlabel('Years Before Present')
plt.ylabel('Depth / Subsidence (meters)')
plt.title('Combined Subsidence and Sea Level Rise Over 20,000 Years')
plt.legend()
plt.grid(True)
plt.show()