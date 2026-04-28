import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# ----------------------------
# physical parameters (iron-like)
# ----------------------------
kB = 1.38e-23
T = 300
a = 2.5e-10

gamma = 0.7
Q = 0.8 * 1.6e-19
nu0 = 1e13

M = (a**2) * nu0 * np.exp(-Q / (kB * T))

# noise strength
sigma = np.sqrt(kB * T)

# ----------------------------
# 2D domain
# ----------------------------
L = 1.0
N_seeds = 80

points = np.random.rand(N_seeds, 2) * L
vor = Voronoi(points)

# ----------------------------
# grid representation
# ----------------------------
gridN = 200
x = np.linspace(0, L, gridN)
y = np.linspace(0, L, gridN)
X, Y = np.meshgrid(x, y)

# assign initial grain labels (nearest seed)
def assign_grains(points):
    grid = np.zeros((gridN, gridN), dtype=int)
    for i in range(gridN):
        for j in range(gridN):
            p = np.array([X[i,j], Y[i,j]])
            d = np.sum((points - p)**2, axis=1)
            grid[i,j] = np.argmin(d)
    return grid

grid = assign_grains(points)

# ----------------------------
# curvature approximation
# ----------------------------
def curvature(field):
    gx, gy = np.gradient(field.astype(float))
    gnorm = np.sqrt(gx**2 + gy**2 + 1e-12)
    nx, ny = gx/gnorm, gy/gnorm
    nx_x, _ = np.gradient(nx)
    _, ny_y = np.gradient(ny)
    return nx_x + ny_y

# ----------------------------
# evolution loop
# ----------------------------
steps = 50

for t in range(steps):

    # indicator field for boundaries
    boundary = np.zeros_like(grid, dtype=float)

    boundary[1:] += (grid[1:] != grid[:-1])
    boundary[:-1] += (grid[:-1] != grid[1:])
    boundary[:,1:] += (grid[:,1:] != grid[:,:-1])
    boundary[:,:-1] += (grid[:,:-1] != grid[:,1:])

    # curvature proxy
    kappa = curvature(boundary)

    # thermal noise
    noise = sigma * np.random.randn(gridN, gridN)

    # interface motion probability
    motion = M * gamma * kappa + noise

    # stochastic boundary updates
    flip = motion > np.percentile(motion, 99)

    # random grain relabeling at boundaries
    idx = np.argwhere(flip)

    for i,j in idx:
        if i > 0 and j > 0 and i < gridN-1 and j < gridN-1:
            neighbors = [
                grid[i+1,j], grid[i-1,j],
                grid[i,j+1], grid[i,j-1]
            ]
            grid[i,j] = np.random.choice(neighbors)

# ----------------------------
# visualize final structure
# ----------------------------
plt.imshow(grid, cmap='tab20')
plt.title("2D Voronoi + curvature + thermal grain evolution")
plt.axis('off')
plt.show()