import numpy as np

# -----------------------------
# Physical constants
# -----------------------------
k_B = 1.380649e-23      # J/K
T = 300                 # Kelvin (room temp)
ln2 = np.log(2)

# Landauer limit per bit
E_landauer = k_B * T * ln2

# -----------------------------
# System parameters
# -----------------------------

# Bit operations
bits = 20_000_000       # 20 million operations

# RF link parameters (toy model)
distance = 0.01         # 1 cm
attenuation_db_per_cm = 2.0   # very lossy plastic-like medium
tx_power = 1e-3         # 1 mW reader transmit power

# Convert dB loss to linear
attenuation_db = attenuation_db_per_cm * distance * 100  # cm scaling correction
attenuation_linear = 10 ** (-attenuation_db / 10)

# Receiver efficiency
rectifier_efficiency = 0.3

# Thermal model
mass = 1e-6             # 1 mg fob
specific_heat = 900     # J/kgK for plastic-ish mix
thermal_capacity = mass * specific_heat

thermal_conductance = 1e-3  # W/K (weak coupling to environment)

# simulation time
dt = 1e-6
steps = 200000

# -----------------------------
# Initial conditions
# -----------------------------
T_env = 300
T_obj = 300

energy_accumulated = 0

# -----------------------------
# Derived energies
# -----------------------------

# Landauer energy for full computation
E_landauer_total = bits * E_landauer

# RF received power
P_received = tx_power * attenuation_linear * rectifier_efficiency

# -----------------------------
# Time evolution
# -----------------------------
temps = []
time = []

for i in range(steps):

    t = i * dt

    # RF energy deposited this step
    E_in = P_received * dt

    # split into:
    # - useful "computation energy floor"
    # - heat
    useful = min(E_in, E_landauer_total / steps)
    heat = E_in - useful

    # accumulate heat
    energy_accumulated += heat

    # thermal dynamics
    dT = (heat / thermal_capacity) - (T_obj - T_env) * (thermal_conductance / thermal_capacity) * dt
    T_obj += dT

    temps.append(T_obj)
    time.append(t)

# -----------------------------
# Results
# -----------------------------
print("Landauer energy total (J):", E_landauer_total)
print("Received RF power (W):", P_received)
print("Final temperature (K):", T_obj)
print("Max temperature (K):", max(temps))