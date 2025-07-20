import numpy as np
import math

# Constants
c = 3e8  # m/s
h = 6.626e-34  # J*s
proton_mass = 1.67e-27  # kg
atomic_radius = 1e-10  # m
pc = 6 * 10**-34

# Energies
E_proton = proton_mass * c**2
N = int((E_proton / pc) * 1e34)  # Target photon number

# Parameters
splitting_efficiency = 0.95   # 95% energy goes into photons, 5% lost as heat per splitting
cooling_efficiency = 0.7      # 70% of cooling power removes heat effectively
cooling_power_max = 1e3       # Watts, max cooling power available (adjustable)
splitting_time_per_step = 0.01  # seconds per splitting step

# Initialize variables
photon_count = 1
photon_energy = E_proton
heat_accumulated = 0.0  # Joules
total_time = 0.0

# Calculate total steps
steps = math.ceil(math.log2(N))

print(f"Target photons: {N}, steps required: {steps}")

for step in range(1, steps + 1):
    # Splitting phase
    new_photon_count = photon_count * 2
    new_photon_energy = photon_energy / 2
    
    # Energy before splitting
    energy_before = photon_count * photon_energy
    # Energy after splitting (photons)
    energy_after = new_photon_count * new_photon_energy * splitting_efficiency
    
    # Heat generated in splitting (loss)
    heat_generated = energy_before - energy_after
    heat_accumulated += heat_generated
    
    # Update photons
    photon_count = new_photon_count
    photon_energy = new_photon_energy
    
    # Add splitting time
    total_time += splitting_time_per_step
    
    # Cooling phase
    # Cooling power effective
    effective_cooling_power = cooling_power_max * cooling_efficiency
    
    # Cooling time needed to remove heat
    cooling_time = heat_accumulated / effective_cooling_power
    
    # Update time with cooling
    total_time += cooling_time
    
    # Heat removed
    heat_accumulated = 0.0  # Assume full heat removal before next step
    
    print(f"Step {step}: photons={photon_count:.3e}, photon_energy={photon_energy:.3e} J, "
          f"heat_generated={heat_generated:.3e} J, cooling_time={cooling_time:.3e} s, total_time={total_time:.3e} s")

# Final photon density in atomic volume
V = 4 / 3 * np.pi * atomic_radius**3
photon_density = photon_count / V
print(f"\nFinal photon count: {photon_count:.3e}")
print(f"Final photon energy: {photon_energy:.3e} J")
print(f"Photon density in atomic radius volume: {photon_density:.3e} photons/m^3")
print(f"Total process time: {total_time:.3e} seconds (~{total_time/3600:.3f} hours)")