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

# Electrostatic repulsion energy normalized by proton energy
cq = 9 * math.pow(10, 9)
ec = 1.6 * math.pow(10, -19)
ev = cq * ec * ec
ev = ev / (atomic_radius * atomic_radius)
ev = ev / E_proton
print(f"Normalized electrostatic repulsion energy: {ev:.3e}")

# --- Incremental splitting and cooling system ---

# Number of splitting steps (each step halves photon energy, doubles photon count)
steps = math.log2(N)

# Energy per photon at final step
E_photon_final = E_proton / N

# Total cooling energy removed is proton rest energy (approximate)
total_cooling_energy = E_proton  # Joules

# Cooling system parameters
desired_time = 60  # seconds over which the full process should complete
cooling_efficiency = 0.7  # 70% efficiency in removing heat (losses included)
cooling_power_required = total_cooling_energy / (desired_time * cooling_efficiency)  # Watts

# Photon density after full splitting
photon_density = N / V  # photons per m^3

# Estimate photon mean free path - rough approximation
# Assuming photon cross-section ~ atomic radius squared (just order of magnitude)
photon_cross_section = atomic_radius**2
mean_free_path = 1 / (photon_density * photon_cross_section)  # meters

print(f"Splitting steps needed (log2(N)): {steps:.3e}")
print(f"Final photon energy: {E_photon_final:.3e} J")
print(f"Total cooling energy required: {total_cooling_energy:.3e} J")
print(f"Cooling power needed (accounting for efficiency) to finish in {desired_time} s: {cooling_power_required:.3e} W")
print(f"Photon density in atomic radius volume: {photon_density:.3e} photons/m^3")
print(f"Estimated photon mean free path: {mean_free_path:.3e} meters")

# Cooling rate per step (energy removed per step per second)
energy_per_step = E_proton / steps
cooling_power_per_step = energy_per_step / desired_time

print(f"Energy removed per splitting step: {energy_per_step:.3e} J")
print(f"Cooling power per splitting step over {desired_time} seconds: {cooling_power_per_step:.3e} W")