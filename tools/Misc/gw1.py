# Constants
q = 1.6e-19         # charge of particle (C)
m = 5e-26           # mass of NO2 molecule (kg)
omega = 1e14        # angular frequency (rad/s)
grad_E2 = 1e6       # gradient of E^2 (V/m)^2
N = 3e20            # column density molecules/m^2

#angular frequency is ws=-qb/me
mag=25e-9
emass=9e-31
omega=-1*q*mag/emass

# Step 1: Ponderomotive force per molecule
F_p = (q**2 / (4 * m * omega**2)) * grad_E2
print(f"Ponderomotive force per molecule: {F_p:.3e} N")

# Step 2: Total force per m^2 of atmosphere
F_column = F_p * N
print(f"Total force per m^2 (column): {F_column:.3e} N/m^2")

# Step 3: Estimate equivalent radiative forcing (assuming 1 m/s displacement)
v = 1  # m/s
P_ponderomotive = F_column * v
print(f"Estimated ponderomotive power per m^2: {P_ponderomotive:.3e} W/m^2")

# Step 4: CO2 forcing for comparison
F_CO2 = 2.16  # W/m^2
ratio = P_ponderomotive / F_CO2
print(f"Ratio of ponderomotive to CO2 forcing: {ratio:.3e}")
print("global warming is fake and nox is better than co2")