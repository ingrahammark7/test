import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define axes ranges
t = np.logspace(-20, -17, 50)           # Time in seconds
T = np.linspace(0, 0.1, 50)            # Temperature in Kelvin
t_grid, T_grid = np.meshgrid(t, T)

# Hypothetical harmonized fraction / runaway probability model
P_run = np.exp(-T_grid/0.01) * (1 - np.exp(-t_grid*1e19))
P_run[P_run > 1] = 1

# Plot 3D surface
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(t_grid, T_grid, P_run, cmap='hot', edgecolor='k', alpha=0.8)

# Safe envelope boundary (semi-transparent)
ax.plot_wireframe(t_grid, T_grid, P_run*0.9, color='blue', alpha=0.3)

# Contour overlay
ax.contour(t_grid, T_grid, P_run, levels=[0.1,0.5,0.9], zdir='z', offset=-0.1, colors='k', linestyles='--')

# Arrows indicating clogged paths / environmental noise
# Draw several arrows from high P_run down to safe envelope
for i in [0, 10, 20, 30, 40]:
    ax.quiver(t_grid[0,i], T_grid[0,i], P_run[0,i]+0.05,
              0, 0, -0.05, color='cyan', arrow_length_ratio=0.2, linewidth=1.5)

# Axis labels
ax.set_xlabel("Time (s, subatomic scale)")
ax.set_ylabel("Temperature (K)")
ax.set_zlabel("Harmonized Fraction / Runaway Probability")

# Axis ticks
ax.set_xticks([1e-20, 1e-19, 1e-18, 1e-17])
ax.set_yticks([0, 0.005, 0.01, 0.05, 0.1])
ax.set_zlim(0,1)

# Color bar
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='f / P_run')

# Annotations
ax.text(1e-20, 0, 1.05, "Critical runaway, ultra-cold, minimal seed", color='red')
ax.text(1e-18, 0.01, 0.5, "Partial harmonization region", color='orange')
ax.text(1e-17, 0.1, 0.0, "Safe region, decoherence dominates", color='green')
ax.text(1e-19, 0.05, 0.6, "Cyan arrows = environmental / clogged path effect", color='cyan')

plt.title("Atomic-Scale Coherence Framework: Harmonization, Runaway Probability, and Safety Mechanisms")
plt.show()