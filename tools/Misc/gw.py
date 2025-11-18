import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
import numpy as np
import json

# Load reshaped terrain
with open("f.json", "r") as f:
    terrain_dict = json.load(f)

x_keys = sorted(int(k) for k in terrain_dict.keys())
y_keys = sorted({int(j) for xs in terrain_dict.values() for j in xs.keys()})

nx = len(x_keys)
ny = len(y_keys)
terrain_grid = np.zeros((ny, nx), dtype=float)

for ix, x in enumerate(x_keys):
    row = terrain_dict[str(x)]
    for iy, y in enumerate(y_keys):
        if str(y) in row:
            terrain_grid[iy, ix] = float(row[str(y)])
        else:
            terrain_grid[iy, ix] = 0.0

# Normalize heights for coloring
min_h, max_h = terrain_grid.min(), terrain_grid.max()
norm_grid = (terrain_grid - min_h) / (max_h - min_h + 1e-6)

class TerrainWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.draw_terrain()

    def draw_terrain(self):
        self.canvas.clear()
        with self.canvas:
            rect_size = 5  # size of each "pixel" rectangle
            for iy in range(0, ny):
                for ix in range(0, nx):
                    h = norm_grid[iy, ix]
                    # Color from green (low) to brown (high)
                    Color(0.2 + 0.6*h, 0.4 - 0.2*h, 0.2, 1)
                    Rectangle(pos=(ix*rect_size, iy*rect_size),
                              size=(rect_size, rect_size))

class TerrainApp(App):
    def build(self):
        root = ScrollView(size_hint=(1, 1),
                          do_scroll_x=True,
                          do_scroll_y=True)
        terrain_widget = TerrainWidget(size=(nx*5, ny*5))
        root.add_widget(terrain_widget)
        return root

if __name__ == "__main__":
    TerrainApp().run()