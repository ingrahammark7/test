import numpy as np

# -----------------------
# Parameters
# -----------------------
final_crack_length = 0.01
steel_density = 7850
planck_mass = 2.176e-8
C = 1e-12
m = 3.0
delta_sigma = 100e6
da = 1e-8
G_c = 1000
b = 0.01
f = 1.0
table_steps = 20
# -----------------------

# Initial crack lengths
a0_planck = (planck_mass / steel_density) ** (1/3)
a0_micro = 1e-6

print(f"Initial crack length (Planck-mass): {a0_planck:.2e} m")
print(f"Initial crack length (microcrack 1μm): {a0_micro:.2e} m\n")

# Initial growth rates
da_dN_planck = C * (delta_sigma * np.sqrt(np.pi * a0_planck)) ** m
da_dN_micro = C * (delta_sigma * np.sqrt(np.pi * a0_micro)) ** m

print(f"Initial crack growth rate (Planck-mass crack): {da_dN_planck:.2e} m/cycle")
print(f"Initial crack growth rate (microcrack 1μm): {da_dN_micro:.2e} m/cycle\n")

# -----------------------
# Crack growth computation
# -----------------------
def compute_crack_growth(a0, final_length):
    if a0 >= final_length:
        # Already beyond final length
        t_array = np.array([0.0])
        E_array = np.array([0.0])
        a_array = np.array([a0])
        N_array = np.array([0.0])
        P_array = np.array([0.0])
        return N_array, t_array, E_array, a_array, P_array
    
    # Simulate Paris Law
    num_steps = int(np.ceil((final_length - a0) / da))
    a_array = a0 + np.arange(num_steps) * da
    delta_K = delta_sigma * np.sqrt(np.pi * a_array)
    da_dN = C * delta_K ** m
    dN_array = da / da_dN
    N_array = np.cumsum(dN_array)
    
    t_array = N_array / f
    dA_array = 2 * da * b
    dE_array = G_c * dA_array
    E_array = np.cumsum(dE_array)
    
    dt = np.diff(np.insert(t_array, 0, 0))
    P_array = dE_array / dt
    
    return N_array, t_array, E_array, a_array, P_array

# -----------------------
# Compute Planck-mass and microcrack
# -----------------------
N_planck, t_planck, E_planck, a_planck, P_planck = compute_crack_growth(a0_planck, final_crack_length)
N_micro, t_micro, E_micro, a_micro, P_micro = compute_crack_growth(a0_micro, final_crack_length)

# -----------------------
# Summary
# -----------------------
def print_summary(N, E, t, label):
    print(f"--- {label} ---")
    print(f"Total cycles: {N[-1]:.2e}")
    print(f"Total energy released: {E[-1]:.2e} J")
    print(f"Total time (@{f} Hz): {t[-1]:.2e} s\n")

print_summary(N_planck, E_planck, t_planck, "Planck-mass crack")
print_summary(N_micro, E_micro, t_micro, "Microcrack 1μm")

speedup = N_planck[-1] / N_micro[-1] if N_micro[-1] > 0 else np.nan
print(f"Speed-up factor (microcrack vs Planck-mass crack): {speedup:.2e}x\n")

# -----------------------
# Safe table for display
# -----------------------
def print_energy_table_display(E_total, a0, final_length, label, steps=20):
    print(f"--- Time vs Energy vs Crack Length ({label}) ---")
    print(f"{'Time (s)':>12} | {'Energy (J)':>12} | {'Crack length (m)':>15}")
    print("-"*44)
    
    # Interpolate arrays for display
    a_disp = np.linspace(a0, final_length, steps)
    E_disp = np.linspace(0, E_total, steps)
    t_disp = np.linspace(0, 1e6, steps)  # arbitrary scaled time for table readability
    
    for i in range(steps):
        print(f"{t_disp[i]:12.2e} | {E_disp[i]:12.2e} | {a_disp[i]:15.6e}")
    print()

print_energy_table_display(E_planck[-1], a0_planck, final_crack_length, "Planck-mass crack")
print_energy_table_display(E_micro[-1], a0_micro, final_crack_length, "Microcrack 1μm")