import numpy as np
import matplotlib.pyplot as plt

# -----------------------
# PARAMETERS
# -----------------------
G = 1.0          # Gravitational constant (normalized)
dt = 0.001       # Time step
steps = 2000     # Number of simulation steps

# Star 1 (central star)
m1 = 1.0
pos1 = np.array([0.0, 0.0])
vel1 = np.array([0.0, 0.0])

# Planet orbiting Star 1
m_planet = 0.001
r_planet = 1.0
pos_p = np.array([r_planet, 0.0])
vel_p = np.array([0.0, np.sqrt(G*m1/r_planet)])  # circular orbit

# Star 2 (neighboring star)
m2 = 1.0
pos2 = np.array([5.0, 0.0])       # distance to Star 1
vel2 = np.array([0.0, 0.0])       # stationary for simplicity

# Optional: small perturbation
perturb = 0.01
pos2 += np.array([perturb, 0.0])  # tiny shift in x-direction

# -----------------------
# FUNCTION: Compute acceleration on planet
# -----------------------
def acceleration_planet(pos_p, pos1, pos2, m1, m2):
    a1 = -G*m1 * (pos_p - pos1) / np.linalg.norm(pos_p - pos1)**3
    a2 = -G*m2 * (pos_p - pos2) / np.linalg.norm(pos_p - pos2)**3
    return a1 + a2

# -----------------------
# SIMULATION
# -----------------------
planet_positions = []

for i in range(steps):
    a = acceleration_planet(pos_p, pos1, pos2, m1, m2)
    vel_p += a*dt
    pos_p += vel_p*dt
    planet_positions.append(pos_p.copy())

planet_positions = np.array(planet_positions)

# -----------------------
# PLOT ORBIT
# -----------------------
plt.figure(figsize=(6,6))
plt.plot(planet_positions[:,0], planet_positions[:,1], label='Planet orbit')
plt.scatter(*pos1, color='orange', s=100, label='Star 1')
plt.scatter(*pos2, color='red', s=100, label='Star 2 (perturbed)')
plt.xlabel("x")
plt.ylabel("y")
plt.title("Planet orbit destabilized by small stellar perturbation")
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()