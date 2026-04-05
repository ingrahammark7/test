import numpy as np
import matplotlib.pyplot as plt

# === Constants ===
g = 9.81  # m/s^2

# === Inputs ===
m_missile = 500       # kg
fuel_energy = 10e9    # J, total fuel energy
max_heat_flux = 300e6 # W/m^2, melting/structural limit

m_fighter = 20000     # kg
v_fighter_init = 340  # m/s
fighter_turn_rate_deg = 30  # deg/s
fighter_area = 50  # m^2 wing area

missile_area = 1.0    # m^2, effective air volume displaced

dt = 0.01
max_time = 30
range_start = 2000

# === Initial conditions ===
v_missile = 0.0
v_fighter = v_fighter_init
range_to_target = range_start
fuel_remaining = fuel_energy

m_fighter_pos = np.array([0.0,0.0])
m_missile_pos = np.array([-range_start,0.0])

fighter_heading = 0.0
missile_heading = 0.0

# Lists for plotting
v_list = []
range_list = []
fuel_list = []
turn_rate_missile_list = []
m_fighter_pos_list = []
m_missile_pos_list = []

for t in np.arange(0, max_time, dt):
    # --- Missile acceleration ---
    heat_flux = 0.5 * v_missile**3 * missile_area
    if heat_flux > max_heat_flux:
        acc_missile = 0.0
    else:
        acc_missile = fuel_remaining / m_missile / (max_time - t + 1e-6)
        acc_missile = min(acc_missile, 500.0)

    # Update missile velocity
    v_missile += acc_missile * dt

    # Fuel burn
    fuel_burn = acc_missile * m_missile * dt
    fuel_remaining -= fuel_burn
    if fuel_remaining < 0:
        fuel_remaining = 0
        acc_missile = 0

    # Turn rate based on heat limit
    g_turn = min(heat_flux / (v_missile * missile_area + 1e-6), 50*g)
    turn_rate_missile = np.degrees(np.sqrt(g_turn / v_missile)) if v_missile > 0 else 0

    # 2D headings
    fighter_heading += np.radians(fighter_turn_rate_deg) * dt * np.sin(t)
    missile_heading += np.radians(turn_rate_missile) * dt

    # Update positions
    m_fighter_pos += np.array([v_fighter * np.cos(fighter_heading), v_fighter * np.sin(fighter_heading)]) * dt
    m_missile_pos += np.array([v_missile * np.cos(missile_heading), v_missile * np.sin(missile_heading)]) * dt

    # Update range
    range_to_target = np.linalg.norm(m_missile_pos - m_fighter_pos)

    # Record
    v_list.append(v_missile)
    range_list.append(range_to_target)
    fuel_list.append(fuel_remaining)
    turn_rate_missile_list.append(turn_rate_missile)
    m_fighter_pos_list.append(m_fighter_pos.copy())
    m_missile_pos_list.append(m_missile_pos.copy())

# === Combined plot ===
plt.figure(figsize=(12,8))

plt.subplot(2,2,1)
plt.plot(range_list, v_list)
plt.xlabel('Range to Fighter (m)')
plt.ylabel('Missile Velocity (m/s)')
plt.grid(True)
plt.title('Missile Velocity')

plt.subplot(2,2,2)
plt.plot(range_list, turn_rate_missile_list)
plt.xlabel('Range to Fighter (m)')
plt.ylabel('Missile Turn Rate (deg/s)')
plt.grid(True)
plt.title('Missile Turn Rate')

plt.subplot(2,2,3)
plt.plot(range_list, fuel_list)
plt.xlabel('Range to Fighter (m)')
plt.ylabel('Fuel Remaining (J)')
plt.grid(True)
plt.title('Missile Fuel')

plt.subplot(2,2,4)
m_fighter_pos_list = np.array(m_fighter_pos_list)
m_missile_pos_list = np.array(m_missile_pos_list)
plt.plot(m_fighter_pos_list[:,0], m_fighter_pos_list[:,1], label='Fighter')
plt.plot(m_missile_pos_list[:,0], m_missile_pos_list[:,1], label='Missile')
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.title('2D Engagement Trajectory')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

