import numpy as np

# -----------------------
# PARAMETERS
# -----------------------
final_crack_length = 1.0      # m
steel_density = 7850          # kg/m^3
planck_mass = 2.176e-8        # kg
C = 1e-12
m = 3.0
delta_sigma = 50e6            # Pa
da = 1e-5                     # m
G_c = 1000                    # J/m²
E_mod = 210e9                 # Pa
nu = 0.3
b = 0.01                       # m, plate thickness
f = 1.0
table_steps = 20
max_steps = 1000
lattice_spacing = 2.5e-10      # m, Fe
E_coh = 6.9e-19                # J per bond
# -----------------------

# Initial cracks
a0_planck = (planck_mass / steel_density) ** (1/3)
a0_micro = 1e-6

print(f"Initial crack length (Planck-mass): {a0_planck:.2e} m")
print(f"Initial crack length (microcrack 1μm): {a0_micro:.2e} m\n")

# -----------------------
# Crack growth (Paris law)
# -----------------------
def compute_crack_growth(a0, final_length, da, max_steps=1000):
    if a0 >= final_length:
        return np.array([0.0]), np.array([a0])
    num_steps = int(np.ceil((final_length - a0)/da))
    num_steps = min(num_steps, max_steps)
    a_array = np.linspace(a0, final_length, num_steps)
    delta_K = delta_sigma * np.sqrt(np.pi * a_array)
    da_dN = C * delta_K**m
    da_step = (final_length - a0)/num_steps
    dN_array = da_step / da_dN
    N_array = np.cumsum(dN_array)
    t_array = N_array / f
    return t_array, a_array

# -----------------------
# Energy calculation
# -----------------------
def energy_total(a_array, b, G_c, sigma, E_mod, lattice_spacing, E_coh):
    E_surface = G_c * 2 * b * a_array
    K = sigma * np.sqrt(np.pi * a_array)
    E_prime = E_mod
    G_elastic = K**2 / E_prime
    E_elastic = G_elastic * 2 * b * a_array
    E_total = E_surface + E_elastic

    # Energy per bond and ratio to cohesive
    atoms_surface = 2 * b * a_array / lattice_spacing**2
    E_per_bond = E_total / atoms_surface
    ratio_to_cohesive = E_per_bond / E_coh

    return E_surface, E_elastic, E_total, ratio_to_cohesive

# -----------------------
# Compute for both cracks
# -----------------------
t_planck, a_planck = compute_crack_growth(a0_planck, final_crack_length, da, max_steps)
t_micro, a_micro = compute_crack_growth(a0_micro, final_crack_length, da, max_steps)

E_surf_planck, E_elast_planck, E_tot_planck, ratio_planck = energy_total(
    a_planck, b, G_c, delta_sigma, E_mod, lattice_spacing, E_coh)

E_surf_micro, E_elast_micro, E_tot_micro, ratio_micro = energy_total(
    a_micro, b, G_c, delta_sigma, E_mod, lattice_spacing, E_coh)

# -----------------------
# Table function
# -----------------------
def print_energy_table(a_array, E_surface, E_elastic, E_total, ratio_to_coh, label, steps=20):
    print(f"--- Energy vs Crack Length ({label}) ---")
    print(f"{'Crack length (m)':>15} | {'Surface (J)':>12} | {'Elastic (J)':>12} | {'Total (J)':>12} | {'E/bond / E_coh':>15}")
    print("-"*85)
    a_disp = np.linspace(a_array[0], a_array[-1], steps)
    E_s_disp = np.linspace(E_surface[0], E_surface[-1], steps)
    E_e_disp = np.linspace(E_elastic[0], E_elastic[-1], steps)
    E_t_disp = np.linspace(E_total[0], E_total[-1], steps)
    ratio_disp = np.linspace(ratio_to_coh[0], ratio_to_coh[-1], steps)
    for i in range(steps):
        print(f"{a_disp[i]:15.6e} | {E_s_disp[i]:12.2e} | {E_e_disp[i]:12.2e} | {E_t_disp[i]:12.2e} | {ratio_disp[i]:15.2e}")
    print()

# -----------------------
# Print tables
# -----------------------
print_energy_table(a_planck, E_surf_planck, E_elast_planck, E_tot_planck, ratio_planck, "Planck-mass crack")
print_energy_table(a_micro, E_surf_micro, E_elast_micro, E_tot_micro, ratio_micro, "Microcrack 1μm")