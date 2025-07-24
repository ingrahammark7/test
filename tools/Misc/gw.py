import numpy as np

# Constants
G = 6.67430e-11  # m^3/kg/s^2
AU = 1.496e11  # m
day_seconds = 86400
year_seconds = 365.25 * day_seconds

# Masses (kg)
mass_sun = 1.989e30
mass_mercury = 3.301e23
mass_venus = 4.867e24

# Initial orbital elements approx (heliocentric, J2000 simplified)
# Positions (m) and velocities (m/s) for circular orbits in x-y plane

# Mercury
r_mercury = 0.387 * AU
v_mercury = 47.36e3  # m/s orbital speed

# Venus
r_venus = 0.723 * AU
v_venus = 35.02e3  # m/s orbital speed

# Sun at origin
pos_sun = np.array([0., 0.])
vel_sun = np.array([0., 0.])

# Initial states: positions and velocities
pos_mercury = np.array([r_mercury, 0.])
vel_mercury = np.array([0., v_mercury])

pos_venus = np.array([-r_venus, 0.])  # Venus opposite side
vel_venus = np.array([0., -v_venus])  # direction for circular orbit

# Pack into arrays for integration convenience
positions = np.array([pos_sun, pos_mercury, pos_venus])
velocities = np.array([vel_sun, vel_mercury, vel_venus])
masses = np.array([mass_sun, mass_mercury, mass_venus])

def acceleration(positions, masses):
    n = len(masses)
    acc = np.zeros_like(positions)
    for i in range(n):
        for j in range(n):
            if i != j:
                r_vec = positions[j] - positions[i]
                r_mag = np.linalg.norm(r_vec)
                acc[i] += G * masses[j] * r_vec / r_mag**3
    return acc

# Simulation parameters
total_time = 100 * year_seconds
dt = day_seconds
steps = int(total_time / dt)

# Arrays to store Mercury perihelion angles over time
perihelion_angles = []

# Initial acceleration
acc = acceleration(positions, masses)

# Integration loop: Velocity Verlet
for step in range(steps):
    # Update positions
    positions += velocities * dt + 0.5 * acc * dt**2
    
    # Compute new acceleration
    acc_new = acceleration(positions, masses)
    
    # Update velocities
    velocities += 0.5 * (acc + acc_new) * dt
    
    # Update acceleration for next step
    acc = acc_new
    
    # Calculate Mercury’s perihelion angle approx:
    r_mercury_vec = positions[1] - positions[0]
    r_mercury_mag = np.linalg.norm(r_mercury_vec)
    
    v_mercury_vec = velocities[1] - velocities[0]
    
    # Angular momentum vector (3D)
    h_vec = np.cross(np.append(r_mercury_vec, 0), np.append(v_mercury_vec, 0))
    
    # Eccentricity vector (3D)
    e_vec_3d = (np.cross(np.append(v_mercury_vec, 0), h_vec) / (G * mass_sun)) - (np.append(r_mercury_vec, 0) / r_mercury_mag)
    e_vec = e_vec_3d[:2]
    
    peri_angle = np.arctan2(e_vec[1], e_vec[0])
    perihelion_angles.append(peri_angle)

# Unwrap angle to prevent jumps at ±π
perihelion_angles = np.unwrap(perihelion_angles)
total_precession_rad = perihelion_angles[-1] - perihelion_angles[0]

# Convert radians to arcseconds
total_precession_arcsec = np.degrees(total_precession_rad) * 3600

print(f"Mercury perihelion precession over 100 years (Newtonian Venus perturbation): {total_precession_arcsec:.2f} arcseconds")