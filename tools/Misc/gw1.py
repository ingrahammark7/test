from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color, Rotate
from kivy.clock import Clock
import random
import math

class SpectacleWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cells = []
        self.base_radii = [100, 180, 260, 340, 420]  # multiple concentric rings
        self.colors = [(1,0,0), (0,1,0), (0,0,1), (1,1,0), (1,0,1)]  # RGB + extra colors
        self.max_jitter = 25
        self.max_alpha_change = 0.5
        self.rotations = []
        self.create_cells()
        Clock.schedule_interval(self.update_cells, 1/30.)  # 30 FPS

    def create_cells(self):
        cx, cy = self.center
        for i, r in enumerate(self.base_radii):
            color = Color(*self.colors[i], 0.6)
            ellipse = Ellipse(pos=(cx - r, cy - r), size=(2*r, 2*r))
            rotation = Rotate(origin=(cx, cy), angle=random.uniform(0,360))
            self.canvas.add(rotation)
            self.canvas.add(color)
            self.canvas.add(ellipse)
            self.cells.append({'ellipse': ellipse, 'color': color, 'base_r': r})
            self.rotations.append(rotation)

    def update_cells(self, dt):
        cx, cy = self.center
        for i, cell in enumerate(self.cells):
            # radius jitter for chaotic effect
            jitter = random.uniform(-self.max_jitter, self.max_jitter)
            r = cell['base_r'] + jitter
            cell['ellipse'].pos = (cx - r, cy - r)
            cell['ellipse'].size = (2*r, 2*r)
            # pulsing opacity
            alpha_jitter = random.uniform(-self.max_alpha_change, self.max_alpha_change)
            cell['color'].a = max(0.2, min(1.0, 0.6 + alpha_jitter))
            # rotate slowly
            self.rotations[i].angle += (i+1) * 0.3  # different speed per layer

        # simulate random VEI-style eruption flashes
        if random.random() < 0.02:
            flash_layer = random.choice(self.cells)
            flash_layer['color'].a = 1.0  # sudden bright spike

class SpectacleApp(App):
    def build(self):
        return SpectacleWidget()

if __name__ == '__main__':
    SpectacleApp().run()