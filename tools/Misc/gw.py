import numpy as np
import matplotlib.pyplot as plt

# Shell and barrel parameters
L_shell = 1.0       # shell length in meters
L_barrel = 6.0      # barrel length in meters
A_shell = 0.16      # m^2 surface area of shell
m_shell = 5.0       # kg
c_shell = 1e3       # J/kg·K (specific heat, simplified)
T_gas = 1000        # K temperature difference driving heat
h = 25              # W/m2·K convective coefficient
E_max = 5e6         # Max usable energy in Joules

# Discretize barrel into N segments
N = 1000
dx = L_barrel / N
x = np.linspace(0, L_barrel, N)

# Initialize arrays
E_deposited = np.zeros(N)
v_shell = np.zeros(N)
Q_dot = h * A_shell * T_gas   # constant convective flux for simplicity

# Accumulated energy and velocity
E_acc = 0
for i in range(N):
    # Energy deposited over this segment (scaled to remaining available energy)
    dE = min(Q_dot * dx / (L_barrel / N), E_max - E_acc)
    E_acc += dE
    E_deposited[i] = E_acc
    # Instantaneous velocity from energy
    v_shell[i] = np.sqrt(2 * E_acc / m_shell)

# Plot results
plt.figure(figsize=(10,5))
plt.plot(x, E_deposited/1e6, label='Cumulative Energy (MJ)')
plt.plot(x, v_shell/1000, label='Shell Velocity (km/s)')
plt.axhline(np.sqrt(2*E_max/m_shell)/1000, color='gray', linestyle='--', label='Max Velocity')
plt.xlabel('Barrel Length (m)')
plt.ylabel('Energy / Velocity')
plt.title('Shell Acceleration and Energy Deposition in Barrel')
plt.legend()
plt.grid(True)
plt.show()