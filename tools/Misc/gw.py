import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

# --------------------------
# Parameters
# --------------------------
T = 50                # total time
steps = 500           # number of time points to evaluate
coupling = 0.1        # coupling strength
temperature = 0.02    # standard deviation of random noise

# --------------------------
# Initial dipoles (2 atoms, 2D)
# --------------------------
theta = np.random.rand(2) * 2*np.pi
D0 = np.array([np.cos(theta[0]), np.sin(theta[0]),
               np.cos(theta[1]), np.sin(theta[1])])  # shape (4,)

# --------------------------
# Coupling matrix for 2 dipoles in 2D
# --------------------------
C = np.array([
    [-coupling, 0, coupling, 0],
    [0, -coupling, 0, coupling],
    [coupling, 0, -coupling, 0],
    [0, coupling, 0, -coupling]
])

# --------------------------
# Time points
# --------------------------
time = np.linspace(0, T, steps)

# Precompute matrix exponentials
dipole_history = np.zeros((steps, 4))
for i, t in enumerate(time):
    dipole_history[i] = expm(C * t) @ D0

# --------------------------
# Add temperature effect (simple approximation)
# --------------------------
# Noise scaled by sqrt(time step)
noise = np.random.normal(0, temperature, size=dipole_history.shape)
dipole_history += noise

# Normalize each dipole to unit vectors
norms = np.linalg.norm(dipole_history.reshape(steps,2,2), axis=2, keepdims=True)
dipole_history = (dipole_history.reshape(steps,2,2) / norms).reshape(steps,4)

# --------------------------
# Plot results
# --------------------------
plt.figure(figsize=(10,5))
plt.plot(time, dipole_history[:,0], label="Atom A x")
plt.plot(time, dipole_history[:,1], label="Atom A y")
plt.plot(time, dipole_history[:,2], '--', label="Atom B x")
plt.plot(time, dipole_history[:,3], '--', label="Atom B y")
plt.xlabel("Time")
plt.ylabel("Dipole components")
plt.title(f"Photon-mediated dipole synchronization (Temperature={temperature})")
plt.grid(True)
plt.legend()
plt.show()