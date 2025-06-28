import numpy as np
import time

class CameraFocusManager:
    def __init__(self, ax, aircraft_list, missile_events):
        self.ax = ax
        self.aircraft_list = aircraft_list
        self.missile_events = missile_events
        self.current_focus = None
        self.focus_start_time = time.time()
        self.focus_cooldown = 3.0  # Min seconds before focus can change
        self.next_focus_time = self.focus_start_time + np.random.uniform(3.0, 6.0)

    def update(self, frame):
        now = time.time()

        # If current focus is None or cooldown expired, or focus out of view, select new focus
        if (self.current_focus is None or
            now > self.next_focus_time or
            not self._is_focus_visible()):
            self.select_new_focus()
            self.focus_start_time = now
            self.next_focus_time = now + np.random.uniform(3.0, 6.0)

        self._apply_camera_transform(frame)

    def select_new_focus(self):
        # Pick all alive aircraft and missiles as potential focus points
        candidates = [ac for ac in self.aircraft_list if ac.alive]
        # Add missiles that are alive as well
        for ac in self.aircraft_list:
            candidates.extend([m for m in ac.missiles if m.alive])

        if not candidates:
            self.current_focus = None
            return

        # Pick a random candidate for focus
        self.current_focus = np.random.choice(candidates)

    def _is_focus_visible(self):
        if self.current_focus is None:
            return False
        pos = self.current_focus.position
        # Get current axis limits
        xlim = self.ax.get_xlim3d()
        ylim = self.ax.get_ylim3d()
        zlim = self.ax.get_zlim3d()

        # Add some margin to view box (20% margin)
        margin_x = (xlim[1] - xlim[0]) * 0.2
        margin_y = (ylim[1] - ylim[0]) * 0.2
        margin_z = (zlim[1] - zlim[0]) * 0.2

        in_x = (pos[0] >= xlim[0] + margin_x) and (pos[0] <= xlim[1] - margin_x)
        in_y = (pos[1] >= ylim[0] + margin_y) and (pos[1] <= ylim[1] - margin_y)
        in_z = (pos[2] >= zlim[0] + margin_z) and (pos[2] <= zlim[1] - margin_z)

        return in_x and in_y and in_z

    def _apply_camera_transform(self, frame):
        if self.current_focus is None:
            # Default camera rotation if no focus
            azim = (frame * 0.5) % 360
            elev = 20
            self.ax.view_init(elev=elev, azim=azim)
            return

        pos = self.current_focus.position
        # Simple logic: center the view near the focused object
        # Adjust azimuth and elevation to look roughly at the focused object

        # We keep a fixed elevation and adjust azimuth based on position
        azim = np.degrees(np.arctan2(pos[1], pos[0]))
        elev = 20 + (pos[2] / 5)  # Slight elevation offset by height

        self.ax.view_init(elev=elev, azim=azim)

        # Optionally, adjust axis limits to zoom on current focus
        zoom_range = 30  # Smaller means zoomed in more
        self.ax.set_xlim(pos[0] - zoom_range, pos[0] + zoom_range)
        self.ax.set_ylim(pos[1] - zoom_range, pos[1] + zoom_range)
        self.ax.set_zlim(pos[2] - zoom_range / 2, pos[2] + zoom_range / 2)