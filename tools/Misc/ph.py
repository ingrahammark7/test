import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import re
import os
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D

# ------------------------------
# Load terrain
# ------------------------------
terrain_file = "f.json"
movement_file = "f2.json"

with open(terrain_file, "r") as f:
    terrain_raw = json.load(f)

terrain_sparse = {}
max_i = 0
max_j = 0
for i_str, row in terrain_raw.items():
    i = int(i_str)
    max_i = max(max_i, i)
    for j_str, h in row.items():
        j = int(j_str)
        max_j = max(max_j, j)
        terrain_sparse.setdefault(i, {})[j] = h

# Downsample for speed
max_display_rows = 150
max_display_cols = 150
row_factor = max(1, max_i // max_display_rows)
col_factor = max(1, max_j // max_display_cols)
display_rows = (max_i + row_factor - 1)//row_factor
display_cols = (max_j + col_factor - 1)//col_factor

# Fill display array
display_terrain = np.zeros((display_rows, display_cols), dtype=np.float32)
for i, row in terrain_sparse.items():
    di = i // row_factor
    if di >= display_rows: continue
    for j, h in row.items():
        dj = j // col_factor
        if dj >= display_cols: continue
        display_terrain[di, dj] = h
# Propagate missing values
for i in range(display_rows):
    last = 1e-6
    for j in range(display_cols):
        if display_terrain[i,j] == 0:
            display_terrain[i,j] = last
        else:
            last = display_terrain[i,j]
for j in range(display_cols):
    last = 1e-6
    for i in range(display_rows):
        if display_terrain[i,j] == 0:
            display_terrain[i,j] = last
        else:
            last = display_terrain[i,j]

# Scale down spikes for performance
display_terrain *= 0.3

# ------------------------------
# Load tank movements
# ------------------------------
with open(movement_file, "r") as f:
    movements_raw = f.read()
pattern = r"\|(\d+)\s+tank\s+moved\s+to\s+(\d+),(\d+)"
matches = re.findall(pattern, movements_raw)

tank_paths = {}
for (tank_id, x_str, y_str) in matches:
    tank_id = int(tank_id)
    x, y = int(x_str), int(y_str)
    tank_paths.setdefault(tank_id, []).append((x, y))

# ------------------------------
# Tkinter window
# ------------------------------
root = tk.Tk()
root.title("3D Terrain Visualization")

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Terrain surface
X, Y = np.meshgrid(np.arange(display_cols), np.arange(display_rows))
terrain_surf = ax.plot_surface(X, Y, display_terrain, cmap=cm.terrain,
                               linewidth=0, antialiased=False)

# ------------------------------
# Tanks
# ------------------------------
colors = ['red','blue','yellow','cyan','magenta','orange','green','purple']
trail_length = 10
tank_dots = {}
tank_trails = {}

for idx, tank_id in enumerate(sorted(tank_paths.keys())):
    dot, = ax.plot([], [], [], 'o', color=colors[idx%len(colors)], markersize=6)
    trail, = ax.plot([], [], [], color=colors[idx%len(colors)], linewidth=1)
    tank_dots[tank_id] = dot
    tank_trails[tank_id] = trail

max_steps = max(len(path) for path in tank_paths.values())

# ------------------------------
# Camera setup
# ------------------------------
def set_default_view():
    ax.view_init(elev=60, azim=-60)
    ax.set_xlim(0, display_cols)
    ax.set_ylim(0, display_rows)
    ax.set_zlim(0, np.max(display_terrain)*1.5)

set_default_view()

# ------------------------------
# Update frame
# ------------------------------
def update_frame(frame):
    for tank_id, path in tank_paths.items():
        step = min(frame, len(path)-1)
        x_vals = []
        y_vals = []
        z_vals = []
        start_idx = max(0, step-trail_length)
        for s in range(start_idx, step+1):
            x, y = path[s]
            xi = int(x // row_factor)
            yi = int(y // col_factor)
            zi = display_terrain[xi, yi] + 0.5
            x_vals.append(yi)
            y_vals.append(xi)
            z_vals.append(zi)
        tank_trails[tank_id].set_data(x_vals, y_vals)
        tank_trails[tank_id].set_3d_properties(z_vals)
        if z_vals:
            tank_dots[tank_id].set_data([x_vals[-1]], [y_vals[-1]])
            tank_dots[tank_id].set_3d_properties([z_vals[-1]])
    canvas.draw_idle()

# ------------------------------
# Slider
# ------------------------------
def on_slider_change(val):
    frame = int(float(val))
    update_frame(frame)

slider = tk.Scale(root, from_=0, to=max_steps, orient=tk.HORIZONTAL,
                  length=600, label="Time step", command=on_slider_change)
slider.pack(side=tk.BOTTOM)

# ------------------------------
# Reset view button
# ------------------------------
def reset_view():
    set_default_view()
    canvas.draw_idle()

btn = tk.Button(root, text="Reset View", command=reset_view)
btn.pack(side=tk.BOTTOM)

# ------------------------------
# Auto-play loop
# ------------------------------
auto_play = True
def autoplay_loop():
    if auto_play:
        val = slider.get()
        if val < max_steps:
            slider.set(val+1)
            root.after(150, autoplay_loop)
        else:
            slider.set(0)
            root.after(150, autoplay_loop)

if auto_play:
    root.after(200, autoplay_loop)

root.mainloop()