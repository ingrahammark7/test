# Synthetic US-like county + logistics network with corrected grid + 3D visualization

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ----------------------------
# PARAMETERS
# ----------------------------
side = 16
N = side * side
steps = 300
dt = 0.1

# ----------------------------
# BUILD "COUNTY GRID" + LOGISTICS NETWORK
# ----------------------------
G = nx.grid_2d_graph(side, side)
G = nx.convert_node_labels_to_integers(G)

# add long-range "highway" edges
for i in range(N):
    for _ in range(2):
        j = np.random.randint(0, N)
        if i != j:
            G.add_edge(i, j)

A = nx.to_numpy_array(G)
deg = A.sum(axis=1, keepdims=True)
deg[deg == 0] = 1
W = A / deg

# ----------------------------
# STATE VARIABLES
# ----------------------------
P = np.zeros(N)
H = np.ones(N) * 0.8
I = np.ones(N) * 0.8

# seed outbreaks
P[np.random.randint(0, N, 5)] = 0.6

# ----------------------------
# PARAMETERS
# ----------------------------
Dp = 0.5
Dh = 0.08
Di = 0.12

r = 0.7
b = 0.02

alpha = 1.1
d1 = 0.8
d2 = 0.5

beta = 0.04
gamma = 0.6
delta = 0.02

def diffuse(W, x):
    return W @ x - x

# ----------------------------
# SIMULATION
# ----------------------------
for t in range(300):

    C = H * I

    dP = Dp * diffuse(W, P)
    dP += r * P * (1 - P) - alpha * C * P

    dH = Dh * diffuse(W, H)
    dH += b * H * (1 - H) - d1 * P * H - d2 * (1 - I) * H

    dI = Di * diffuse(W, I)
    dI += beta * H * (1 - I) - gamma * P * I - delta * I

    P += dt * dP
    H += dt * dH
    I += dt * dI

    P = np.clip(P, 0, 1)
    H = np.clip(H, 0, 1)
    I = np.clip(I, 0, 1)

# ----------------------------
# 2D MAP VIEW
# ----------------------------
final_P = P.reshape(side, side)

plt.figure()
plt.imshow(final_P)
plt.title("Synthetic county pest pressure map")
plt.colorbar()
plt.show()

# ----------------------------
# 3D SURFACE VIEW
# ----------------------------
X = np.arange(side)
Y = np.arange(side)
X, Y = np.meshgrid(X, Y)
Z = final_P

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z)
ax.set_title("3D pest pressure landscape (synthetic US-like network)")
plt.show()

# ----------------------------
# NETWORK VISUALIZATION
# ----------------------------
plt.figure()
nx.draw(G, node_size=10, with_labels=False)
plt.title("Synthetic US-like county + logistics network")
plt.show()