import numpy as np

# Constants
G = 6.67430e-11  # gravitational constant (m^3 kg^-1 s^-2)
mass_venus = 4.867e24  # kg
mass_mercury = 3.301e23  # kg
AU = 1.496e11  # meters
year_days = 365.25
century_days = 100 * year_days
day_seconds = 86400  # seconds in a day

# Orbital parameters (assuming circular orbits for simplicity)
radius_mercury = 0.387 * AU  # average distance to sun
radius_venus = 0.723 * AU
omega_mercury = 2 * np.pi / (88 * day_seconds)  # rad/s
omega_venus = 2 * np.pi / (225 * day_seconds)  # rad/s

# Time array: 1-day time steps for 100 years
t = np.arange(0, century_days * day_seconds, day_seconds)

# Mercury and Venus positions (initially on opposite sides of the Sun)
theta_mercury = omega_mercury * t
theta_venus = omega_venus * t + np.pi

x_mercury = radius_mercury * np.cos(theta_mercury)
y_mercury = radius_mercury * np.sin(theta_mercury)
x_venus = radius_venus * np.cos(theta_venus)
y_venus = radius_venus * np.sin(theta_venus)

# Compute the gravitational force vector and its effect on Mercury's orbit
dx = x_venus - x_mercury
dy = y_venus - y_mercury
distance = np.sqrt(dx**2 + dy**2)

# Gravitational force magnitude (not vector, just scalar influence)
force = G * mass_mercury * mass_venus / distance**2

# Compute average perturbing acceleration on Mercury from Venus
acceleration = force / mass_mercury  # m/s^2

# Cumulative velocity perturbation over time (Euler integration)
velocity_perturbation = np.cumsum(acceleration * day_seconds)

# Position perturbation over time
position_perturbation = np.cumsum(velocity_perturbation * day_seconds)

# Approximate angular error: arcseconds per km of radial error
# Mercury’s distance from Earth ~0.61 AU average
avg_mercury_distance = 0.61 * AU  # meters
arcsec_per_km = (1 / avg_mercury_distance) * (180 / np.pi) * 3600 * 1000

# Final displacement in meters and arcseconds
final_displacement_km = position_perturbation[-1] / 1000
arcsec_error = final_displacement_km * arcsec_per_km

print(arcsec_error, final_displacement_km)