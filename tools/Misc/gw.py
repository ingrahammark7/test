import numpy as np

# constants
rho_air = 1.225  # kg/m^3 (sea level approx, jet stream slightly lower but similar order)
v = 100          # m/s jet stream speed (your assumption)

# wind power density (correct formula)
wind_power_density = 0.5 * rho_air * v**3  # W/m^2

# hypothetical aircraft
mass = 100000      # kg (100 tons)
g = 9.81           # m/s^2
wing_area = 500    # m^2

# required lift force
weight = mass * g  # N

# "power equivalent" if you incorrectly convert weight over some velocity scale
# (this is just to show mismatch, not a real aerodynamic quantity)
sink_rate = 10  # m/s (typical glide-ish vertical speed scale)
required_power = weight * sink_rate  # W

print("Wind power density (W/m^2):", wind_power_density)
print("Total wind power over wing area (MW):", wind_power_density * wing_area / 1e6)
print("Aircraft weight (N):", weight)
print("Approx power needed to oppose gravity at 10 m/s descent (MW):", required_power / 1e6)