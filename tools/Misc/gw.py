# Constants
G = 6.67430e-11  # m^3 kg^-1 s^-2
m_p = 1.67262e-27  # kg
d = 1e-15  # m
v = 3e7  # m/s
import math

# Time per crossing
dt = (d**.5)/ v

# Number of crossings per second
f = v / (d**2)

# Calculate instantaneous gravitational force at distance d
de=(d**.5)/f
F_g = G * m_p**2 / de**2

# Total impulse per second (force * total time in 1s)
impulse_per_sec = F_g * dt* f # This should equal F_g


print(f"Instantaneous gravitational force: {F_g:.3e} N")
print(f"Crossing time per event: {dt:.3e} s")
print(f"Crossings per second: {f:.3e}")
print(f"Impulse per second (force*time): {impulse_per_sec:.3e} N·s")

# Number of crossings per second
f1 = v / d
# Total impulse per second (force * total time in 1s)
dt1=d/v
F_g1 = G * m_p**2 / d**2

impulse_per_sec1 = F_g1 * dt1 * f1 # This should equal F_g
ff=math.pow(10,38)
fd=impulse_per_sec/impulse_per_sec1
print(f"Ratio impulse per sec to instantaneous force: {fd:.3f}")
m=math.log10(fd)
print("log ratio")
print(m)
#gravity is 10^44 times stronger than the strong force