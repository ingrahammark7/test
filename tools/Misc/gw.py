import numpy as np

# -----------------------------
# Material properties for steel
# -----------------------------
rho_steel = 7850       # kg/m^3
C_steel = 460          # J/(kg*K)
E_steel = 210e9        # Pa, Young's modulus
beta = 0.9             # fraction of energy converted to heat

# -----------------------------
# Crack and loading parameters
# -----------------------------
sigma_applied = 100e6  # Pa, applied stress
rho_tip = 0.3e-9       # m, atomic-scale crack tip radius

# Crack lengths from 1 µm to 10 cm
a_vals = np.logspace(-6, -1, 200)

# Crack velocities to test (m/s)
v_crack_vals = [1, 500, 5000]  # low, medium, Mach 1

# -----------------------------
# Function: dynamic crack tip temperature with explicit velocity
# -----------------------------
def crack_tip_temp_dynamic_velocity(a, v_crack):
    """
    Compute tip temperature including velocity effects.
    
    Parameters:
        a : float or np.array
            Crack half-length [m]
        v_crack : float
            Crack tip velocity [m/s]
            
    Returns:
        delta_T : float or np.array
            Temperature rise [K]
    """
    # Stress intensity factor
    K = sigma_applied * np.sqrt(np.pi * a)
    # Energy release rate
    G = K**2 / E_steel
    # Characteristic deposition time over tip radius
    t_dep = rho_tip / v_crack
    # Tip area
    tip_area = rho_tip**2
    # Power density
    power_density = G * v_crack / tip_area
    # Temperature rise
    delta_T = beta * power_density * t_dep / (rho_steel * C_steel)
    return delta_T

# -----------------------------
# Compute critical crack length for ΔT >= 1000 K
# -----------------------------
target_delta_T = 1000  # K

for v in v_crack_vals:
    delta_T_vals = crack_tip_temp_dynamic_velocity(a_vals, v)
    idx = np.argmax(delta_T_vals >= target_delta_T)
    critical_crack_length = a_vals[idx]
    print(f"Crack velocity = {v} m/s -> Critical crack length for ΔT >= 1000 K: {critical_crack_length:.2e} m, ΔT = {delta_T_vals[idx]:.1f} K")

# Optional: print first few temperatures
print("\nSample tip temperatures for a few crack lengths at Mach 1:")
delta_T_vals = crack_tip_temp_dynamic_velocity(a_vals, 5000)
for i in range(5):
    print(f"  a = {a_vals[i]*1e6:.3f} µm, ΔT = {delta_T_vals[i]:.1f} K")