import numpy as np
import matplotlib.pyplot as plt

# === Constants ===
g = 9.81  # m/s^2

# === Inputs (user-provided) ===
m_missile = 500       # kg
fuel_energy = 10e9    # J total fuel energy
max_heat_flux = 300e6 # W/m^2, melting/structural limit

m_fighter = 20000     # kg
v_fighter = 340       # m/s, Mach 1

missile_area = 1.0    # m^2, effective air volume displaced for heating/drag

dt = 0.01  # s time step
max_time = 30  # seconds simulation

# === Initial conditions ===
v_missile = 0.0
range_to_target = 2000  # m
fuel_remaining = fuel_energy

# Lists for plotting
v_list = []
range_list = []
fuel_list = []
turn_rate_list = []
time_list = []

for t in np.arange(0, max_time, dt):
    # --- Aerodynamic heating ---
    heat_flux = 0.5 * v_missile**3 * missile_area  # W, proportional to volume of air moved
    if heat_flux > max_heat_flux:
        acc_max = 0.0
    else:
        acc_max = fuel_remaining / m_missile / (max_time - t + 1e-6)
        acc_max = min(acc_max, 500.0)

    # --- Missile acceleration ---
    v_missile += acc_max * dt

    # --- Range update ---
    closing_speed = v_missile - v_fighter
    range_to_target += closing_speed * dt

    # --- Fuel consumption ---
    fuel_burn = acc_max * m_missile * dt
    fuel_remaining -= fuel_burn
    if fuel_remaining < 0:
        fuel_remaining = 0
        acc_max = 0

    # --- Turn rate derived from heat limit ---
    g_turn = min(heat_flux / (v_missile * missile_area + 1e-6), 50*g)  # m/s^2
    turn_rate = np.degrees(np.sqrt(g_turn / v_missile)) if v_missile > 0 else 0

    # --- Record ---
    time_list.append(t)
    v_list.append(v_missile)
    range_list.append(range_to_target)
    fuel_list.append(fuel_remaining)
    turn_rate_list.append(turn_rate)

# === Plots ===
plt.figure(figsize=(10,5))
plt.plot(time_list, v_list)
plt.xlabel('Time (s)')
plt.ylabel('Missile Velocity (m/s)')
plt.title('Missile Velocity vs Time (Physics-only, Air Volume)')
plt.grid(True)
plt.show()

plt.figure(figsize=(10,5))
plt.plot(time_list, turn_rate_list)
plt.xlabel('Time (s)')
plt.ylabel('Missile Turn Rate (deg/s)')
plt.title('Missile Turn Rate vs Time (Heat-limited, Air Volume)')
plt.grid(True)
plt.show()

plt.figure(figsize=(10,5))
plt.plot(time_list, fuel_list)
plt.xlabel('Time (s)')
plt.ylabel('Fuel Remaining (J)')
plt.title('Missile Fuel vs Time')
plt.grid(True)
plt.show()
