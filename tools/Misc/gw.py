import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider

# ---------------------------
# Base parameters
# ---------------------------
E0 = 500.0            # Initial kinetic energy (arbitrary units)
m = 6.0               # Shock multiplier (empirical)
k_att = 0.15          # Attenuation constant (1/cm)
k_v = 1.0             # Cavity volume coefficient
T_list = np.linspace(0, 2, 100)  # Armor thicknesses (arbitrary units)
Delta_max = 0.6       # Max fraction of energy removed by thickest armor
threshold = 0.5       # Fraction of energy loss considered protective

# Armor effect function
def F(T):
    return np.clip(1 - 0.5*T, 0.5, 1.2)

# Energy removed by armor
def energy_post(T, Delta_max):
    return E0 * (1 - np.clip((Delta_max/2)*T, 0, Delta_max))

# Compute trapped energy
def trapped_energy(T, r_yaw, f_eff, L, Delta_max):
    d_yaw = r_yaw / f_eff * F(T)
    d_shock = m * d_yaw
    E_post = energy_post(T, Delta_max)
    E_trapped = E_post * (1 - np.exp(-k_att*(L - d_shock)))
    return E_trapped

# ---------------------------
# Interactive plot with crossover highlight
# ---------------------------
def interactive_plot(r_yaw=1.0, f_eff=0.4, L=30.0):
    E_trap_list = np.array([trapped_energy(T, r_yaw, f_eff, L, Delta_max) for T in T_list])
    E_loss_fraction = 1 - E_trap_list / E0
    
    # Find crossover index (armor just becomes protective)
    idx = np.argmax(E_loss_fraction >= threshold)
    T_crossover = T_list[idx] if idx > 0 else None
    
    plt.figure(figsize=(10,5))
    plt.plot(T_list, E_trap_list, label='Trapped Energy')
    plt.axhline(E0, color='gray', linestyle='--', label='Initial Energy')
    
    # Highlight crossover
    if T_crossover is not None:
        plt.axvline(T_crossover, color='red', linestyle='--', label=f'Crossover ~{T_crossover:.2f}')
    
    plt.xlabel('Armor Thickness (arbitrary units)')
    plt.ylabel('Trapped Energy (arbitrary units)')
    plt.title(f'Yaw={r_yaw} cm, Friction={f_eff}, Medium Thickness={L} cm')
    plt.legend()
    plt.grid(True)
    plt.show()

# Create sliders for r_yaw, f_eff, and L
interact(interactive_plot,
         r_yaw=FloatSlider(value=1.0, min=0.5, max=3.0, step=0.1, description='Yaw Radius (cm)'),
         f_eff=FloatSlider(value=0.4, min=0.1, max=1.0, step=0.05, description='Friction'),
         L=FloatSlider(value=30.0, min=10.0, max=50.0, step=1.0, description='Medium Thickness (cm)'));