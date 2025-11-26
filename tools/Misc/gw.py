import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Parameters ---
# Aircraft path: simple climb, cruise, and descent
t = np.linspace(0, 100, 500)  # seconds
x = t * 100                   # ground distance (m)
y = 50*np.sin(0.05*t)         # lateral maneuver
z = 20000 + 500*np.sin(0.1*t) # altitude (m)

# Air-relative Mach along path (example)
mach_air = 0.9 + 0.15*np.sin(0.05*t)  # varies 0.9-1.05

# Ground-relative Mach with tailwind (constant 100 m/s)
speed_of_sound = 295  # m/s at altitude
V_air = mach_air * speed_of_sound
V_ground = V_air + 100
mach_ground = V_ground / speed_of_sound

# --- 3D Plot ---
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111, projection='3d')

# Color by air-relative Mach
colors = plt.cm.plasma((mach_air - mach_air.min()) / (mach_air.max() - mach_air.min()))

ax.scatter(x, y, z, c=colors, s=20)

# Labels and aesthetics
ax.set_xlabel('Ground X (m)')
ax.set_ylabel('Lateral Y (m)')
ax.set_zlabel('Altitude Z (m)')
ax.set_title('Aircraft Maneuver with Air & Ground Mach Visualization')

# Colorbar for Mach
mappable = plt.cm.ScalarMappable(cmap='plasma')
mappable.set_array(mach_air)
cbar = plt.colorbar(mappable, ax=ax, shrink=0.5)
cbar.set_label('Air-relative Mach')

# Plot tailwind vector at starting point
ax.quiver(x[0], y[0], z[0], 100, 0, 0, color='cyan', length=500, normalize=True, linewidth=2, label='Jet Stream Tailwind')
ax.legend()

plt.show()