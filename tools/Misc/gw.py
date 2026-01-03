import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import Stefan_Boltzmann as sigma, g, R
from scipy.optimize import fsolve

# ------------------------
# Physical constants
# ------------------------
T_air = 300        # Ambient air (K)
P_air = 101325     # Atmospheric pressure (Pa)
rho_air = 1.2      # Air density (kg/m^3)
k_air = 0.026      # Thermal conductivity air (W/m K)
nu_air = 1.5e-5    # Kinematic viscosity (m^2/s)
alpha_air = 2.2e-5 # Thermal diffusivity air (m^2/s)
beta = 1 / T_air   # Thermal expansion coefficient (1/K)

# ------------------------
# Fire and pan parameters
# ------------------------
H_flame = 0.3      # Flame height (m)
T_flame = 1000     # Flame temperature (K)
epsilon = 0.8      # Pan emissivity
A_fire = 0.05      # Flame projected area (m^2)
A_pan = 0.1        # Pan area facing flame (m^2)
L_pan = 0.2        # Pan characteristic length (m)
R_offset = 0.0     # Horizontal offset from flame center (m)

# Heights to evaluate
heights = np.linspace(0.05, 0.6, 50)

# ------------------------
# Function to compute pan temperature at given height
# ------------------------
def pan_temp(h):
    # Natural convection: air velocity from buoyant plume
    # Approximate air temperature in plume linearly
    T_plume = T_air + (T_flame - T_air) * (1 - np.exp(-3*h/H_flame))
    rho_hot = P_air / (R * T_plume)
    v_air = np.sqrt(2 * g * (rho_air - rho_hot)/rho_air * h)  # m/s

    # Convective heat transfer coefficient from Ra number
    def Tpan_eq(T_pan):
        Ra = g * beta * (T_pan - T_air) * L_pan**3 / (nu_air * alpha_air)
        Nu = 0.54 * Ra**(1/4)
        h_c = Nu * k_air / L_pan
        # Radiative flux from flame as line source
        Q_rad = sigma * epsilon * (T_flame**4 - T_pan**4) * (A_fire / A_pan) / ((h - H_flame/2)**2 + R_offset**2)**0.5
        Q_conv = h_c * (T_pan - T_air)
        return Q_rad - Q_conv
    T_guess = 400   # K
    T_pan_sol, = fsolve(Tpan_eq, T_guess)
    return T_pan_sol

# Compute temperatures
T_pan_list = np.array([pan_temp(h) for h in heights])

# Find optimum height
idx_opt = np.argmax(T_pan_list)
h_opt = heights[idx_opt]
T_opt = T_pan_list[idx_opt]

print(f"Optimal pan height: {h_opt*100:.1f} cm")
print(f"Max pan temperature: {T_opt-273:.1f} °C")

# ------------------------
# Plot
# ------------------------
plt.figure(figsize=(8,5))
plt.plot(heights*100, T_pan_list-273, label='Pan Temp (°C)')
plt.axvline(h_opt*100, color='r', linestyle='--', label=f'Opt Height: {h_opt*100:.1f} cm')
plt.xlabel('Height above fire base (cm)')
plt.ylabel('Pan temperature (°C)')
plt.title('Pan Temperature vs Height (Physics-based)')
plt.grid(True)
plt.legend()
plt.show()