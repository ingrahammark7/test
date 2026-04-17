import numpy as np
import matplotlib.pyplot as plt

N = 300
T = 600
dt = 0.1

# State variables
P = np.zeros(N)        # pests
H = np.ones(N) * 0.8   # humans
I = np.ones(N) * 0.8   # infrastructure

# initial pest seed
P[20:30] = 0.4

# diffusion
Dp = 0.6
Dh = 0.1
Di = 0.15

# parameters
r = 0.8

b = 0.02      # human recovery
alpha = 1.3   # suppression strength

d1 = 0.9      # pest impact on humans
d2 = 0.5      # infrastructure dependency

beta = 0.04   # infra build rate
gamma = 0.7   # pest damage to infra
delta = 0.02  # infra decay

def lap(z):
    return np.roll(z,1) + np.roll(z,-1) - 2*z

history_H = []
history_P = []
history_I = []

for t in range(T):

    C = H * I

    # pests
    dP = Dp * lap(P)
    dP += r * P * (1 - P) - alpha * C * P

    # humans
    dH = Dh * lap(H)
    dH += b * H * (1 - H) - d1 * P * H - d2 * (1 - I) * H

    # infrastructure
    dI = Di * lap(I)
    dI += beta * H * (1 - I) - gamma * P * I - delta * I

    P += dt * dP
    H += dt * dH
    I += dt * dI

    P = np.clip(P, 0, 1)
    H = np.clip(H, 0, 1)
    I = np.clip(I, 0, 1)

    if t % 10 == 0:
        history_H.append(H.copy())
        history_P.append(P.copy())
        history_I.append(I.copy())

# Plot human population evolution
plt.figure(figsize=(10,5))
for i, frame in enumerate(history_H):
    plt.plot(frame, alpha=0.2)
plt.title("Human population density (spatial)")
plt.xlabel("Space")
plt.ylabel("H")
plt.show()

# Plot infrastructure
plt.figure(figsize=(10,5))
for i, frame in enumerate(history_I):
    plt.plot(frame, alpha=0.2)
plt.title("Infrastructure density (spatial)")
plt.xlabel("Space")
plt.ylabel("I")
plt.show()

# Plot pests
plt.figure(figsize=(10,5))
for i, frame in enumerate(history_P):
    plt.plot(frame, alpha=0.2)
plt.title("Pest pressure (spatial)")
plt.xlabel("Space")
plt.ylabel("P")
plt.show()