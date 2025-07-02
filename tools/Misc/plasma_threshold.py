import math

# Constants
kB = 1.380649e-23       # Boltzmann constant (J/K)
m_air = 4.65e-26        # Effective mass of air molecule (mostly N2, kg)
ionization_energy_N2 = 15.6 * 1.602e-19  # Ionization energy of nitrogen (J)
Na = 6.022e23           # Avogadro's number
air_density = 1.225     # kg/m³
area = 1.0              # m²
mach_start = 1
mach_end = 100
step = 1
speed_of_sound = 343    # m/s

print(f"{'Mach':<6} {'Speed(m/s)':<12} {'Atoms/s':<14} {'KE per atom (eV)':<20} {'Temp (K)':<10} {'Ionize?'}")
print("-" * 80)

for mach in range(mach_start, mach_end + 1, step):
    v = mach * speed_of_sound
    volume_per_sec = v * area            # m³/s
    mass_per_sec = air_density * volume_per_sec  # kg/s
    atoms_per_sec = mass_per_sec / m_air         # atoms/s

    # Kinetic energy per atom (0.5mv²)
    ke = 0.5 * m_air * v**2
    ke_ev = ke / 1.602e-19

    # Estimate equivalent plasma temperature (in K)
    temp = ke / kB

    ionizes = "Yes" if ke >= ionization_energy_N2 else "No"

    print(f"{mach:<6} {v:<12.1f} {atoms_per_sec:<14.2e} {ke_ev:<20.2f} {temp:<10.0f} {ionizes}")