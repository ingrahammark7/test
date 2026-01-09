import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.674e-11                 # gravitational constant, m^3/kg/s^2
ly_to_m = 9.46e15             # 1 light-year in meters
t_yrs = 1e10                  # 10 Gyr
t_s = t_yrs * 3.154e7 * 1e3   # convert years to seconds (approx)
dx = ly_to_m                  # desired displacement: 1 ly

# Required acceleration
a = 2 * dx / t_s**2           # a = 2*dx / t^2

# Distance array in light-years
d_ly = np.logspace(0, 3, 200)  # 1 ly to 1000 ly
d_m = d_ly * ly_to_m

# Required mass for each distance
m_kg = a * d_m**2 / G

# Convert mass to Earth masses for intuition
m_earth = 5.972e24
m_in_earth = m_kg / m_earth

# Plot
plt.figure(figsize=(8,6))
plt.loglog(d_ly, m_in_earth)
plt.xlabel("Distance to perturber (ly)")
plt.ylabel("Required mass (Earth masses)")
plt.title("Mass required to displace a star by 1 ly over 10 Gyr")
plt.grid(True, which="both", ls="--")
plt.show()