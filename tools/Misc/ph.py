#!/usr/bin/env python3
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
import re
import os
import tkinter as tk
from tkinter import ttk
import time

# ------------------------------
# Files
# ------------------------------
terrain_file = "f.json"
movement_file = "f2.json"
shot_file = "f3.json"  # optional

# ------------------------------
# Loading screen
# ------------------------------
class LoadingScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Loading...")
        self.root.geometry("400x120")
        self.label = tk.Label(self.root, text="Initializing...", font=("Arial", 12))
        self.label.pack(pady=10)
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=350, mode="determinate")
        self.progress.pack(pady=10)
        self.root.update()

    def set_text(self, text):
        self.label.config(text=text)
        self.root.update()

    def set_progress(self, value):
        self.progress['value'] = value
        self.root.update()

    def close(self):
        self.root.destroy()

loading_screen = LoadingScreen()
loading_screen.set_text("Loading terrain...")
loading_screen.set_progress(10)
time.sleep(0.05)

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

loading_screen.set_progress(40)
loading_screen.set_text("Terrain loaded...")
time.sleep(0.05)

# ------------------------------
# Load tank movements
# ------------------------------
loading_screen.set_text("Loading tank movements...")
loading_screen.set_progress(50)
time.sleep(0.05)

with open(movement_file, "r") as f:
    movements_raw = f.read()

pattern = r"\|(\d+)\s+tank\s+moved\s+to\s+(\d+),(\d+)"
matches = re.findall(pattern, movements_raw)

tank_paths = {}
for idx, (tank_id, x_str, y_str) in enumerate(matches):
    tank_id = int(tank_id)
    x, y = int(x_str), int(y_str)
    tank_paths.setdefault(tank_id, []).append((x, y))
    loading_screen.set_progress(50 + int(40*(idx+1)/len(matches)))
    loading_screen.root.update()

# ------------------------------
# Load optional shots
# ------------------------------
shots = []
if os.path.exists(shot_file):
    loading_screen.set_text("Loading shots...")
    with open(shot_file,"r") as f:
        raw = f.read()
    shot_pattern = r"\|(\d+),(\d+),(\d+),(\d+)"
    shots = [tuple(map(int, m)) for m in re.findall(shot_pattern, raw)]

loading_screen.set_progress(100)
loading_screen.set_text("Done!")
loading_screen.root.update()
time.sleep(0.2)
loading_screen.close()

# ------------------------------
# Determine display shape
# ------------------------------
screen_rows, screen_cols = 400, 400  # approximate
rows_factor = max(1, max_i // screen_rows)
cols_factor = max(1, max_j // screen_cols)
display_rows = (max_i + rows_factor - 1)//rows_factor
display_cols = (max_j + cols_factor - 1)//cols_factor

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
    # Fill zeros quickly: propagate last known row/col
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
    return np.maximum(display, 1e-6)

display_terrain = fill_display(terrain_sparse, (display_rows, display_cols), rows_factor, cols_factor)

# ------------------------------
# Setup plot
# ------------------------------
fig, ax = plt.subplots(figsize=(8,8))
im = ax.imshow(display_terrain.T, origin='lower', cmap='terrain',
               interpolation='nearest',
               norm=LogNorm(vmin=np.min(display_terrain), vmax=np.max(display_terrain)))
plt.colorbar(im, label="Height (log scale)")

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
permanent_shots = True  # set False for conditional display
proximity_radius = 5    # conditional shots radius
shot_markers = []

if permanent_shots:
    for (x1,y1,x2,y2) in shots:
        line, = ax.plot([x1,x2],[y1,y2], color="black", linewidth=1, linestyle="--")
        shot_markers.append(line)

ax.set_xlim(0, display_rows)
ax.set_ylim(0, display_cols)
ax.set_title("Top-down game view (approximate display)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.legend()

max_steps = max(len(path) for path in tank_paths.values())
trail_length = 20

# ------------------------------
# Animation
# ------------------------------
def animate(frame):
    # Tanks
    for tank_id, path in tank_paths.items():
        current_step = min(frame, len(path))
        if current_step>0:
            coords = np.array(path[:current_step])
            tank_lines[tank_id].set_data(coords[:,0], coords[:,1])
            start_idx = max(0, current_step-trail_length)
            tail_coords = np.array(path[start_idx:current_step])
            if len(tail_coords)>0:
                tank_dots[tank_id].set_data([tail_coords[-1,0]], [tail_coords[-1,1]])
    # Shots (conditional)
    if not permanent_shots:
        for idx, (x1,y1,x2,y2) in enumerate(shots):
            active = False
            for path in tank_paths.values():
                if len(path)==0:
                    continue
                tank_pos = path[min(frame,len(path)-1)]
                if np.hypot(tank_pos[0]-x2, tank_pos[1]-y2)<=proximity_radius:
                    active = True
                    break
            if active:
                if idx>=len(shot_markers):
                    line, = ax.plot([x1,x2],[y1,y2], color="black", linewidth=1, linestyle="--")
                    shot_markers.append(line)
                else:
                    shot_markers[idx].set_data([x1,x2],[y1,y2])
            else:
                if idx<len(shot_markers):
                    shot_markers[idx].set_data([],[])
    # Clock
    clock_text.set_text(f"Time step: {frame}")
    return list(tank_lines.values()) + list(tank_dots.values()) + shot_markers + [clock_text]

ani = FuncAnimation(fig, animate, frames=max_steps+5, interval=200, blit=False)
plt.show()