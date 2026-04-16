import numpy as np
import matplotlib.pyplot as plt

# Parameters
P = 1.0                 # laser power (W)
absorptivity = 0.3      # fraction absorbed
P_abs = P * absorptivity

r = 0.5e-3              # spot radius (m)
A = np.pi * r**2        # spot area (m^2)

q = P_abs / A          # heat flux (W/m^2)

k = 50.0               # thermal conductivity (W/mK) steel
alpha = 1.2e-5         # thermal diffusivity (m^2/s)

# Time array
t = np.logspace(-4, 2, 300)  # from 0.1 ms to 100 s

# Surface temperature rise
T = (2 * q / k) * np.sqrt(alpha * t / np.pi)

# Plot
plt.figure()
plt.loglog(t, T)
plt.xlabel("Time (s)")
plt.ylabel("Surface temperature rise (K)")
plt.title("Steel surface heating under 1 W laser (1 mm spot)")
plt.grid(True, which="both")
plt.show()

# Print peak at 1 second
t_test = 1.0
T_test = (2 * q / k) * np.sqrt(alpha * t_test / np.pi)
print("Temp rise at 1 s:", T_test, "K")