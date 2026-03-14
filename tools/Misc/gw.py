import math

# --- Constants ---
g = 9.80665  # m/s^2, gravity
rho_20kft = 0.652  # kg/m^3, air density at 20,000 ft
mach = 0.7
gamma = 1.4  # ratio of specific heats for air
R = 287.05  # J/(kg*K), specific gas constant for air
T_20kft = 216.65  # K, standard temp at 20kft

# --- Boeing 777 parameters (approximations) ---
b777_empty_weight = 135000  # kg, typical empty weight of 777-200
b777_max_fuel = 181000  # kg, max fuel
b777_length = 63.7  # m
b777_wing_span = 60.9  # m
b777_fuselage_diameter = 6.2  # m
propulsion_efficiency = 0.35  # typical thermal efficiency of jet engines

# --- 1. Frontal area ---
frontal_area = math.pi * (b777_fuselage_diameter / 2)**2  # m^2
print("Frontal area (m^2):", frontal_area)

# --- 2. Airspeed ---
# Speed of sound at 20k ft
a = math.sqrt(gamma * R * T_20kft)
v = mach * a  # m/s
print("Velocity at Mach 0.7 at 20k ft (m/s):", v)

# --- 3. Air volume displaced per second ---
volume_flow = frontal_area * v  # m^3/s
mass_flow = volume_flow * rho_20kft  # kg/s
print("Air volume per sec (m^3/s):", volume_flow)
print("Air mass flow per sec (kg/s):", mass_flow)

# --- 4. Kinetic energy of air displaced per second (power) ---
# KE = 0.5 * m * v^2 per second => Watts
power_air = 0.5 * mass_flow * v**2  # W
print("Kinetic power of air displaced (W):", power_air)

# --- 5. Required fuel power (account for efficiency) ---
fuel_power = power_air / propulsion_efficiency  # W
print("Required fuel power (W):", fuel_power)

# --- 6. Flight time possible with max fuel ---
# Assume jet fuel energy density: 43 MJ/kg
fuel_energy_density = 43e6  # J/kg
max_fuel_energy = b777_max_fuel * fuel_energy_density  # J
flight_time_sec = max_fuel_energy / fuel_power  # s
flight_time_hr = flight_time_sec / 3600
print("Estimated flight time (hours):", flight_time_hr)

# --- 7. Average mass during flight ---
avg_mass = ((b777_empty_weight + b777_max_fuel) + b777_empty_weight) / 2  # kg
print("Average aircraft mass (kg):", avg_mass)

# --- 8. Fuel energy used to overcome gravity over this time ---
# Work against gravity = m * g * h per second integrated over time
# For level flight, only vertical work = 0; if we just compute potential if lifted 0m, trivial
# We'll assume all fuel contributes to lifting equivalent avg_mass: Power_gravity = m * g * v_vertical
# For horizontal flight, we can compare gravitational potential energy "equivalent" to fuel used
gravity_work = avg_mass * g * flight_time_sec  # J
print("Equivalent gravitational energy over flight (J):", gravity_work)

# --- 9. Ratio of fuel used to move air vs gravity equivalent ---
ratio = max_fuel_energy / gravity_work
print("Fuel energy / gravity work ratio:", ratio)