import numpy as np

# Constants
c = 3e8  # Speed of light (m/s)
solar_constant_1au = 1361  # Solar irradiance at 1 AU (W/m²)
au = 1.496e11  # Astronomical unit (m)
sigma = 5.67e-8  # Stefan-Boltzmann constant (W/m²/K⁴)

# User-defined parameters
spacecraft_mass_kg = 100000       # Spacecraft mass (kg)
sail_area_m2 = 1_000_000          # Sail area (m²)
ion_exhaust_velocity_m_s = 100000  # Ion exhaust velocity (m/s)
ion_thruster_efficiency = 0.7     # Efficiency (0-1)
target_velocity_fraction_c = 0.1  # Target velocity fraction of c
absorption_coeff = 0.1            # Absorptivity (0-1)
emissivity_coeff = 0.9            # Emissivity (0-1)
heat_capacity_j_per_kg_k = 700    # Heat capacity (J/kg·K)
cooling_factor = 1e-4             # Cooling factor (fraction per second)
time_step_s = 1000                  # Time step (seconds)
distance_au = 1                   # Distance from Sun (AU) — you can change this

# Functions

def solar_power_at_distance(distance_m):
    return solar_constant_1au * (au / distance_m) ** 2

def thrust_from_power(power_watts, exhaust_velocity_m_s, efficiency=0.7):
    return 2 * efficiency * power_watts / exhaust_velocity_m_s

def acceleration(thrust_newtons, spacecraft_mass_kg):
    return thrust_newtons / spacecraft_mass_kg

def relativistic_velocity(acceleration_m_s2, proper_time_s):
    return c * np.tanh(acceleration_m_s2 * proper_time_s / c)

def coordinate_time(acceleration_m_s2, proper_time_s):
    return (c / acceleration_m_s2) * np.sinh(acceleration_m_s2 * proper_time_s / c)

def relativistic_time_to_velocity(target_velocity_m_s, acceleration_m_s2):
    atanh_arg = target_velocity_m_s / c
    if abs(atanh_arg) >= 1:
        raise ValueError("Target velocity must be less than c")
    return (c / acceleration_m_s2) * np.arctanh(atanh_arg)

def simulate_cli():
    distance_m = distance_au * au
    solar_power_density = solar_power_at_distance(distance_m)
    total_power_input = solar_power_density * sail_area_m2
    thrust_newtons = thrust_from_power(total_power_input, ion_exhaust_velocity_m_s, ion_thruster_efficiency)
    acceleration_m_s2 = acceleration(thrust_newtons, spacecraft_mass_kg)

    target_velocity_m_s = target_velocity_fraction_c * c
    proper_time_to_target_s = relativistic_time_to_velocity(target_velocity_m_s, acceleration_m_s2)

    num_steps = int(proper_time_to_target_s / time_step_s) + 1

    temperature = 3.0  # Initial temperature (K)

    print(f"Simulating acceleration to {target_velocity_fraction_c*100:.1f}% of c over {num_steps} steps")
    print(f"{'Step':>5} | {'PropTime(s)':>10} | {'CoordTime(s)':>12} | {'Vel(m/s)':>12} | {'Vel(%c)':>8} | {'Temp(K)':>8}")

    for i in range(num_steps):
        proper_time = i * time_step_s
        velocity = relativistic_velocity(acceleration_m_s2, proper_time)
        coord_time = coordinate_time(acceleration_m_s2, proper_time)

        # Thermal calculation
        absorbed_power_density = solar_power_density * absorption_coeff
        emitted_power_density = emissivity_coeff * sigma * temperature ** 4
        net_power_density = absorbed_power_density - emitted_power_density
        net_power_density -= cooling_factor * (temperature - 3)
        net_power_total = net_power_density * sail_area_m2
        delta_T = (net_power_total * time_step_s) / (spacecraft_mass_kg * heat_capacity_j_per_kg_k)
        temperature = max(temperature + delta_T, 3)

        print(f"{i:5d} | {proper_time:10.1f} | {coord_time:12.1f} | {velocity:12.0f} | {velocity/c*100:8.3f} | {temperature:8.1f}")

simulate_cli()