import os
os.environ["KIVY_GL_BACKEND"] = "sdl2"

import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.graphics.texture import Texture

# ============================================================
# FULLSCREEN
# ============================================================

Window.fullscreen = "auto"

# ============================================================
# CONFIG
# ============================================================

LAYERS = 6
FOG_COLOR = np.array([120, 140, 170], dtype=np.float32)
FOG_DENSITY = 0.12
DEPTH_ATT = 0.25
MOTION_DECAY = 0.86

def get_size():
    w, h = Window.size
    return max(60, min(120, int(min(w, h) / 10)))

SIZE = get_size()

# ============================================================
# FIELD
# ============================================================

def build_layer(h):
    x = np.linspace(0, 6, SIZE)
    y = np.linspace(0, 6, SIZE)
    X, Y = np.meshgrid(x, y)

    field = np.sin(X + h * 0.0003) + np.cos(Y - h * 0.0002)
    return (field > 0.35).astype(np.uint8)

def build_stack(h):
    return [build_layer(h + i * 1200) for i in range(LAYERS)]

# ============================================================
# CAMERA
# ============================================================

class Camera:
    def __init__(self):
        self.z = 0.0

# ============================================================
# APP
# ============================================================

class CinematicApp(App):

    def build(self):

        self.title = "Cinematic Fly-Through Engine"

        self.cam = Camera()

        self.h = 5000
        self.stack = build_stack(self.h)

        self.prev_frame = np.zeros((SIZE, SIZE, 3), dtype=np.float32)

        # ---------------- TOUCH STATE ----------------

        self.cam_yaw = 0.0
        self.cam_pitch = 0.0
        self.cam_speed = 2.0
        self._last_touch = None

        # ---------------- UI ----------------

        root = BoxLayout(orientation="vertical")

        self.ui_title = Label(text="Cinematic Fly-Through Engine")
        self.ui_status = Label(text="STABLE")

        root.add_widget(self.ui_title)
        root.add_widget(self.ui_status)

        # ---------------- TEXTURE ----------------

        self.texture = Texture.create(size=(SIZE, SIZE), colorfmt="rgb")
        self.texture.flip_vertical()

        with root.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(texture=self.texture, pos=(0, 0), size=Window.size)

        Window.bind(size=self._resize)

        # ---------------- LOOP ----------------

        Clock.schedule_interval(self.update, 0.05)
        Clock.schedule_interval(self.rebuild, 1.2)

        return root

    # ========================================================
    # RESIZE FIX
    # ========================================================

    def _resize(self, *args):

        global SIZE
        SIZE = get_size()

        self.rect.pos = (0, 0)
        self.rect.size = Window.size

        self.texture = Texture.create(size=(SIZE, SIZE), colorfmt="rgb")
        self.texture.flip_vertical()

        self.stack = build_stack(self.h)
        self.prev_frame = np.zeros((SIZE, SIZE, 3), dtype=np.float32)

    # ========================================================
    # TOUCH CONTROL
    # ========================================================

    def on_touch_down(self, touch):
        self._last_touch = (touch.x, touch.y)
        return True

    def on_touch_move(self, touch):

        if self._last_touch is None:
            return True

        dx = touch.x - self._last_touch[0]
        dy = touch.y - self._last_touch[1]

        self.cam_yaw += dx * 0.003
        self.cam_pitch += dy * 0.002

        self.cam_pitch = max(-1.2, min(1.2, self.cam_pitch))

        self.cam_speed = 2.0 + (-dy * 0.01)

        self._last_touch = (touch.x, touch.y)
        return True

    def on_touch_up(self, touch):
        self._last_touch = None
        return True

    # ========================================================
    # REBUILD FIELD
    # ========================================================

    def rebuild(self, dt):
        self.stack = build_stack(self.h)

    # ========================================================
    # MAIN LOOP
    # ========================================================

    def update(self, dt):

        self.cam.z += self.cam_speed

        frame = np.zeros((SIZE, SIZE, 3), dtype=np.float32)

        cx, cy = SIZE // 2, SIZE // 2

        cos_a = np.cos(self.cam_yaw)
        sin_a = np.sin(self.cam_yaw)

        # ====================================================
        # VOLUMETRIC RENDER
        # ====================================================

        for z, layer in enumerate(self.stack):

            depth = z * 1.4 - self.cam.z * 0.01
            depth_factor = np.exp(-DEPTH_ATT * abs(depth))

            for x in range(SIZE):
                for y in range(SIZE):

                    if layer[x, y]:

                        dx = x - cx
                        dy = y - cy

                        rx = dx * cos_a - dy * sin_a
                        ry = dx * sin_a + dy * cos_a

                        ry *= (1.0 + self.cam_pitch)

                        px = int(cx + rx * (200 / (abs(depth) + 3)))
                        py = int(cy + ry * (200 / (abs(depth) + 3)))

                        if 0 <= px < SIZE and 0 <= py < SIZE:

                            intensity = 220 * depth_factor

                            frame[px, py] = [
                                0,
                                intensity,
                                255 * depth_factor
                            ]

        # ====================================================
        # MOTION BLUR
        # ====================================================

        frame = frame * (1 - MOTION_DECAY) + self.prev_frame * MOTION_DECAY
        self.prev_frame = frame.copy()

        # ====================================================
        # FOG (CINEMATIC ATMOSPHERE)
        # ====================================================

        cx, cy = SIZE // 2, SIZE // 2

        for i in range(SIZE):
            for j in range(SIZE):

                p = frame[i, j]

                dist = np.sqrt((i - cx)**2 + (j - cy)**2) / SIZE
                fog = 1 - np.exp(-FOG_DENSITY * dist)

                frame[i, j] = p * (1 - fog) + FOG_COLOR * fog

        # ====================================================
        # OUTPUT
        # ====================================================

        frame = np.clip(frame, 0, 255).astype(np.uint8)

        self.texture.blit_buffer(
            frame.ravel(),
            colorfmt="rgb",
            bufferfmt="ubyte"
        )

        self.rect.texture = self.texture

        # status
        self.ui_status.text = f"speed={self.cam_speed:.2f} yaw={self.cam_yaw:.2f}"


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    CinematicApp().run()