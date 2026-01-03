import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import Stefan_Boltzmann as sigma, g, R
from scipy.optimize import fsolve

# ------------------------
# Physical constants
# ------------------------
T_air = 300        # Ambient air temperature (K)
P_air = 101325     # Atmospheric pressure (Pa)
rho_air = 1.2      # Air density (kg/m^3)
k_air = 0.026      # Thermal conductivity of air (W/m K)
nu_air = 1.5e-5    # Kinematic viscosity (m^2/s)
alpha_air = 2.2e-5 # Thermal diffusivity (m^2/s)
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
R_offset = 0.0     # Horizontal offset from flame center

# Heights to evaluate
heights = np.linspace(0.01, 0.6, 50)  # start just above base

# ------------------------
# Function to compute pan temperature at given height
# ------------------------
def pan_temp(h):
    # Air velocity from buoyant plume (simplified)
    # Linearly increases with height above flame
    T_plume = T_air + (T_flame - T_air) * (h / H_flame)  # crude linear approx
    rho_hot = P_air / (R * T_plume)
    v_air = np.sqrt(2 * g * max(rho_air - rho_hot, 0) / rho_air * h)  # m/s

    # Convective heat transfer coefficient using Ra/Nu
    def Tpan_eq(T_pan):
        Ra = g * beta * (T_pan - T_air) * L_pan**3 / (nu_air * alpha_air)
        Nu = 0.54 * Ra**(1/4)
        h_c = Nu * k_air / L_pan
        # Radiation from flame: integrate along flame height
        # Simplified: sum small segments
        n_segments = 20
        z = np.linspace(0, H_flame, n_segments)
        dz = H_flame / n_segments
        Q_rad = np.sum(sigma * epsilon * (T_flame**4 - T_pan**4) * (dz * A_fire / H_flame) / ((h - z)**2 + R_offset**2))
        Q_conv = h_c * (T_pan - T_air)
        return Q_rad - Q_conv
    T_guess = T_air + 50
    T_pan_sol, = fsolve(Tpan_eq, T_guess)
    return T_pan_sol

# Compute pan temperatures
T_pan_list = np.array([pan_temp(h) for h in heights])

# ------------------------
# Plot
# ------------------------
plt.figure(figsize=(8,5))
plt.plot(heights*100, T_pan_list-273, label='Pan Temp (°C)')
plt.xlabel('Height above fire base (cm)')
plt.ylabel('Pan temperature (°C)')
plt.title('Pan Temperature vs Height (Physics-based, no fake peak)')
plt.grid(True)
plt.legend()
plt.show()

print(f"Pan temperature just above flame tip: {T_pan_list[-1]-273:.1f} °C")
print(f"Pan temperature at flame base: {T_pan_list[0]-273:.1f} °C")