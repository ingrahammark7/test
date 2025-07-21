import numpy as np
import math

# Constants
c = 3e8  # m/s
h = 6.626e-34  # J*s
proton_mass = 1.67e-27  # kg
atomic_radius = math.pow(10,-10) # m
planck_length = 1.616e-35  # m
seconds_per_year = 3.1536e7 # s
pc = 6 * math.pow(10, -34)  # Energy unit (your scaling)
meng=pc
ema=9*math.pow(10,-31)
g=6.7*math.pow(10,-11)
ef=pc/(c*c)
fo=g*ef*ef
rad=math.pow(10,-38)
tens=2*math.pow(10,9)

rad=atomic_radius
rad=rad*rad
fo=fo/rad
v=fo/ef
v=math.sqrt(v)
#e-29m elec


# Proton and photon energies
E_proton = proton_mass * c**2  # Proton rest energy in Joules (~1.5e-10 J)
E_photon_planck = (h * c) / planck_length  # Energy of one Planck photon (~1.23e9 J)

# Number of Planck photons from one proton (with your scaling)
par=math.pow(10,7)
N = (E_proton / pc) * par# Huge number, ~ e+68 range or so
av=math.pow(10,24)
pow=N*pc
emas=proton_mass*par
print(f"{emas:.3e}")
print("ff")

# Volume of atomic radius sphere (m^3)
V = 4 / 3 * np.pi * atomic_radius**3

# Calculate minimum distance for 1 crossing per year (from your code)
cr = c / atomic_radius
cr = cr * seconds_per_year
hr=math.pow(cr,1/3)
d_min = math.pow(cr * N, (1 /2))
d_min = atomic_radius / d_min
pow=hr*pow
print(pow)

print(f"Number of Planck photons from one proton: {N:.3e}")
print(f"Minimum distance for 1 crossing per year: {d_min:.3e} meters")