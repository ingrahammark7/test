import numpy as np
import matplotlib.pyplot as plt

# parameters
p_per_shot = 0.02
fire_rate = 2.0
theta = 0.5  # radian engagement tracking window

def success_prob(h, v):
    # angular velocity approx v/h
    omega = v / h
    T = theta / omega  # engagement window
    n_shots = max(0, T * fire_rate)
    # probability of at least one hit
    return 1 - (1 - p_per_shot) ** n_shots

# grid
heights = np.linspace(5, 100, 60)   # meters
speeds = np.linspace(5, 25, 60)     # m/s

Z = np.zeros((len(heights), len(speeds)))

for i, h in enumerate(heights):
    for j, v in enumerate(speeds):
        Z[i, j] = success_prob(h, v)

plt.figure()
plt.imshow(Z, origin='lower', extent=[5,25,5,100], aspect='auto')
plt.xlabel("Drone speed (m/s)")
plt.ylabel("Altitude (m)")
plt.title("Interception Probability Threshold Map (Pistol Engagement Model)")
plt.colorbar()
plt.show()

Z.mean()