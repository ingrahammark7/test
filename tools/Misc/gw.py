import numpy as np
import matplotlib.pyplot as plt

N = 300
T = 600
dt = 0.1

# State variables
P = np.zeros(N)
H = np.ones(N)

# Initial pest seed
P[10:20] = 0.4

# Parameters
Dp = 0.6
Dh = 0.15

r = 0.8

alpha = 1.5   # control effectiveness
beta = 0.03   # infrastructure recovery
gamma = 0.8   # pest damage to infrastructure

eta = 1.2     # nonlinearity of control production

def lap(z):
    return np.roll(z,1) + np.roll(z,-1) - 2*z

history_control = []

for t in range(T):

    # derive control from infrastructure
    C = H ** eta

    # pest dynamics
    dP = Dp * lap(P)
    dP += r * P * (1 - P) - alpha * C * P

    # infrastructure dynamics
    dH = Dh * lap(H)
    dH += beta * (1 - H) - gamma * P * H

    P += dt * dP
    H += dt * dH

    P = np.clip(P, 0, 1)
    H = np.clip(H, 0, 1)

    if t % 10 == 0:
        history_control.append((H ** eta).copy())

# Plot control evolution
plt.figure(figsize=(10,5))
for i, frame in enumerate(history_control):
    plt.plot(frame, alpha=0.3 + 0.7*i/len(history_control))

plt.title("Effective control (derived from infrastructure)")
plt.xlabel("Space")
plt.ylabel("Control level")
plt.show()