import numpy as np
import matplotlib.pyplot as plt

# --------------------------
# Simulation parameters
# --------------------------
dt = 0.01             # time step
T = 50                # total time
steps = int(T/dt)
coupling = 0.1        # photon-mediated coupling strength
temperature = 0.05    # random phase noise

# --------------------------
# Initialize dipole vectors in 2D (x, y)
# --------------------------
theta = np.random.rand(2) * 2*np.pi        # random initial angles
dipoles = np.array([np.cos(theta), np.sin(theta)]).T  # shape (2,2)

# Precompute arrays to store results
dipole_history = np.zeros((steps, 2, 2))
dipole_history[0] = dipoles

# --------------------------
# Closed-form vectorized update using linearized coupling
# --------------------------
# For small dt, we can approximate the continuous-time evolution:
# dD/dt = coupling * (D_other - D) + noise
# D(t+dt) = D(t) + dt * dD/dt + sqrt(dt)*noise

# Generate all noise at once for speed
noise = np.random.normal(0, temperature, size=(steps, 2, 2))

for t in range(1, steps):
    # Coupling term: difference of dipoles
    delta = coupling * (dipoles[::-1] - dipoles)
    
    # Update dipoles (vectorized)
    dipoles = dipoles + dt * delta + np.sqrt(dt) * noise[t]
    
    # Normalize dipoles to unit vectors (keep polarization magnitude 1)
    norms = np.linalg.norm(dipoles, axis=1, keepdims=True)
    dipoles = dipoles / norms
    
    dipole_history[t] = dipoles

# --------------------------
# Plot results
# --------------------------
time = np.arange(steps) * dt

plt.figure(figsize=(10,5))
plt.plot(time, dipole_history[:,0,0], label="Atom A x-component")
plt.plot(time, dipole_history[:,0,1], label="Atom A y-component")
plt.plot(time, dipole_history[:,1,0], '--', label="Atom B x-component")
plt.plot(time, dipole_history[:,1,1], '--', label="Atom B y-component")
plt.xlabel("Time")
plt.ylabel("Dipole components")
plt.title(f"Photon-Mediated Dipole Synchronization (Temperature={temperature})")
plt.legend()
plt.grid(True)
plt.show()