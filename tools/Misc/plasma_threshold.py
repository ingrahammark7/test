import json

# Load materials
with open('mat.json', 'r') as f:
    materials = json.load(f)

# Extract steel data
steel = next(m for m in materials if m['name'].lower() == 'steel')
density_steel = steel['density']       # kg/m3
tensile_steel = steel['tensile']       # Pa = J/kg

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