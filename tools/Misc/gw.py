import numpy as np

# Constants
G = 6.67430e-11  # gravitational constant (m^3 kg^-1 s^-2)
AU = 1.496e11    # meters
day_seconds = 86400
year_days = 365.25
century_days = 100 * year_days

# Masses
mass_venus = 4.867e24  # kg
mass_mercury = 3.301e23  # kg

# Orbits (assumed circular)
radius_mercury = 0.387 * AU
radius_venus = 0.723 * AU
omega_mercury = 2 * np.pi / (88 * day_seconds)
omega_venus = 2 * np.pi / (225 * day_seconds)

# Time steps: 1 day for 100 years
t = np.arange(0, century_days * day_seconds, day_seconds)
n = len(t)

# Venus and Mercury positions (Venus starts opposite)
theta_mercury = omega_mercury * t
theta_venus = omega_venus * t + np.pi  # start opposite

x_mercury = radius_mercury * np.cos(theta_mercury)
y_mercury = radius_mercury * np.sin(theta_mercury)

x_venus = radius_venus * np.cos(theta_venus)
y_venus = radius_venus * np.sin(theta_venus)

# Compute vector distances and unit vectors
dx = x_venus - x_mercury
dy = y_venus - y_mercury
distance = np.sqrt(dx**2 + dy**2)

# Avoid divide by zero
distance[distance == 0] = 1e-10

# Gravitational acceleration vector on Mercury due to Venus
a_x = G * mass_venus * dx / distance**3
a_y = G * mass_venus * dy / distance**3

# Integrate acceleration to get velocity perturbation
vpx = np.cumsum(a_x * day_seconds)
vpy = np.cumsum(a_y * day_seconds)

# Integrate velocity to get position perturbation
ppx = np.cumsum(vpx * day_seconds)
ppy = np.cumsum(vpy * day_seconds)

# Net position perturbation vector (final drift)
final_dx = ppx[-1]
final_dy = ppy[-1]
final_drift_magnitude = np.sqrt(final_dx**2 + final_dy**2)

# Angular error from Earth at 0.61 AU (avg Mercury-Earth distance)
earth_dist = 0.61 * AU
arcsec_per_meter = (1 / earth_dist) * (180 / np.pi) * 3600
angular_error_arcsec = final_drift_magnitude * arcsec_per_meter

# Output
print(f"Final Mercury position perturbation due to Venus: {final_drift_magnitude/1000:.2f} km")
print(f"Approximate angular displacement (arcseconds): {angular_error_arcsec:.2f}")