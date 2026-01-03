# Steel vs Graphite electrode lifetime in chloride solution
# Realistic electrolysis current densities

# Constants
F = 96485          # C/mol, Faraday constant
M_Fe = 0.055845    # kg/mol, molar mass of iron
n_Fe = 2           # electrons transferred (Fe -> Fe2+)
rho_steel = 7800   # kg/m^3, density of steel

# Electrode dimensions
length = 0.1       # meters
cross_area_cm2 = 1.0 # cm^2
cross_area_m2 = cross_area_cm2 * 1e-4 # m^2
volume_steel = length * cross_area_m2 # m^3
mass_steel = rho_steel * volume_steel # kg

# Current densities to test (A/cm^2)
current_densities = [0.01, 0.1, 1.0]  # realistic for electrolysis

for i_corr in current_densities:
    I_corr = i_corr * cross_area_cm2  # A
    t_life = (mass_steel * n_Fe * F) / (M_Fe * I_corr)  # seconds
    t_life_minutes = t_life / 60
    t_life_hours = t_life / 3600
    print(f"Steel lifetime at {i_corr:.2f} A/cm²: {t_life_minutes:.1f} min ({t_life_hours:.2f} h)")

# Graphite lifetime approximation
print("Graphite electrode lifetime: Infinite (negligible mass loss)")