import math

# Constants
c = 3e8  # speed of light, m/s
v_target = 0.5 * c  # target velocity
m_payload = 1.0  # kg
sigma_sail = 1.0  # kg/m^2 sail areal mass density

# Atomic radius (distance between sheets)
atomic_radius = 1e-10  # meters

# Power density from electrostatic repulsion (Joules / seconds per m^2)
U = 36  # joules per event (energy between sheets)
t_event = 4.5e-15  # seconds per event
power_density = U / t_event  # W/m^2

def relativistic_ke(m, v):
    gamma = 1 / math.sqrt(1 - (v / c) ** 2)
    return m * c ** 2 * (gamma - 1)

def time_to_accelerate(A):
    total_mass = m_payload + sigma_sail * A
    KE = relativistic_ke(total_mass, v_target)
    total_power = power_density * A
    t = KE / total_power
    return t, total_mass, KE, total_power

# We'll find A that minimizes time t by scanning over a range of A
areas = [1e-12 * 2**i for i in range(60)]  # from 1 pm^2 up to ~1 m^2 exponentially

min_time = None
best_A = None
best_result = None

for A in areas:
    t, m_tot, KE, P_tot = time_to_accelerate(A)
    if (min_time is None) or (t < min_time):
        min_time = t
        best_A = A
        best_result = (t, m_tot, KE, P_tot)

t, m_tot, KE, P_tot = best_result

print(f"Best sail area: {best_A:.3e} m^2")
print(f"Total mass (payload + sail): {m_tot:.3f} kg")
print(f"Power available: {P_tot:.3e} W")
print(f"Kinetic energy needed: {KE:.3e} J")
print(f"Time to accelerate to 0.5c: {t:.3e} seconds ≈ {t / (3600 * 24 * 365):.2f} years")