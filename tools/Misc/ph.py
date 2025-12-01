import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import re
import os
import tkinter as tk
from tkinter import ttk
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
max_i += 1
max_j += 1

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
# Load optional shots
# ------------------------------
shots = []
if os.path.exists(shot_file):
    with open(shot_file,"r") as f:
        raw = f.read()
    shot_pattern = r"\|(\d+),(\d+),(\d+),(\d+)"
    shots = [tuple(map(int, m)) for m in re.findall(shot_pattern, raw)]

# ------------------------------
# Display parameters
# ------------------------------
screen_rows, screen_cols = 400, 400
rows_factor = max(1, max_i // screen_rows)
cols_factor = max(1, max_j // screen_cols)
display_rows = (max_i + rows_factor - 1)//rows_factor
display_cols = (max_j + cols_factor - 1)//cols_factor
scale_x = display_rows / max_i
scale_y = display_cols / max_j

# ------------------------------
# Fast fill zeros for display
# ------------------------------
def fill_display(sparse_dict, shape, factor_rows, factor_cols):
    display = np.zeros(shape, dtype=np.float32)
    for i, row in sparse_dict.items():
        di = i // factor_rows
        if di >= shape[0]: continue
        for j, h in row.items():
            dj = j // factor_cols
            if dj >= shape[1]: continue
            display[di, dj] = h
    # propagate last known value
    for i in range(shape[0]):
        last = 1e-6
        for j in range(shape[1]):
            if display[i,j]==0:
                display[i,j]=last
            else:
                last = display[i,j]
    for j in range(shape[1]):
        last = 1e-6
        for i in range(shape[0]):
            if display[i,j]==0:
                display[i,j]=last
            else:
                last = display[i,j]
    return np.maximum(display,1e-6)

display_terrain = fill_display(terrain_sparse, (display_rows, display_cols), rows_factor, cols_factor)

# ------------------------------
# Tkinter main window
# ------------------------------
root = tk.Tk()
root.title("Game Visualization")

fig, ax = plt.subplots(figsize=(6,6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

im = ax.imshow(display_terrain.T, origin='lower', cmap='terrain',
               interpolation='nearest',
               norm=LogNorm(vmin=np.min(display_terrain), vmax=np.max(display_terrain)))
plt.colorbar(im, ax=ax, label="Height (log scale)")

colors = ['red','blue','yellow','cyan','magenta','orange','green','purple']
tank_lines = {}
tank_dots = {}
for idx, tank_id in enumerate(sorted(tank_paths.keys())):
    line, = ax.plot([],[], color=colors[idx%len(colors)], label=f"Tank {tank_id}", linewidth=2)
    dot, = ax.plot([],[], 'o', color=colors[idx%len(colors)], markersize=6)
    tank_lines[tank_id] = line
    tank_dots[tank_id] = dot

clock_text = ax.text(0.02,0.95,"", transform=ax.transAxes, fontsize=12,
                     verticalalignment='top',
                     bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))

# Shots
permanent_shots = True
shot_markers = []
if permanent_shots:
    for (x1,y1,x2,y2) in shots:
        line, = ax.plot([x1*scale_x, x2*scale_x],[y1*scale_y, y2*scale_y],
                        color="black", linewidth=1, linestyle="--")
        shot_markers.append(line)

ax.set_xlim(0, display_rows)
ax.set_ylim(0, display_cols)
ax.set_title("Top-down game view")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.legend()

max_steps = max(len(path) for path in tank_paths.values())
trail_length = 20

# ------------------------------
# Update function
# ------------------------------
def update_frame(frame):
    for tank_id, path in tank_paths.items():
        current_step = min(frame, len(path))
        if current_step>0:
            coords = np.array(path[:current_step], dtype=np.float32)
            coords[:,0] *= scale_x
            coords[:,1] *= scale_y
            tank_lines[tank_id].set_data(coords[:,0], coords[:,1])
            start_idx = max(0, current_step-trail_length)
            tail_coords = np.array(path[start_idx:current_step], dtype=np.float32)
            tail_coords[:,0] *= scale_x
            tail_coords[:,1] *= scale_y
            if len(tail_coords)>0:
                tank_dots[tank_id].set_data([tail_coords[-1,0]], [tail_coords[-1,1]])
    clock_text.set_text(f"Time step: {frame}")
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
# Automatic playback (optional)
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
# Start Tkinter loop
# ------------------------------
root.mainloop()