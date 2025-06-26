import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap

fighters = {
    "F-5": {
        "gun": "20 mm M39",
        "nation": "USA",
        "in_service": 1963,
        "max_turn_rate": 18,  # deg/s sustained approx
        "max_speed": 1500,    # km/h approx max speed
        "stall_speed": 160,   # km/h approx stall speed
        "acceleration": 50,   # km/h per second approx
        "max_climb_rate": 50  # m/s approx climb rate
    },
    "F-16": {
        "gun": "20 mm M61",
        "nation": "USA",
        "in_service": 1978,
        "max_turn_rate": 20,
        "max_speed": 2100,
        "stall_speed": 200,
        "acceleration": 70,
        "max_climb_rate": 70
    },
}

class DogfightSimulator:
    def __init__(self, ac1_name, ac2_name):
        self.ac1_name = ac1_name
        self.ac2_name = ac2_name
        
        self.ac1_data = fighters[ac1_name]
        self.ac2_data = fighters[ac2_name]
        
        # 3D position: x, y, z (meters)
        self.ac1_pos = np.array([0.0, 0.0, 5000.0])  # start at 5000m altitude
        self.ac2_pos = np.array([2000.0, 0.0, 4500.0])
        
        self.ac1_heading = 0.0
        self.ac2_heading = 180.0
        
        self.ac1_speed = self.ac1_data["stall_speed"] + 100
        self.ac2_speed = self.ac2_data["stall_speed"] + 100
        
        self.ac1_target_speed = self.ac1_speed
        self.ac2_target_speed = self.ac2_speed
        
        self.ac1_max_turn_rate = self.ac1_data["max_turn_rate"]
        self.ac2_max_turn_rate = self.ac2_data["max_turn_rate"]
        
        self.ac1_max_speed = self.ac1_data["max_speed"]
        self.ac2_max_speed = self.ac2_data["max_speed"]
        
        self.ac1_acceleration = self.ac1_data["acceleration"]
        self.ac2_acceleration = self.ac2_data["acceleration"]
        
        self.ac1_max_climb_rate = self.ac1_data["max_climb_rate"]
        self.ac2_max_climb_rate = self.ac2_data["max_climb_rate"]
        
        # Climb rate (m/s), start neutral
        self.ac1_climb_rate = 0.0
        self.ac2_climb_rate = 0.0
        
        self.dt = 0.05
        
        # Setup figure with 2 subplots: top-down and altitude
        self.fig, (self.ax_xy, self.ax_z) = plt.subplots(2, 1, figsize=(8,10))
        
        # Top-down view setup
        self.ax_xy.set_xlim(-500, 2500)
        self.ax_xy.set_ylim(-1500, 1500)
        self.ax_xy.set_aspect('equal')
        self.ax_xy.set_title("Dogfight Top-Down View")
        
        # Altitude plot setup
        self.ax_z.set_xlim(0, 600)  # 600 frames (approx 30 sec)
        self.ax_z.set_ylim(0, 12000)  # 0-12km altitude
        self.ax_z.set_xlabel("Time (frames)")
        self.ax_z.set_ylabel("Altitude (m)")
        self.ax_z.set_title("Altitude over time")
        
        # Trails for xy position
        self.ac1_trail_x, self.ac1_trail_y = [], []
        self.ac2_trail_x, self.ac2_trail_y = [], []
        self.ac1_trail_plot, = self.ax_xy.plot([], [], 'b-', alpha=0.5)
        self.ac2_trail_plot, = self.ax_xy.plot([], [], 'r-', alpha=0.5)
        
        # Altitude history
        self.ac1_altitude_hist = []
        self.ac2_altitude_hist = []
        self.ac1_alt_plot, = self.ax_z.plot([], [], 'b-', label=self.ac1_name)
        self.ac2_alt_plot, = self.ax_z.plot([], [], 'r-', label=self.ac2_name)
        self.ax_z.legend()
        
        self.ac1_arrow = None
        self.ac2_arrow = None
        
        self.info_text = self.ax_xy.text(0.02, 0.95, "", transform=self.ax_xy.transAxes)
        
        # Color map for altitude marker color (blue low, red high)
        self.cmap = get_cmap("coolwarm")
        self.norm = Normalize(vmin=0, vmax=12000)
        
        self.ani = animation.FuncAnimation(self.fig, self.update_animation, frames=600,
                                           interval=int(self.dt*1000), blit=False, repeat=False)
        
    def update_animation(self, frame):
        # Compute angles to opponent (ignore altitude for heading)
        vec_ac1_to_ac2 = self.ac2_pos[:2] - self.ac1_pos[:2]
        vec_ac2_to_ac1 = self.ac1_pos[:2] - self.ac2_pos[:2]
        
        angle_ac1_to_ac2 = np.degrees(np.arctan2(vec_ac1_to_ac2[1], vec_ac1_to_ac2[0])) % 360
        angle_ac2_to_ac1 = np.degrees(np.arctan2(vec_ac2_to_ac1[1], vec_ac2_to_ac1[0])) % 360
        
        # Smooth heading turns
        self.ac1_heading = self.smooth_turn(self.ac1_heading, angle_ac1_to_ac2, self.ac1_max_turn_rate)
        self.ac2_heading = self.smooth_turn(self.ac2_heading, angle_ac2_to_ac1, self.ac2_max_turn_rate)
        
        # Distance (3D)
        dist = np.linalg.norm(self.ac1_pos - self.ac2_pos)
        
        # Simple logic for climb: if opponent higher, try to climb, else descend
        alt_diff = self.ac2_pos[2] - self.ac1_pos[2]
        self.ac1_climb_rate = np.clip(alt_diff * 0.1, -self.ac1_max_climb_rate, self.ac1_max_climb_rate)
        
        alt_diff2 = self.ac1_pos[2] - self.ac2_pos[2]
        self.ac2_climb_rate = np.clip(alt_diff2 * 0.1, -self.ac2_max_climb_rate, self.ac2_max_climb_rate)
        
        # Speed control (similar to before)
        if dist > 1500:
            self.ac1_target_speed = self.ac1_max_speed * 0.95
            self.ac2_target_speed = self.ac2_max_speed * 0.95
        elif dist > 500:
            self.ac1_target_speed = (self.ac1_max_speed + self.ac1_speed)/2 * 0.8
            self.ac2_target_speed = (self.ac2_max_speed + self.ac2_speed)/2 * 0.8
        else:
            self.ac1_target_speed = self.ac1_data["stall_speed"] + 200
            self.ac2_target_speed = self.ac2_data["stall_speed"] + 200
        
        self.ac1_speed = self.adjust_speed(self.ac1_speed, self.ac1_target_speed, self.ac1_acceleration)
        self.ac2_speed = self.adjust_speed(self.ac2_speed, self.ac2_target_speed, self.ac2_acceleration)
        
        # Update positions (x, y)
        self.ac1_pos[:2] += self.move_forward(self.ac1_heading, self.ac1_speed)
        self.ac2_pos[:2] += self.move_forward(self.ac2_heading, self.ac2_speed)
        
        # Update altitudes (z)
        self.ac1_pos[2] += self.ac1_climb_rate * self.dt
        self.ac2_pos[2] += self.ac2_climb_rate * self.dt
        
        # Clamp altitude between 0 and 12,000 m
        self.ac1_pos[2] = np.clip(self.ac1_pos[2], 0, 12000)
        self.ac2_pos[2] = np.clip(self.ac2_pos[2], 0, 12000)
        
        # Update trails for XY
        self.ac1_trail_x.append(self.ac1_pos[0])
        self.ac1_trail_y.append(self.ac1_pos[1])
        self.ac2_trail_x.append(self.ac2_pos[0])
        self.ac2_trail_y.append(self.ac2_pos[1])
        
        max_trail_len = 100
        self.ac1_trail_x = self.ac1_trail_x[-max_trail_len:]
        self.ac1_trail_y = self.ac1_trail_y[-max_trail_len:]
        self.ac2_trail_x = self.ac2_trail_x[-max_trail_len:]
        self.ac2_trail_y = self.ac2_trail_y[-max_trail_len:]
        
        # Update altitude history
        self.ac1_altitude_hist.append(self.ac1_pos[2])
        self.ac2_altitude_hist.append(self.ac2_pos[2])
        self.ac1_altitude_hist = self.ac1_altitude_hist[-600:]
        self.ac2_altitude_hist = self.ac2_altitude_hist[-600:]
        
        # Clear previous arrows
        if self.ac1_arrow:
            self.ac1_arrow.remove()
        if self.ac2_arrow:
            self.ac2_arrow.remove()
        
        # Color by altitude
        c1 = self.cmap(self.norm(self.ac1_pos[2]))
        c2 = self.cmap(self.norm(self.ac2_pos[2]))
        
        # Draw aircraft arrows, color-coded by altitude
        self.ac1_arrow = self.ax_xy.arrow(self.ac1_pos[0], self.ac1_pos[1], 
                                     50 * np.cos(np.radians(self.ac1_heading)), 
                                     50 * np.sin(np.radians(self.ac1_heading)), 
                                     head_width=60, head_length=60, fc=c1, ec=c1)
        self.ac2_arrow = self.ax_xy.arrow(self.ac2_pos[0], self.ac2_pos[1], 
                                     50 * np.cos(np.radians(self.ac2_heading)), 
                                     50 * np.sin(np.radians(self.ac2_heading)), 
                                     head_width=60, head_length=60, fc=c2, ec=c2)
        
        # Update trails plots
        self.ac1_trail_plot.set_data(self.ac1_trail_x, self.ac1_trail_y)
        self.ac2_trail_plot.set_data(self.ac2_trail_x, self.ac2_trail_y)
        
        # Update altitude plots
        frames = np.arange(len(self.ac1_altitude_hist))
        self.ac1_alt_plot.set_data(frames, self.ac1_altitude_hist)
        self.ac2_alt_plot.set_data(frames, self.ac2_altitude_hist)
        
       # Update info text
        info = (
            f"Frame: {frame}\n"
            f"{self.ac1_name} Pos: ({self.ac1_pos[0]:.0f}, {self.ac1_pos[1]:.0f}, {self.ac1_pos[2]:.0f} m)  "
            f"Heading: {self.ac1_heading:.1f}°  Speed: {self.ac1_speed:.0f} km/h\n"
            f"{self.ac2_name} Pos: ({self.ac2_pos[0]:.0f}, {self.ac2_pos[1]:.0f}, {self.ac2_pos[2]:.0f} m)  "
            f"Heading: {self.ac2_heading:.1f}°  Speed: {self.ac2_speed:.0f} km/h\n"
            f"Distance: {dist:.0f} m"
        )
        self.info_text.set_text(info)

        # Stop animation if fighters get too close
        if dist < 100:
            self.info_text.set_text(info + "\n>>> Close range merge engagement <<<")
            self.ani.event_source.stop()

        return (self.ac1_arrow, self.ac2_arrow, self.ac1_trail_plot, 
                self.ac2_trail_plot, self.ac1_alt_plot, self.ac2_alt_plot, self.info_text)

    def smooth_turn(self, current, target, max_turn_rate):
        diff = (target - current + 360) % 360
        if diff > 180:
            diff -= 360
        max_turn = max_turn_rate * self.dt
        if abs(diff) < max_turn:
            return target
        return (current + np.sign(diff) * max_turn) % 360

    def adjust_speed(self, current_speed, target_speed, acceleration):
        max_change = acceleration * self.dt
        diff = target_speed - current_speed
        if abs(diff) < max_change:
            return target_speed
        return current_speed + np.sign(diff) * max_change

    def move_forward(self, heading_deg, speed_kmh):
        rad = np.radians(heading_deg)
        speed_m_s = speed_kmh * 1000 / 3600
        dx = speed_m_s * self.dt * np.cos(rad)
        dy = speed_m_s * self.dt * np.sin(rad)
        return np.array([dx, dy])

def main():
    print("Available fighters:")
    for k in fighters.keys():
        print(f" - {k}")
    try:
        ac1 = input("Enter first fighter model name: ").strip()
        ac2 = input("Enter second fighter model name: ").strip()
        if ac1 not in fighters or ac2 not in fighters:
            print("Invalid selection. Using defaults F-5 vs F-16.")
            ac1, ac2 = "F-5", "F-16"
    except Exception:
        print("Input unavailable. Using defaults F-5 vs F-16.")
        ac1, ac2 = "F-5", "F-16"

    print(f"Initializing simulation: {ac1} vs {ac2}")
    sim = DogfightSimulator(ac1, ac2)
    plt.show()

if __name__ == "__main__":
    main()