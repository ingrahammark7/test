import math

# Barrel parameters
L = 1.5           # Barrel length (m)
r = 0.05          # Inner radius (m)
t = 0.01          # Barrel thickness (m)
rho = 7850        # Steel density (kg/m^3)
c = 470           # Specific heat J/(kg*K)
T_plastic = 1000 + 273.15  # K
T_ambient = 300  # K

# Fraction of energy absorbed by barrel
f_barrel = 0.3  # 30% absorbed by barrel, 70% into mount/airframe

# Gun parameters: (name, total_energy_J, num_rounds)
guns = [
    ("MiG-21 GSh-6", 1.2e9, 500),
    ("F-4 SUU-16", 6e8, 1200),
    ("Su-15 GSh-6 x2", 2.4e9, 1000),  # 2 barrels combined
]

# Barrel mass
V = math.pi * L * ((r+t)**2 - r**2)
m_barrel = V * rho

print(f"Barrel mass: {m_barrel:.2f} kg\n")

for name, E_total, num_rounds in guns:
    E_round = E_total / num_rounds
    delta_T_round = E_round * f_barrel / (m_barrel * c)
    N_max = (T_plastic - T_ambient) / delta_T_round
    print(f"{name}:")
    print(f"  Energy per round: {E_round:.2e} J")
    print(f"  Temp rise per round: {delta_T_round:.2f} K")
    print(f"  Max rounds before plastic temp: {N_max:.1f}\n")