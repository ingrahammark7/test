import numpy as np

# Constants
mu0 = 4 * np.pi * 1e-7  # Vacuum permeability
dt = 0.001              # Time step (s)
steps = 100             # Reduced for readability

class Magnet:
    def __init__(self, position, moment, mass=0.01):
        self.position = position  # 1D position
        self.moment = moment
        self.mass = mass
        self.velocity = 0.0

def dipole_force(m1, m2, r):
    if r == 0:
        return 0
    return (3 * mu0 / (4 * np.pi * r**4)) * m1.moment * m2.moment

def dipole_energy(m1, m2, r):
    if r == 0:
        return 0
    return -(mu0 / (4 * np.pi * r**3)) * m1.moment * m2.moment

# Initialize magnets
magnet1 = Magnet(position=0.0, moment=1.0)
magnet2 = Magnet(position=0.05, moment=1.0)

# Simulation
for step in range(steps):
    r = magnet2.position - magnet1.position
    F = dipole_force(magnet1, magnet2, r)
    
    # Update velocities
    magnet1.velocity -= F * dt / magnet1.mass
    magnet2.velocity += F * dt / magnet2.mass
    
    # Update positions
    magnet1.position += magnet1.velocity * dt
    magnet2.position += magnet2.velocity * dt
    
    # Energies
    kinetic = 0.5*magnet1.mass*magnet1.velocity**2 + 0.5*magnet2.mass*magnet2.velocity**2
    potential = dipole_energy(magnet1, magnet2, r)
    total = kinetic + potential
    
    print(f"Step {step}: KE={kinetic:.6e} J, PE={potential:.6e} J, Total={total:.6e} J")