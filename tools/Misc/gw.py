import numpy as np

# iron parameters (order-of-magnitude)
gamma = 0.7
kB = 1.38e-23
Q = 0.8 * 1.6e-19
M0 = 1e-4

T_hot = 1200   # processing temperature
T_cool = 300
t_hot = 10**4  # seconds hot stage

# mobility at hot stage
M = M0 * np.exp(-Q / (kB * T_hot))

# arrested grain size scale
R = np.sqrt(M * gamma * t_hot)

print("final grain size (m):", R)
print("final grain size (microns):", R*1e6)