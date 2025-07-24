import numpy as np

# Constants
G = 6.67430e-11  # m^3 kg^-1 s^-2
mass_venus = 4.867e24  # kg
mass_mercury = 3.301e23  # kg
AU = 1.496e11  # meters
day_seconds = 86400  # seconds in a day

# Orbital parameters (circular orbits)
radius_mercury = 0.387 * AU
radius_venus = 0.723 * AU
omega_mercury = 2 * np.pi / (88 * day_seconds)  # rad/s
omega_venus = 2 * np.pi / (225 * day_seconds)   # rad/s

# Time setup: 1 day steps for 100 years
century_days = 100 * 365.25
t = np.arange(0, century_days * day_seconds, day_seconds)
n_steps = len(t)

# Initialize position arrays
x_mercury = np.zeros(n_steps)
y_mercury = np.zeros(n_steps)
x_venus = radius_venus * np.cos(omega_venus * t + np.pi)  # Venus starts opposite Mercury
y_venus = radius_venus * np.sin(omega_venus * t + np.pi)

# Mercury initial position and velocity (circular orbit)
x_mercury[0] = radius_mercury
y_mercury[0] = 0
v_mercury_x = 0
v_mercury_y = radius_mercury * omega_mercury  # tangential velocity for circular orbit

# We will store velocity perturbations relative to ideal circular velocity
v_pert_x = 0
v_pert_y = 0

# To isolate perturbation, ideal Mercury orbit (no Venus) at each step:
x_mercury_ideal = radius_mercury * np.cos(omega_mercury * t)
y_mercury_ideal = radius_mercury * np.sin(omega_mercury * t)

# Integration loop (Euler)
for i in range(1, n_steps):
    # Vector from Mercury to Venus
    dx = x_venus[i-1] - x_mercury[i-1]
    dy = y_venus[i-1] - y_mercury[i-1]
    dist = np.sqrt(dx**2 + dy**2)
    
    # Gravitational acceleration vector due to Venus on Mercury
    a_mag = G * mass_venus / dist**2
    a_x = a_mag * dx / dist
    a_y = a_mag * dy / dist

    # Update velocity perturbation
    v_pert_x += a_x * day_seconds
    v_pert_y += a_y * day_seconds
    
    # Update Mercury's position with velocity perturbation added to ideal velocity
    # Ideal velocity components (circular orbit)
    v_ideal_x = -radius_mercury * omega_mercury * np.sin(omega_mercury * t[i-1])
    v_ideal_y = radius_mercury * omega_mercury * np.cos(omega_mercury * t[i-1])
    
    # Total velocity = ideal + perturbation
    v_total_x = v_ideal_x + v_pert_x
    v_total_y = v_ideal_y + v_pert_y
    
    # Euler position update
    x_mercury[i] = x_mercury[i-1] + v_total_x * day_seconds
    y_mercury[i] = y_mercury[i-1] + v_total_y * day_seconds

# Calculate radial difference from ideal orbit (perturbation magnitude)
radial_diff = np.sqrt((x_mercury - x_mercury_ideal)**2 + (y_mercury - y_mercury_ideal)**2)

# Estimate angular displacement (precession) from Earth viewpoint
# Average distance Mercury-Earth ~ 0.61 AU = 0.61 * AU meters
avg_mercury_distance = 0.61 * AU  # meters
arcsec_per_meter = (1 / avg_mercury_distance) * (180 / np.pi) * 3600

# Take the final radial difference in meters and convert to arcseconds
final_displacement_m = radial_diff[-1]
arcsec_error = final_displacement_m * arcsec_per_meter

print(f"Final radial displacement (m): {final_displacement_m:.2f}")
print(f"Approximate angular displacement from Earth (arcseconds): {arcsec_error:.2f}")