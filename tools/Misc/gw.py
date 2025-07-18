import math

# Constants
NA = 6.022e23  # Avogadro's number, molecules/mol
kB = 1.38e-23  # Boltzmann constant, J/K
g = 9.81  # gravity, m/s^2
eta = 1.8e-5  # dynamic viscosity of air, Pa·s
rho_air = 1.2  # air density kg/m^3 (sea level)
rho_salt = 2170  # salt density kg/m^3

# Inputs
mass_salt_g = 1.0  # grams
molar_mass_salt = 58.44  # g/mol (NaCl)
particle_diameter_m = 1e-6  # 1 micron
airspeed_m_per_s = 1.0  # m/s
temp_K = 298  # Kelvin (25C)
relative_humidity = 0.5  # 50%
settling_height_m = 3000  # 3 km altitude
column_area_m2 = 1.0  # cross-sectional area of air column in m^2

# Calculations

# Number of moles of salt
moles_salt = mass_salt_g / molar_mass_salt

# Number of salt molecules
num_salt_molecules = moles_salt * NA

# Particle volume and mass
radius = particle_diameter_m / 2
particle_volume = (4/3) * math.pi * radius**3  # m^3
particle_mass = rho_salt * particle_volume  # kg

# Number of particles
mass_salt_kg = mass_salt_g / 1000
num_particles = mass_salt_kg / particle_mass

# Water vapor number density
# Saturation vapor pressure at 25C ~3167 Pa
partial_pressure_water = relative_humidity * 3167  # Pa
number_density_water = partial_pressure_water / (kB * temp_K)  # molecules/m^3

# Cross-sectional area of one particle
cross_section_area = math.pi * radius**2  # m^2

# Volume swept per second by particle
volume_swept_per_sec = cross_section_area * airspeed_m_per_s  # m^3/s

# Number of water molecules encountered per particle per second
water_molecules_per_particle_sec = number_density_water * volume_swept_per_sec

# Total water molecules encountered by all salt particles per second
total_water_encounters_per_sec = num_particles * water_molecules_per_particle_sec

# Calculate settling velocity with Stokes' Law
settling_velocity = (2/9) * (radius**2) * g * (rho_salt - rho_air) / eta  # m/s

# Time to settle from altitude (seconds)
settling_time_sec = settling_height_m / settling_velocity

# Total water molecules encountered over settling time
total_water_encounters_over_time = total_water_encounters_per_sec * settling_time_sec

# Molar ratio: total water molecules encountered over settling time to salt molecules
molar_ratio = total_water_encounters_over_time / num_salt_molecules

# Calculate total water molecules in air column
air_column_volume = column_area_m2 * settling_height_m  # m^3
total_water_molecules_in_column = number_density_water * air_column_volume

# Calculate salt mass needed so total encounters = total water molecules in column
# Since encounters scale linearly with salt mass:
salt_mass_needed_kg = (total_water_molecules_in_column / total_water_encounters_over_time) * mass_salt_kg
salt_mass_needed_g = salt_mass_needed_kg * 1000  # convert to grams

# Print results
print(f"Number of salt molecules in {mass_salt_g}g salt: {num_salt_molecules:.2e}")
print(f"Number of salt particles (1 micron diameter): {num_particles:.2e}")
print(f"Water molecules encountered per particle per second: {water_molecules_per_particle_sec:.2e}")
print(f"Total water molecules encountered by all salt particles per second: {total_water_encounters_per_sec:.2e}")
print(f"Settling velocity (m/s): {settling_velocity:.2e}")
print(f"Time to settle {settling_height_m} m (seconds): {settling_time_sec:.2e} (~{settling_time_sec / (3600*24*365):.2f} years)")
print(f"Total water molecules encountered over settling time: {total_water_encounters_over_time:.2e}")
print(f"Molar ratio (water molecules encountered / salt molecules): {molar_ratio:.2f}")
print(f"Total water molecules in {column_area_m2} m² × {settling_height_m} m air column: {total_water_molecules_in_column:.2e}")
print(f"Salt mass needed (grams) to encounter all water molecules in column: {salt_mass_needed_g:.5e} g")