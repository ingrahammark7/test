import numpy as np
import matplotlib.pyplot as plt

def diamond_square(size, scale):
    """Generate a fractal terrain using the Diamond-Square algorithm.
    
    size: grid size (must be 2^n + 1)
    scale: initial random range for height variation
    """
    terrain = np.zeros((size, size))
    step = size - 1
    terrain[0, 0] = np.random.uniform(-scale, scale)
    terrain[0, step] = np.random.uniform(-scale, scale)
    terrain[step, 0] = np.random.uniform(-scale, scale)
    terrain[step, step] = np.random.uniform(-scale, scale)

    def diamond_step(x, y, step_size, offset):
        avg = (
            terrain[x, y] +
            terrain[x + step_size, y] +
            terrain[x, y + step_size] +
            terrain[x + step_size, y + step_size]
        ) / 4.0
        terrain[x + step_size//2, y + step_size//2] = avg + offset * np.random.uniform(-1, 1)

    def square_step(x, y, step_size, offset):
        half = step_size // 2
        def avg_surrounding(points):
            vals = []
            for px, py in points:
                if 0 <= px < size and 0 <= py < size:
                    vals.append(terrain[px, py])
            return np.mean(vals) if vals else 0

        # middle of top edge
        terrain[x + half, y] = avg_surrounding([
            (x, y),
            (x + step_size, y),
            (x + half, y - half),
            (x + half, y + half)
        ]) + offset * np.random.uniform(-1, 1)

        # middle of bottom edge
        terrain[x + half, y + step_size] = avg_surrounding([
            (x, y + step_size),
            (x + step_size, y + step_size),
            (x + half, y + step_size - half),
            (x + half, y + step_size + half)
        ]) + offset * np.random.uniform(-1, 1)

        # middle of left edge
        terrain[x, y + half] = avg_surrounding([
            (x, y),
            (x, y + step_size),
            (x - half, y + half),
            (x + half, y + half)
        ]) + offset * np.random.uniform(-1, 1)

        # middle of right edge
        terrain[x + step_size, y + half] = avg_surrounding([
            (x + step_size, y),
            (x + step_size, y + step_size),
            (x + step_size - half, y + half),
            (x + step_size + half, y + half)
        ]) + offset * np.random.uniform(-1, 1)

    while step > 1:
        half_step = step // 2
        # Diamond steps
        for x in range(0, size - 1, step):
            for y in range(0, size - 1, step):
                diamond_step(x, y, step, scale)

        # Square steps
        for x in range(0, size - 1, step):
            for y in range(0, size - 1, step):
                square_step(x, y, step, scale)

        step = half_step
        scale /= 2  # reduce random offset each iteration

    # Normalize terrain to 0-1
    terrain_min = terrain.min()
    terrain_max = terrain.max()
    terrain = (terrain - terrain_min) / (terrain_max - terrain_min)

    return terrain

# Generate fractal terrain on a 257x257 grid (2^8 + 1)
size = 257
terrain = diamond_square(size, scale=1.0)

# Resize terrain to match cloud map size (180x360)
from scipy.ndimage import zoom
terrain_resized = zoom(terrain, (180/size, 360/size))

# Latitude and longitude grids (matching previous example)
lat = np.linspace(-90, 90, 180)
lon = np.linspace(-180, 180, 360)
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Baseline cloud cover modulated by terrain elevation (more clouds over mountains)
baseline_cloud_map = 0.6 * np.exp(-(lat_grid / 40)**2) + 0.2
baseline_cloud_map *= (0.7 + 0.6 * terrain_resized)  # boost cloudiness on high terrain

# Ion molarity localized near China (as before)
center_lat, center_lon = 35, 105
sigma = 15
distance = np.sqrt((lat_grid - center_lat)**2 + (lon_grid - center_lon)**2)
ion_molarity_map = 1e-9 * np.exp(-distance**2 / (2 * sigma**2))

# CCN efficiency function (same as before)
def ccn_efficiency(M, eta_0=1.0, M_crit=1e-9, alpha=1e10):
    excess = np.maximum(0, M - M_crit)
    return eta_0 * np.exp(-alpha * excess)

eta_map = ccn_efficiency(ion_molarity_map)
k_cloud = 0.3
modified_cloud_map = baseline_cloud_map * (1 + k_cloud * (eta_map - 1))

# Plot all together
fig, axs = plt.subplots(1, 3, figsize=(18,6), constrained_layout=True)

im0 = axs[0].imshow(terrain_resized, extent=[-180,180,-90,90], cmap='terrain')
axs[0].set_title('Fractal Terrain Elevation')
axs[0].set_xlabel('Longitude')
axs[0].set_ylabel('Latitude')
plt.colorbar(im0, ax=axs[0], fraction=0.046, pad=0.04)

im1 = axs[1].imshow(baseline_cloud_map, extent=[-180,180,-90,90], cmap='Blues', vmin=0, vmax=1)
axs[1].set_title('Baseline Cloud Cover (with terrain)')
axs[1].set_xlabel('Longitude')
axs[1].set_ylabel('Latitude')
plt.colorbar(im1, ax=axs[1], fraction=0.046, pad=0.04)

im2 = axs[2].imshow(modified_cloud_map, extent=[-180,180,-90,90], cmap='Blues', vmin=0, vmax=1)
axs[2].set_title('Modified Cloud Cover with Ion Effect')
axs[2].set_xlabel('Longitude')
axs[2].set_ylabel('Latitude')
plt.colorbar(im2, ax=axs[2], fraction=0.046, pad=0.04)

plt.suptitle('Synthetic Terrain & Cloud Cover Maps with Weather Control Effect')
plt.show()