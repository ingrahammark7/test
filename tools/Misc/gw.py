import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# physical constants (iron-like)
# ----------------------------
kB = 1.38e-23
T = 300
a = 2.5e-10

gamma = 0.7
Q = 0.8 * 1.6e-19
nu0 = 1e13

# mobility from atomic hopping
M = (a**2) * nu0 * np.exp(-Q / (kB * T))

# ----------------------------
# initial grain distribution
# (broad but not biasing result)
# ----------------------------
N = 300
R = np.random.lognormal(mean=np.log(100e-9), sigma=0.5, size=N)

dt = 1e3
steps = 600

mean_R = []

# ----------------------------
# evolution loop (grain competition)
# ----------------------------
for t in range(steps):

    R_avg = np.mean(R)

    dR = M * gamma * (1/R_avg - 1/R)

    R += dt * dR

    R = np.clip(R, a, None)

    mean_R.append(np.mean(R))

# ----------------------------
# plot
# ----------------------------
plt.plot(np.array(mean_R)*1e9)
plt.xlabel("time step")
plt.ylabel("mean grain size (nm)")
plt.title("Competing grain network evolution (pure curvature + hopping)")
plt.show()