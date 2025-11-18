import json
import time
import numpy as np
from tqdm import tqdm  # progress bar

# ----------------------
# Pure Python Perlin 2D
# ----------------------
import math
import random

# Permutation table
perm = list(range(256))
random.seed(42)
random.shuffle(perm)
perm += perm  # repeat to avoid overflow

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(a, b, t):
    return a + t * (b - a)

def grad(hash, x, y):
    h = hash & 3
    u = x if h & 2 == 0 else -x
    v = y if h & 1 == 0 else -y
    return u + v

def perlin(x, y):
    xi = int(math.floor(x)) & 255
    yi = int(math.floor(y)) & 255

    xf = x - math.floor(x)
    yf = y - math.floor(y)

    u = fade(xf)
    v = fade(yf)

    aa = perm[perm[xi] + yi]
    ab = perm[perm[xi] + yi + 1]
    ba = perm[perm[xi + 1] + yi]
    bb = perm[perm[xi + 1] + yi + 1]

    x1 = lerp(grad(aa, xf, yf), grad(ba, xf - 1, yf), u)
    x2 = lerp(grad(ab, xf, yf - 1), grad(bb, xf - 1, yf - 1), u)

    return lerp(x1, x2, v)

# ----------------------
# Terrain Parameters
# ----------------------
grid_size_x = 512   # smaller for testing; scale up as needed
grid_size_y = 512
scale = 50.0
octaves = 4
persistence = 0.5
lacunarity = 2.0

terrain = np.zeros((grid_size_x, grid_size_y), dtype=np.float32)

# ----------------------
# Timer + Progress
# ----------------------
start_time = time.time()
for i in tqdm(range(grid_size_x), desc="Generating Perlin terrain"):
    for j in range(grid_size_y):
        value = 0.0
        amp = 1.0
        freq = 1.0 / scale
        max_amp = 0.0
        x = i * freq
        y = j * freq
        for o in range(octaves):
            value += perlin(x, y) * amp
            max_amp += amp
            amp *= persistence
            freq *= lacunarity
            x = i * freq
            y = j * freq
        terrain[i, j] = value / max_amp

end_time = time.time()
print(f"Perlin terrain generated in {end_time - start_time:.2f} seconds")

# ----------------------
# Export to JSON
# ----------------------
terrain_list = terrain.tolist()
with open("perlin_terrain.json", "w") as f:
    json.dump(terrain_list, f)

print("Terrain exported to perlin_terrain.json")