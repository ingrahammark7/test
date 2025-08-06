import numpy as np
import matplotlib.pyplot as plt

# Parameters
grid_size = 100
p_collapse = 0.05      # Base collapse spread probability per neighbor
p_recovery = 0.01      # Recovery probability per collapsed cell
rho = 0.1              # Refugees generated per collapsed cell per timestep
alpha = 1.0            # Refugee absorption capacity per stable cell
beta = 0.02            # Increase in collapse chance per excess refugee unit
timesteps = 200

# Initialize grid: start mostly stable with a small collapsed region in center
grid = np.zeros((grid_size, grid_size), dtype=int)
center = grid_size // 2
grid[center-2:center+3, center-2:center+3] = 1  # initial collapsed zone

refugees = 0.0
refugee_history = []
stable_history = []
collapsed_history = []

def get_neighbors(x, y, size):
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size:
                neighbors.append((nx, ny))
    return neighbors

for t in range(timesteps):
    new_grid = grid.copy()
    stable_cells = np.sum(grid == 0)
    collapsed_cells = np.sum(grid == 1)
    
    # Update refugee count
    refugees += rho * collapsed_cells
    absorption_capacity = alpha * stable_cells
    excess_refugees = max(0, refugees - absorption_capacity)
    
    for x in range(grid_size):
        for y in range(grid_size):
            if grid[x, y] == 0:  # stable cell
                # Check neighbors for collapse influence
                neighbors = get_neighbors(x, y, grid_size)
                collapsed_neighbors = sum(grid[nx, ny] for (nx, ny) in neighbors)
                # Base collapse chance from neighbors
                collapse_chance = 1 - (1 - p_collapse) ** collapsed_neighbors
                # Increase collapse chance if refugee pressure exists
                collapse_chance += beta * excess_refugees
                collapse_chance = min(1.0, collapse_chance)
                
                if np.random.rand() < collapse_chance:
                    new_grid[x, y] = 1
                    
            else:  # collapsed cell
                if np.random.rand() < p_recovery:
                    new_grid[x, y] = 0
    
    # Some refugees are resettled proportional to recovered area
    recovered_cells = np.sum((grid == 1) & (new_grid == 0))
    refugees = max(0, refugees - recovered_cells * alpha * 0.1)
    
    grid = new_grid
    
    stable_history.append(np.sum(grid == 0))
    collapsed_history.append(np.sum(grid == 1))
    refugee_history.append(refugees)

# Plot results
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(stable_history, label='Stable cells')
plt.plot(collapsed_history, label='Collapsed cells')
plt.xlabel('Time step')
plt.ylabel('Number of cells')
plt.legend()
plt.title('Stable vs Collapsed Zones Over Time')

plt.subplot(1, 2, 2)
plt.plot(refugee_history, color='orange')
plt.xlabel('Time step')
plt.ylabel('Refugees (arbitrary units)')
plt.title('Refugee Population Over Time')

plt.tight_layout()
plt.show()