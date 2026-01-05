import numpy as np

# -----------------------
# PARAMETERS (user adjustable)
# -----------------------
final_crack_length = 1.0       # m, macroscopic crack
steel_density = 7850           # kg/m^3
planck_mass = 2.176e-8         # kg
C = 1e-12                      # Paris law constant
m = 3.0                         # Paris law exponent
delta_sigma = 50e6             # Pa, stress range
da = 1e-5                       # m, crack increment
G_c = 1000                     # J/m², fracture energy of steel
b = 0.01                        # m, plate thickness
f = 1.0                         # Hz, loading frequency
table_steps = 20                # number of table points
max_steps = 1000                # max simulation array size
# -----------------------

# Initial cracks
a0_planck = (planck_mass / steel_density) ** (1/3)
a0_micro = 1e-6                 # 1 μm microcrack

print(f"Initial crack length (Planck-mass): {a0_planck:.2e} m")
print(f"Initial crack length (microcrack 1μm): {a0_micro:.2e} m\n")

# -----------------------
# CRACK GROWTH SIMULATION
# -----------------------
def compute_crack_growth(a0, final_length, da, max_steps=1000):
    if a0 >= final_length:
        return np.array([0.0]), np.array([a0])
    
    num_steps = int(np.ceil((final_length - a0)/da))
    num_steps = min(num_steps, max_steps)   # bound array size
    a_array = np.linspace(a0, final_length, num_steps)
    
    # Paris law growth per cycle
    delta_K = delta_sigma * np.sqrt(np.pi * a_array)
    da_dN = C * delta_K**m
    
    # Avoid division by zero or extremely tiny N
    da_step = (final_length - a0)/num_steps
    dN_array = da_step / da_dN
    N_array = np.cumsum(dN_array)
    t_array = N_array / f
    
    return t_array, a_array

# -----------------------
# PHYSICAL ENERGY
# -----------------------
def energy_physical(a0, final_length, b, G_c):
    crack_area = 2 * b * (final_length - a0)
    return G_c * crack_area

# -----------------------
# COMPUTE FOR BOTH CRACKS
# -----------------------
t_planck, a_planck = compute_crack_growth(a0_planck, final_crack_length, da, max_steps)
t_micro, a_micro = compute_crack_growth(a0_micro, final_crack_length, da, max_steps)

E_total_planck = energy_physical(a0_planck, final_crack_length, b, G_c)
E_total_micro  = energy_physical(a0_micro, final_crack_length, b, G_c)

print(f"Physically realistic energy (Planck-mass crack): {E_total_planck:.2e} J")
print(f"Physically realistic energy (Microcrack): {E_total_micro:.2e} J\n")

# -----------------------
# SUMMARY TABLE FUNCTION
# -----------------------
def print_energy_table(E_total, a_array, label, table_steps=20):
    print(f"--- Energy vs Crack Length ({label}) ---")
    print(f"{'Crack length (m)':>15} | {'Energy (J)':>12}")
    print("-"*30)
    
    a_disp = np.linspace(a_array[0], a_array[-1], table_steps)
    E_disp = np.linspace(0, E_total, table_steps)
    
    for i in range(table_steps):
        print(f"{a_disp[i]:15.6e} | {E_disp[i]:12.2e}")
    print()

# -----------------------
# PRINT TABLES
# -----------------------
print_energy_table(E_total_planck, a_planck, "Planck-mass crack", table_steps)
print_energy_table(E_total_micro, a_micro, "Microcrack 1μm", table_steps)

# -----------------------
# OPTIONAL: SPEED-UP FACTOR (total cycles)
# -----------------------
speedup = (t_planck[-1]/t_micro[-1]) if t_micro[-1] > 0 else np.nan
print(f"Speed-up factor (microcrack vs Planck-mass crack): {speedup:.2e}x\n")