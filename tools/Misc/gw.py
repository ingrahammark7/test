import os
os.environ["KIVY_GL_BACKEND"] = "sdl2"

import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.clock import Clock

from kivy.graphics import Rectangle, Color
from kivy.graphics.texture import Texture

# ============================================================
# PHYSICS CORE (stable simplified model)
# ============================================================

A = 0.015
C_TH = 900.0
T_MAX = 450.0

def rho(h):
    return 1.225 * np.exp(-h / 8500)

def Q_aero(M, h):
    return 2e-4 * rho(h) * (M * 340.0) ** 3 * A

def Q_elec(P):
    return 50.0 + 0.32 * P

def Q_cool(T):
    return 60.0 * A * (T - 220.0)

# ============================================================
# GPU FIELD (vectorized phase space)
# ============================================================

SIZE = 60
LAYERS = 5

M_vals = np.linspace(0.5, 6.0, SIZE)
P_vals = np.linspace(0, 2000, SIZE)

M_mesh, P_mesh = np.meshgrid(M_vals, P_vals, indexing="ij")

def build_layer(h):
    Qin = Q_aero(M_mesh, h) + Q_elec(P_mesh)
    return (Qin < 2e6).astype(np.uint8)

def build_stack(base_h):
    return [build_layer(base_h + i * 1500) for i in range(LAYERS)]

# ============================================================
# 3D PROJECTION (fake orbit camera)
# ============================================================

def project(x, y, z, angle, cx, cy):
    ca = np.cos(angle)
    sa = np.sin(angle)

    xr = x * ca - z * sa
    zr = x * sa + z * ca + 5.0

    scale = 220 / (zr + 1.0)

    return int(cx + xr * scale), int(cy + y * scale)

# ============================================================
# APP
# ============================================================

class GPUPhaseSpaceApp(App):

    def build(self):

        # ---------------- STATE ----------------
        self.T = 300.0
        self.base_h = 5000
        self.angle = 0.0

        # ---------------- UI ROOT ----------------
        root = BoxLayout(orientation="vertical")

        # SAFE LABELS (NO KIVY PROPERTY COLLISIONS)
        self.ui_title = Label(text="GPU Phase-Space Engine (3D Orbit)")
        self.ui_mach = Label(text="Mach: 2.0")
        self.ui_power = Label(text="Power: 500")
        self.ui_alt = Label(text="Altitude: 5000")
        self.ui_temp = Label(text="Temp: 300 K")
        self.ui_status = Label(text="STABLE")

        # SLIDERS
        self.slider_mach = Slider(min=0.5, max=6.0, value=2.0)
        self.slider_power = Slider(min=0, max=2000, value=500)
        self.slider_alt = Slider(min=0, max=12000, value=5000)

        for w in [
            self.ui_title,
            self.ui_mach,
            self.slider_mach,
            self.ui_power,
            self.slider_power,
            self.ui_alt,
            self.slider_alt,
            self.ui_temp,
            self.ui_status,
        ]:
            root.add_widget(w)

        # ---------------- TEXTURE ----------------
        self.texture = Texture.create(size=(SIZE, SIZE), colorfmt="rgba")
        self.texture.flip_vertical()

        with root.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(texture=self.texture, pos=root.pos, size=root.size)

        root.bind(pos=self._update_rect, size=self._update_rect)

        # ---------------- SIM STATE ----------------
        self.stack = build_stack(self.base_h)

        self.cloud_near = np.random.rand(200, 2) * SIZE
        self.cloud_far = np.random.rand(120, 2) * SIZE

        # ---------------- LOOP ----------------
        Clock.schedule_interval(self.step, 0.05)
        Clock.schedule_interval(self.update_field, 1.2)

        return root

    # ========================================================
    # LABEL UPDATE
    # ========================================================

    def update_labels(self):

        self.ui_mach.text = f"Mach: {self.slider_mach.value:.2f}"
        self.ui_power.text = f"Power: {self.slider_power.value:.0f}"
        self.ui_alt.text = f"Altitude: {self.slider_alt.value:.0f}"
        self.ui_temp.text = f"Temp: {self.T:.1f} K"

    # ========================================================
    # PHYSICS STEP
    # ========================================================

    def step(self, dt):

        M = self.slider_mach.value
        P = self.slider_power.value
        H = self.slider_alt.value

        Qin = Q_aero(M, H) + Q_elec(P)
        Qout = Q_cool(self.T)

        self.T += (Qin - Qout) / C_TH * 0.1

        # orbit motion
        self.angle += 0.03

        # cloud drift (parallax depth effect)
        self.cloud_near[:, 0] += 0.25
        self.cloud_near[:, 1] += 0.18

        self.cloud_far[:, 0] += 0.08
        self.cloud_far[:, 1] += 0.05

        self.cloud_near %= SIZE
        self.cloud_far %= SIZE

        self.render()
        self.update_labels()

        if self.T > T_MAX:
            self.ui_status.text = "UNSTABLE"
        else:
            self.ui_status.text = "STABLE"

    # ========================================================
    # FIELD UPDATE
    # ========================================================

    def update_field(self, dt):
        self.base_h = self.slider_alt.value
        self.stack = build_stack(self.base_h)

    # ========================================================
    # 3D ORBIT RENDER
    # ========================================================

    def render(self):

        data = np.zeros((SIZE, SIZE, 4), dtype=np.uint8)

        cx, cy = SIZE // 2, SIZE // 2

        # terrain layers (depth stack)
        for z, layer in enumerate(self.stack):

            for x in range(SIZE):
                for y in range(SIZE):

                    if layer[x, y]:

                        px, py = project(
                            x - cx,
                            y - cy,
                            z * 1.2,
                            self.angle,
                            cx,
                            cy,
                        )

                        if 0 <= px < SIZE and 0 <= py < SIZE:

                            intensity = int(255 / (1 + z))

                            data[px, py] = [0, intensity, 255 - intensity, 160]

        # cloud overlay (near)
        for x, y in self.cloud_near.astype(int):
            data[x % SIZE, y % SIZE] = [255, 255, 255, 220]

        # cloud overlay (far)
        for x, y in self.cloud_far.astype(int):
            data[x % SIZE, y % SIZE] = [180, 180, 255, 120]

        self.texture.blit_buffer(
            data.ravel(),
            colorfmt="rgba",
            bufferfmt="ubyte",
        )

        self.rect.texture = self.texture

    # ========================================================
    # RESIZE
    # ========================================================

    def _update_rect(self, *args):
        self.rect.pos = self.rect.pos
        self.rect.size = self.rect.size


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    GPUPhaseSpaceApp().run()