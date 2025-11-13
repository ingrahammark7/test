# ================================================
# Ultimate Trig-Free Tracked Vehicle Simulation
# ================================================

import sympy as sp
import csv
import matplotlib.pyplot as plt

class TrackedVehicle:
    def __init__(self, b, x0=0.0, y0=0.0, heading_deg=None, heading_vec=None,
                 series_order=5, symbolic=False, terrain_factor=1.0, bounds=None):
        """
        Initialize tracked vehicle.

        Parameters:
        b : float
            Track width
        x0, y0 : float
            Initial position
        heading_deg : float
            Initial heading in degrees (optional)
        heading_vec : tuple (h_x0, h_y0)
            Initial heading vector (optional, overrides heading_deg)
        series_order : int
            Number of terms in series expansion
        symbolic : bool
            Use symbolic computations (SymPy)
        terrain_factor : float or callable
            Multiplier to scale v_L and v_R for terrain/slip effects
        bounds : tuple ((x_min, x_max), (y_min, y_max))
            Optional collision/boundary limits
        """
        self.b = b
        self.series_order = series_order
        self.symbolic = symbolic
        self.terrain_factor = terrain_factor
        self.bounds = bounds

        # Position
        self.x = sp.Symbol('x0') if symbolic else x0
        self.y = sp.Symbol('y0') if symbolic else y0

        # Initialize heading vector
        if heading_vec is not None:
            self.h_x, self.h_y = heading_vec
        elif heading_deg is not None:
            self.h_x, self.h_y = self.deg_to_frac(heading_deg)
        else:
            self.h_x, self.h_y = (1.0, 0.0)

        # Trajectory storage
        self.trajectory = [(self.x, self.y, self.h_x, self.h_y)]

    # --------------------------------------------
    # Trig-free degree to fractional vector
    # --------------------------------------------
    @staticmethod
    def deg_to_frac(deg):
        """Convert 0-359 degrees to fractional vector (h_x, h_y) trig-free."""
        deg_mod = deg % 360
        # Quadrants simplified for arithmetic only
        if deg_mod == 0:
            return (1.0, 0.0)
        elif deg_mod == 90:
            return (0.0, 1.0)
        elif deg_mod == 180:
            return (-1.0, 0.0)
        elif deg_mod == 270:
            return (0.0, -1.0)
        elif deg_mod < 90:
            return (90 - deg_mod, deg_mod)
        elif deg_mod < 180:
            return (-(deg_mod - 90), 180 - deg_mod)
        elif deg_mod < 270:
            return (-(270 - deg_mod), -(deg_mod - 180))
        else:
            return (deg_mod - 270, -(360 - deg_mod))

    # --------------------------------------------
    # Optional conversion from vector to degrees trig-free
    # --------------------------------------------
    @staticmethod
    def frac_to_deg(h_x, h_y):
        """Approximate heading in degrees from fractional vector trig-free."""
        # Use quadrant mapping for approximate arithmetic degrees
        if h_x == 0:
            if h_y > 0:
                return 90
            else:
                return 270
        elif h_y == 0:
            return 0 if h_x > 0 else 180
        # Linear approximation without atan2
        ratio = abs(h_y / h_x)
        deg = ratio * 45  # rough approximation
        if h_x > 0 and h_y > 0:
            return deg
        elif h_x < 0 and h_y > 0:
            return 180 - deg
        elif h_x < 0 and h_y < 0:
            return 180 + deg
        else:
            return 360 - deg

    # --------------------------------------------
    # Single step update (series expansion, terrain, boundaries)
    # --------------------------------------------
    def step(self, v_L, v_R, dt):
        """Update position and heading for one time step."""
        # Apply terrain factor
        if callable(self.terrain_factor):
            scale = self.terrain_factor(self.x, self.y)
        else:
            scale = self.terrain_factor
        v_L *= scale
        v_R *= scale

        v = (v_L + v_R) / 2
        omega = (v_R - v_L) / self.b

        # Series expansion of heading
        h_x_new, h_y_new = self.h_x, self.h_y
        for n in range(1, self.series_order + 1):
            term = (omega * dt) ** n / sp.factorial(n)
            if n % 4 == 1:
                h_x_new -= self.h_y * term
                h_y_new += self.h_x * term
            elif n % 4 == 2:
                h_x_new -= self.h_x * term
                h_y_new -= self.h_y * term
            elif n % 4 == 3:
                h_x_new += self.h_y * term
                h_y_new -= self.h_x * term
            else:
                h_x_new += self.h_x * term
                h_y_new += self.h_y * term

        # Normalize heading
        norm = sp.sqrt(h_x_new ** 2 + h_y_new ** 2)
        h_x_new /= norm
        h_y_new /= norm

        # Compute displacement
        dx = v * h_x_new * dt
        dy = v * h_y_new * dt
        new_x = self.x + dx
        new_y = self.y + dy

        # Apply boundary check
        if self.bounds is not None:
            (x_min, x_max), (y_min, y_max) = self.bounds
            new_x = max(x_min, min(new_x, x_max))
            new_y = max(y_min, min(new_y, y_max))

        self.x, self.y = new_x, new_y
        self.h_x, self.h_y = h_x_new, h_y_new
        self.trajectory.append((self.x, self.y, self.h_x, self.h_y))

    # --------------------------------------------
    # Simulate multiple steps
    # --------------------------------------------
    def simulate(self, v_L_list, v_R_list, dt, adaptive_dt=False):
        """
        Simulate over multiple steps.

        v_L_list, v_R_list : list of left/right track speeds
        dt : base time step
        adaptive_dt : bool
            Reduce dt if omega*dt > threshold for series accuracy
        """
        for v_L, v_R in zip(v_L_list, v_R_list):
            step_dt = dt
            if adaptive_dt:
                omega = abs((v_R - v_L) / self.b)
                threshold = 0.1  # max allowed omega*dt for series
                if omega * dt > threshold:
                    step_dt = threshold / omega
            self.step(v_L, v_R, step_dt)

    # --------------------------------------------
    # Export trajectory to CSV
    # --------------------------------------------
    def export_csv(self, filename):
        """Export trajectory to CSV file."""
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['x', 'y', 'h_x', 'h_y'])
            for point in self.trajectory:
                writer.writerow([float(p.evalf()) if isinstance(p, sp.Basic) else p for p in point])

    # --------------------------------------------
    # Plot trajectory
    # --------------------------------------------
    def plot(self):
        """Plot x/y trajectory."""
        xs = [float(p[0].evalf()) if isinstance(p[0], sp.Basic) else p[0] for p in self.trajectory]
        ys = [float(p[1].evalf()) if isinstance(p[1], sp.Basic) else p[1] for p in self.trajectory]
        plt.plot(xs, ys, marker='o')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Tracked Vehicle Trajectory')
        plt.axis('equal')
        plt.grid(True)
        plt.show()