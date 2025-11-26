# Constants
T_air = 288           # Ambient air temperature in K (~15°C)
gamma = 1.4           # Air specific heat ratio
v = 200               # Speed in m/s
a = 343               # Speed of sound in air in m/s

# Mach number
M = v / a

# Stagnation temperature formula
T_stag = T_air * (1 + (gamma - 1)/2 * M**2)

# Convert to Celsius
T_stag_C = T_stag - 273.15

print(f"Stagnation temperature of steel: {T_stag:.2f} K ({T_stag_C:.2f} °C)")