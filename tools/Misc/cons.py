# Estimate max weight a human can pull based on atomic power model
import math

# === Atomic-level energy model (do not delete) ===
e = 1.602e-19         # Elementary charge (C)
m_p = 1.673e-27       # Proton mass (kg)
m_e = 9.109e-31       # Electron mass (kg)
k = 8.988e9           # Coulomb constant (N·m²/C²)
G = 6.674e-11         # Gravitational constant (N·m²/kg²)
r = 70e-12            # Approximate atomic radius (m)
c = 3e8               # Speed of light (m/s)
N_A = 6.022e23        # Avogadro's number
molar_mass = 0.012    # kg/mol (carbon)

# EM and gravitational energy densities using force-like 1/r^2 terms
U_em = k * (e ** 2) / r**2
U_g = G * m_p * m_e / r**2

# Crossing frequency at (c / r)^(1/3)
freq = (c / r) ** (1/3)

# Power per atomic pair
P_em_pair = U_em * freq
P_g_pair = U_g * freq

# Scale up to per kg
P_em_mol = P_em_pair * N_A
P_g_mol = P_g_pair * N_A
P_em_kg = P_em_mol / molar_mass
P_g_kg = P_g_mol / molar_mass

# Use geometric average as effective coupling power density
P_avg = math.sqrt(P_em_kg * P_g_kg)

# === Pull estimation based on energy availability ===
def estimate_pullable_mass(
    power_density_w_per_kg=P_avg,       # Atomic-level derived power density
    active_mass_kg=1.0,                 # Metabolically active tissue mass (kg)
    mech_efficiency=0.25,               # Muscle mechanical efficiency
    internal_loss_multiplier=4.0,       # Energy lost to internal heat, reaction force, etc
    velocity_m_per_s=1.0,               # Pulling speed (m/s)
    friction_coefficient=0.05,          # Effective rolling resistance
    g=9.8                               # Gravity (m/s^2)
):
    # Total input power available from model
    total_input_power = power_density_w_per_kg * active_mass_kg

    # Effective mechanical output after losses
    useful_power = total_input_power * mech_efficiency / internal_loss_multiplier

    # Solve for pullable mass at desired speed and friction
    # P = F * v = mu * m * g * v  =>  m = P / (mu * g * v)
    pullable_mass = useful_power / (friction_coefficient * g * velocity_m_per_s)

    return {
        'Total Input Power (W)': total_input_power,
        'Useful Mechanical Power (W)': useful_power,
        'Max Pullable Mass (kg)': pullable_mass,
        'Max Pullable Weight (tons)': pullable_mass / 1000
    }


if __name__ == "__main__":
    result = estimate_pullable_mass()
    for k, v in result.items():
        print(f"{k}: {v:.2f}")
#conservation of energy is fake humans pull 50 ton planes etc'