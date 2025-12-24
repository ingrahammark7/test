# Copper wire power limit calculation

# Constants
rho = 1.68e-8  # Copper resistivity in ohm-meter
length = 100    # Wire length in meters
width = 1e-3    # Wire width in meters (1 mm)
thickness = width # Wire thickness in meters (1 mm)
cross_section = width * thickness  # m^2

# Wire resistance
resistance = rho * length / cross_section
print(f"Wire resistance (ohms): {resistance:.6f} Ω")

# Allowable current (approximate for 1 mm^2 copper in air)
I_max = 10  # Amps, continuous safe current

# Maximum power dissipation in wire
P_max = I_max**2 * resistance
print(f"Max power dissipated in wire (watts): {P_max:.2f} W")

# For a DC circuit, power delivered to load = I_max * V
# Optional: calculate voltage drop over wire
V_drop = I_max * resistance
print(f"Voltage drop over wire at {I_max} A: {V_drop:.2f} V")