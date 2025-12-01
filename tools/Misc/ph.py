#!/usr/bin/env python3
import json
import numpy as np
import matplotlib.pyplot as plt
import os
import re

# File paths
terrain_file = "f.json"
movement_file = "f2.json"

# ------------------------------
# Load terrain
# ------------------------------
if not os.path.exists(terrain_file):
    raise FileNotFoundError(f"{terrain_file} not found")

with open(terrain_file, "r") as f:
    terrain_raw = json.load(f)

# Determine max x and y to create a numpy array
max_x = max(int(k) for k in terrain_raw.keys()) + 1
max_y = max(max(int(j) for j in terrain_raw[k].keys()) for k in terrain_raw) + 1

# Build terrain grid
terrain = np.zeros((max_x, max_y))
for i_str, row in terrain_raw.items():
    i = int(i_str)
    for j_str, h in row.items():
        j = int(j_str)
        terrain[i, j] = h

# ------------------------------
# Load tank movements
# ------------------------------
if not os.path.exists(movement_file):
    raise FileNotFoundError(f"{movement_file} not found")

with open(movement_file, "r") as f:
    movements_raw = f.read()

# Extract tank movements using regex
# Pattern: "|<tank_id> tank moved to x,y"
movement_pattern = r"\|(\d+)\s+tank\s+moved\s+to\s+(\d+),(\d+)"
matches = re.findall(movement_pattern, movements_raw)

# Organize movements by tank ID
tank_paths = {}
for tank_id, x_str, y_str in matches:
    tank_id = int(tank_id)
    x, y = int(x_str), int(y_str)
    if tank_id not in tank_paths:
        tank_paths[tank_id] = []
    tank_paths[tank_id].append((x, y))

# ------------------------------
# Plot terrain and tank paths
# ------------------------------
plt.figure(figsize=(10, 8))

# Show terrain
plt.imshow(terrain.T, origin='lower', cmap='terrain', interpolation='nearest')
plt.colorbar(label='Height')

# Plot each tank path
colors = ['red', 'blue', 'yellow', 'cyan', 'magenta']
for idx, (tank_id, path) in enumerate(tank_paths.items()):
    path = np.array(path)
    plt.plot(path[:, 0], path[:, 1], marker='o', color=colors[idx % len(colors)],
             label=f'Tank {tank_id}', linewidth=2, markersize=4)

plt.title("Top-down view of game world with tank movement")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.tight_layout()
plt.show()