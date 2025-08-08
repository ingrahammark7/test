import math

# Constants
G = 6.67430e-11         # gravitational constant (m^3 kg^-1 s^-2)
e_mass = 9.10938356e-31 # electron mass (kg)
e_charge = 1.602176634e-19 # electron charge (C)
atomic_radius = 1.26e-10  # approximate atomic radius (meters, e.g. for Iron)
electron_velocity_thermal = 1e5  # rough thermal velocity of electron in m/s (order of magnitude)

# Planck mass roughly 2.176e-8 kg, you got about 2.39e-8 kg, so use yours:
planck_mass_grain = 2.39e-8  # kg

# Calculate gravitational acceleration on electron at atomic radius distance from mass grain
def gravitational_acceleration(mass, distance):
    return G * mass / (distance ** 2)

# Calculate time for electron to move one atomic radius under gravity alone
def time_to_cross_distance(accel, distance):
    # s = 0.5 * a * t^2  => t = sqrt(2s/a)
    if accel == 0:
        return float('inf')
    return math.sqrt(2 * distance / accel)

# Calculate displacement of electron over time given initial velocity and acceleration
def displacement(initial_velocity, acceleration, time):
    # s = vt + 0.5 * a * t^2
    return initial_velocity * time + 0.5 * acceleration * time ** 2

def main():
    distance = atomic_radius  # m
    mass = planck_mass_grain  # kg
    
    # Gravitational acceleration at atomic radius distance
    g_accel = gravitational_acceleration(mass, distance)
    print(f"Gravitational acceleration at {distance:.3e} m from {mass:.3e} kg mass: {g_accel:.3e} m/s²")

    # Time for electron to cross one atomic radius under gravity alone (starting from rest)
    t_cross = time_to_cross_distance(g_accel, distance)
    print(f"Time to cross one atomic radius under gravity alone: {t_cross:.3e} s")

    # Electron displacement due to thermal velocity only (ignore gravity)
    disp_thermal = displacement(electron_velocity_thermal, 0, t_cross)
    print(f"Electron displacement due to thermal velocity alone in that time: {disp_thermal:.3e} m")

    # Electron displacement including gravity acceleration
    disp_with_gravity = displacement(electron_velocity_thermal, g_accel, t_cross)
    print(f"Electron displacement with gravity acceleration included: {disp_with_gravity:.3e} m")

    # Calculate approximate thermal acceleration magnitude for comparison
    # a_thermal ~ v / t_cross (assuming linear acceleration for rough estimate)
    a_thermal = electron_velocity_thermal / t_cross
    print(f"Approximate electron thermal acceleration: {a_thermal:.3e} m/s²")

    print(g_accel)
    print(a_thermal**(1/6))
    # Compare gravity acceleration to thermal acceleration to decide dominance
    if g_accel > a_thermal**(1/6):
        print("Gravity dominates electron motion at this scale!")
    else:
        print("Electron motion dominated by other forces; gravity negligible at this scale.")

if __name__ == "__main__":
    main()