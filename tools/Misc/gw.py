import numpy as np
import math

# Constants
c = 3e8  # m/s
h = 6.626e-34  # J*s
proton_mass = 1.67e-27  # kg
atomic_radius = 1e-10  # m
planck_length = 1.616e-35  # m
seconds_per_year = 3.1536e7  # s
pc = 6 * math.pow(10, -34)  # Energy unit (your scaling)
meng=pc
g=6.7*math.pow(10,-11)
ef=pc/(c*c)
fo=g*ef*ef
rad=math.pow(10,-38)
rad=rad*rad
fo=fo/rad
v=fo/ef
v=math.sqrt(v)



# Proton and photon energies
E_proton = proton_mass * c**2  # Proton rest energy in Joules (~1.5e-10 J)
E_photon_planck = (h * c) / planck_length  # Energy of one Planck photon (~1.23e9 J)

# Number of Planck photons from one proton (with your scaling)
N = (E_proton / pc) * math.pow(10, 34)  # Huge number, ~ e+68 range or so

# Volume of atomic radius sphere (m^3)
V = 4 / 3 * np.pi * atomic_radius**3

# Calculate minimum distance for 1 crossing per year (from your code)
cr = c / atomic_radius
cr = cr * seconds_per_year
d_min = math.pow(cr * N, (1 / 3))
d_min = atomic_radius / d_min

print(f"Number of Planck photons from one proton: {N:.3e}")
print(f"Minimum distance for 1 crossing per year: {d_min:.3e} meters")

