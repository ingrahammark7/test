from mpmath import mp, power, pi, sqrt

# Set maximum precision
mp.dps = 100

# Constants
f = mp.mpf('1.45e-6')             # fraction of water permittivity needed
mass_water = mp.mpf('2.992e-26')  # kg, one water molecule
density_water = mp.mpf('1000')    # kg/m^3

# Mass ratio
mass_object = mass_water / f
print(f"Mass of object: {mass_object} kg")

# Atom count (approximate, assuming 1 atom per water mass unit)
atom_count = mass_object / mass_water
print(f"Approximate number of water-molecule masses: {atom_count}")

# Volume of object
volume_object = mass_object / density_water  # m^3

# Radius of object assuming spherical
radius_object = (3 * volume_object / (4 * pi))**(1/3)
print(f"Radius of object: {radius_object} m")