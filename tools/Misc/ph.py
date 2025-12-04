import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import os
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.collections import LineCollection

# ------------------------------
# Files
# ------------------------------
terrain_file = "f.json"
movement_file = "f2.json"
shot_file = "f3.json"  # optional

# ------------------------------
# Load terrain
# ------------------------------
with open(terrain_file, "r") as f:
    terrain_raw = json.load(f)

max_i = max_j = 0
terrain_sparse = {}
for i_str, row in terrain_raw.items():
    i = int(i_str)
    max_i = max(max_i, i)
    terrain_sparse[i] = {}
    for j_str, h in row.items():
        j = int(j_str)
        max_j = max(max_j, j)
        terrain_sparse[i][j] = h
max_i += 1
max_j += 1

# ------------------------------
# Load tank movements
# ------------------------------
import re
with open(movement_file, "r") as f:
    movements_raw = f.read()
pattern = r"\|(\d+)\s+tank\s+moved\s+to\s+(\d+),(\d+)"
matches = re.findall(pattern, movements_raw)

tank_paths = {}
for tank_id, x_str, y_str in matches:
    tank_id = int(tank_id)
    x, y = int(x_str), int(y_str)
    tank_paths.setdefault(tank_id, []).append((x, y))

# ------------------------------
# Load optional shots
# ------------------------------
shots = []
if os.path.exists(shot_file):
    with open(shot_file, "r") as f:
        raw = f.read()
    shot_pattern = r"\|(\d+),(\d+),(\d+),(\d+)"
    shots = [tuple(map(int, m)) for m in re.findall(shot_pattern, raw)]

# ------------------------------
# Display parameters
# ------------------------------
screen_rows, screen_cols = 400, 400
rows_factor = max(1, max_i // screen_rows)
cols_factor = max(1, max_j // screen_cols)
display_rows = (max_i + rows_factor - 1) // rows_factor
display_cols = (max_j + cols_factor - 1) // cols_factor
scale_x = display_rows / max_i
scale_y = display_cols / max_j

# ------------------------------
# Fill terrain for display
# ------------------------------
display_terrain = np.full((display_rows, display_cols), 1e-6, dtype=np.float32)
for i, row in terrain_sparse.items():
    di = i // rows_factor
    if di >= display_rows: continue
    for j, h in row.items():
        dj = j // cols_factor
        if dj >= display_cols: continue
        display_terrain[di, dj] = h
# propagate row-wise and column-wise to fill gaps
for i in range(display_rows):
    display_terrain[i, :] = np.maximum.accumulate(display_terrain[i, :])
for j in range(display_cols):
    display_terrain[:, j] = np.maximum.accumulate(display_terrain[:, j])

# ------------------------------
# Tkinter setup
# ------------------------------
root = tk.Tk()
root.title("Tank Game Visualization")

fig, ax = plt.subplots(figsize=(6,6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

im = ax.imshow(display_terrain.T, origin='lower', cmap='terrain',
               interpolation='nearest', norm=LogNorm(vmin=np.min(display_terrain), vmax=np.max(display_terrain)))
plt.colorbar(im, ax=ax, label="Height (log scale)")

# ------------------------------
# Tank visualization (optimized)
# ------------------------------
colors = ['red','blue','yellow','cyan','magenta','orange','green','purple']
tank_lines = {}
tank_dots = {}
trail_length = 20

for idx, tank_id in enumerate(sorted(tank_paths.keys())):
    # Using LineCollection for efficiency
    segments = [np.zeros((2,2))]  # dummy initial segment
    lc = LineCollection(segments, color=colors[idx%len(colors)], linewidths=2)
    ax.add_collection(lc)
    tank_lines[tank_id] = lc
    dot, = ax.plot([], [], 'o', color=colors[idx%len(colors)], markersize=6)
    tank_dots[tank_id] = dot

# ------------------------------
# Shots visualization
# ------------------------------
permanent_shots = True
proximity_radius = 3
if permanent_shots:
    for (x1,y1,x2,y2) in shots:
        ax.plot([x1*scale_x, x2*scale_x],[y1*scale_y, y2*scale_y],
                color="black", linewidth=1, linestyle="--")

# ------------------------------
# Clock text
# ------------------------------
clock_text = ax.text(0.02,0.95,"", transform=ax.transAxes, fontsize=12,
                     verticalalignment='top',
                     bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))

# ------------------------------
# Axes limits and labels
# ------------------------------
ax.set_xlim(0, display_rows)
ax.set_ylim(0, display_cols)
ax.set_title("Top-down Game View")
ax.set_xlabel("X")
ax.set_ylabel("Y")

max_steps = max(len(path) for path in tank_paths.values())

# ------------------------------
# Update function
# ------------------------------
def update_frame(frame):
    for tank_id, path in tank_paths.items():
        current_step = min(frame, len(path))
        if current_step > 0:
            coords = np.array(path[:current_step], dtype=np.float32)
            coords[:,0] *= scale_x
            coords[:,1] *= scale_y

            # Update LineCollection
            if current_step > 1:
                segments = [coords[i:i+2] for i in range(len(coords)-1)]
                tank_lines[tank_id].set_segments(segments)
            
            # Update dot
            tank_dots[tank_id].set_data([coords[-1,0]], [coords[-1,1]])

    clock_text.set_text(f"Time step: {frame}")
    canvas.draw_idle()

# ------------------------------
# Slider
# ------------------------------
def on_slider_change(val):
    update_frame(int(float(val)))

slider = tk.Scale(root, from_=0, to=max_steps, orient=tk.HORIZONTAL,
                  length=600, label="Time step", command=on_slider_change)
slider.pack(side=tk.BOTTOM)

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

# ------------------------------
# Start Tkinter mainloop
# ------------------------------
root.mainloop()