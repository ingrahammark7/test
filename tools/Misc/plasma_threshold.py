import json

# Load materials
with open('mat.json', 'r') as f:
    materials = json.load(f)

# Extract steel data
steel = next(m for m in materials if m['name'].lower() == 'steel')
density_steel = steel['density']       # kg/m3
tensile_steel = steel['tensile']       # Pa = J/kg

# Extract nitrogen data
nitrogen = next(m for m in materials if m['name'].lower() == 'nitrogen')
density_nitrogen = nitrogen['density']  # kg/m3
hvl_nitrogen_cm = nitrogen['hvl']['0.5MeV']  # cm

# Constants
area = 1.0                            # m^2
rho_air = 1.225                      # kg/m^3 at sea level (approx)
speed_of_sound = 340                 # m/s at sea level
mach = 30
velocity = mach * speed_of_sound     # m/s

# Mass flow rate (kg/s)
mass_flux = rho_air * velocity * area

# Energy per kg nitrogen kinetic energy (J/kg = Pa equivalence)
energy_per_kg = velocity ** 2

# Total power on surface (W = J/s)
power = mass_flux * energy_per_kg

# Ablation rate (kg/s), energy required to remove 1 kg steel = tensile strength (J/kg)
ablation_rate_kg_per_s = power / tensile_steel

# Ablation rate (m/s thickness)
ablation_rate_m_per_s = ablation_rate_kg_per_s / density_steel

print(f"At Mach {mach} (velocity {velocity:.1f} m/s):")
print(f"Mass flux of nitrogen: {mass_flux:.2f} kg/s per m^2")
print(f"Kinetic energy per kg nitrogen: {energy_per_kg:.2e} J/kg")
print(f"Power on surface: {power:.2e} W/m^2")
print(f"Estimated ablation rate: {ablation_rate_kg_per_s:.4f} kg/s")
print(f"Estimated thickness ablation rate: {ablation_rate_m_per_s*1000:.3f} mm/s")

# --- New calculations ---

# Constants for electron calculations
electron_charge = 1.602e-19  # Coulombs
avogadro = 6.022e23  # atoms/mol

# Atomic info
electrons_per_nitrogen = 7
electrons_per_steel = 26  # Approximate for iron

atomic_mass_nitrogen = 14e-3  # kg/mol
atomic_mass_steel = 55.85e-3  # kg/mol

# Convert HVL from cm to m
hvl_steel_cm = steel['hvl']['0.5MeV']
hvl_steel_m = hvl_steel_cm / 100.0
hvl_nitrogen_m = hvl_nitrogen_cm / 100.0

# Calculate electron removal rate (electrons per second)
atoms_per_sec_nitrogen = (mass_flux / atomic_mass_nitrogen) * avogadro
electrons_removed_per_sec = atoms_per_sec_nitrogen * electrons_per_nitrogen

# Energy per electron removal (0.5 MeV to Joules)
energy_per_electron = 0.5e6 * 1.60218e-19  # J

# Power required to remove electrons (Watts)
power_electron_removal = electrons_removed_per_sec * energy_per_electron

# Ionization time for steel skin layer
volume_steel = area * hvl_steel_m
mass_steel = density_steel * volume_steel
atoms_steel = (mass_steel / atomic_mass_steel) * avogadro
electrons_steel = atoms_steel * electrons_per_steel
time_ionize_steel = electrons_steel / electrons_removed_per_sec

# Ionization time for air layer (1 HVL nitrogen)
volume_air = area * hvl_nitrogen_m
mass_air = density_nitrogen * volume_air
atoms_air = (mass_air / atomic_mass_nitrogen) * avogadro
electrons_air = atoms_air * electrons_per_nitrogen
time_ionize_air = electrons_air / electrons_removed_per_sec

print("\nAdditional ionization and static charge info:")
print(f"Electron removal power: {power_electron_removal:.2e} W")
print(f"Time to ionize steel skin layer: {time_ionize_steel:.2e} s")
print(f"Time to ionize nitrogen air layer: {time_ionize_air:.2e} s")