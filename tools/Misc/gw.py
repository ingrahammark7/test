import math

# Door parameters
m = 120.0         # kg, mass of sliding door
d = 2.0           # meters, distance door slides to fully open

# Motor / EM parameters
F_emag = 400.0    # N, electromagnetic force provided by motor
a_max = F_emag / m  # m/s², acceleration

# Assuming constant acceleration until halfway, then deceleration
d_half = d / 2

# Time to reach half distance using s = 0.5 * a * t^2
t_half = math.sqrt(2 * d_half / a_max)

# Total time to open (accelerate + decelerate)
t_total = 2 * t_half

# Velocity at midpoint
v_max = a_max * t_half

# Power required at midpoint (P = F * v)
P_max = F_emag * v_max  # Watts

print(f"Door mass: {m} kg")
print(f"Slide distance: {d} m")
print(f"Electromagnetic force: {F_emag} N")
print(f"Max acceleration: {a_max:.2f} m/s²")
print(f"Time to fully open: {t_total:.2f} s")
print(f"Max velocity: {v_max:.2f} m/s")
print(f"Max power required: {P_max:.2f} W")