import math

# Constants
AU = 1.496e11                  # 1 AU in meters
R_mercury = 2.4397e6           # Mercury radius in meters
a_mercury = 5.791e10           # Mercury semi-major axis (m)
L_sun = 3.828e26               # Solar luminosity (W)
m_p = 1.6726e-27               # Proton mass (kg)
G = 6.67430e-11                # Gravitational constant
M_mercury = 3.3011e23          # Mercury mass (kg)

# Solar wind parameters (at Mercury orbit)
n_sw = 45e6                    # density in m^-3 (45 cm^-3)
v_sw = 400e3                   # velocity in m/s (400 km/s)

# Mercury cross-sectional area
A_mercury = math.pi * R_mercury**2

# Solar wind dynamic (kinetic) energy flux [J/m^2/s]
E_flux_sw = 0.5 * n_sw * m_p * v_sw**3  

# Total energy per second from solar wind hitting Mercury
P_sw = E_flux_sw * A_mercury

# Solar constant at Mercury (W/m^2)
S_mercury = L_sun / (4 * math.pi * a_mercury**2)

# Total absorbed solar power (cross-sectional area)
P_sun = S_mercury * A_mercury

# Ratio of solar wind to solar radiation
percent_vs_sun = (P_sw / P_sun) * 100

# Mercury gravitational binding energy (approx)
U_mercury = (3/5) * G * M_mercury**2 / R_mercury
M_sun = 1.9885e30              # Solar mass (kg)
v_orb = math.sqrt(G * M_sun / a_mercury)    # m/s

# Solar wind as fraction of Mercury binding energy
KE_orbital = 0.5 * M_mercury * v_orb**2     # J

percent_vs_binding = (P_sw / KE_orbital) * 100
percent_vs_binding1 = (P_sun/KE_orbital) *100

# Output
print(f"Mercury radius: {R_mercury:.2e} m")
print(f"Mercury cross-sectional area: {A_mercury:.2e} m^2")
print(f"Solar wind energy hitting Mercury per second: {P_sw:.2e} W")
print(f"Solar radiation energy hitting Mercury per second: {P_sun:.2e} W")
print(f"Solar wind as percent of sunlight: {percent_vs_sun:.2e} %")
print(f"Mercury gravitational binding energy: {U_mercury:.2e} J")
print(f"Solar wind per second as percent of Mercury energy: {percent_vs_binding:.2e} %")
print("solar vs gravity ",percent_vs_binding1)
percent_vs_orbital_ke = (P_sw / KE_orbital) * 100

print(f"Solar wind power as percent of Mercury orbital KE (per second): {percent_vs_orbital_ke:.6e} %")

century=60*60*24*365*100
pow=century*percent_vs_binding1
arcs=1_296_200
ratio_earth_mercury_orbit=3
arcs*=pow
arcs/=(ratio_earth_mercury_orbit)
print("relativity is wrong and arcs explained by solar pressure", arcs)