import numpy as np

# Constants
volume_air = 5.1e18        # m³, troposphere volume
water_density = 10         # g/m³ average vapor
water_mass = volume_air * water_density  # grams
molar_mass_water = 18      # g/mol
mol_water = water_mass / molar_mass_water

# Water molecules globally
NA = 6.022e23
water_molecules = mol_water * NA

# Salt parameters
mol_salt = 1e6             # Try 1 million mol as an example
ions_per_mol = 2
total_ions = mol_salt * ions_per_mol * NA

# Contact rate (ion touches 1 molecule/sec)
contact_time = 6.05e5  # seconds (1 week)
total_contacts_per_ion = contact_time
total_contacts_possible = total_ions * total_contacts_per_ion

# Efficiency: what percent of water gets touched?
efficacy = total_contacts_possible / water_molecules

print(f"Water molecules in air: {water_molecules:.2e}")
print(f"Total salt ions released: {total_ions:.2e}")
print(f"Total ion-molecule contacts: {total_contacts_possible:.2e}")
print(f"Coverage efficacy: {efficacy:.4f} ({efficacy*100:.2f}%)")
print(f"Salt mass: {mol_salt * 58.5:.2f} g ({(mol_salt * 58.5)/1e6:.2f} tonnes)")

import numpy as np

# Constants
stefan_boltzmann = 5.670374419e-8  # W/m²K⁴
earth_surface_area = 5.1e14  # m²
baseline_temp_K = 288  # Approx 15°C in Kelvin
temp_increase_K = 3  # Estimated average global warming (3°C)
new_temp_K = baseline_temp_K + temp_increase_K

# Calculate radiated power before and after warming
radiated_power_baseline = stefan_boltzmann * earth_surface_area * baseline_temp_K**4
radiated_power_warmed = stefan_boltzmann * earth_surface_area * new_temp_K**4

# Excess heat loss rate
excess_radiation = radiated_power_warmed - radiated_power_baseline  # W

# Assume total excess heat added due to warming is 2.9e23 J (IPCC rough estimate)
total_excess_heat = 2.9e23  # J

# Time to lose half of that excess energy
half_excess_heat = total_excess_heat / 2
time_seconds = half_excess_heat / excess_radiation
time_years = time_seconds / (60 * 60 * 24 * 365.25)

print(excess_radiation, time_years)

import numpy as np

# Example parameters (tune these to fit your context)
eta_0 = 1.0          # Base efficiency at low ion molarity
M_crit = 1e-9        # Critical molarity threshold (mol/m³)
alpha = 1e10         # Decay rate of efficiency beyond threshold (1/(mol/m³))

# Compute ion molarity M in mol/m³
# mol_salt = total salt mol (already defined)
# volume_air = total atmospheric volume in m³ (already defined)

M = mol_salt / volume_air  # mol/m³

# CCN efficiency factor with saturation decay beyond M_crit
def ccn_efficiency(M, eta_0, M_crit, alpha):
    excess = max(0, M - M_crit)
    return eta_0 * np.exp(-alpha * excess)

eta = ccn_efficiency(M, eta_0, M_crit, alpha)

# Update efficacy with saturation effect
efficacy_saturated = efficacy * eta

print(f"Ion molarity M: {M:.2e} mol/m³")
print(f"CCN efficiency factor eta: {eta:.4f}")
print(f"Original efficacy: {efficacy:.6f}")
print(f"Saturation-adjusted efficacy: {efficacy_saturated:.6f}")

import numpy as np
import matplotlib.pyplot as plt

# Parameters
length = 1e6          # domain length in meters (1000 km)
nx = 200              # number of spatial points
dx = length / (nx-1)  # spatial step

dt = 60               # time step in seconds (1 minute)
nt = 1440             # number of time steps (1 day simulation)

v = 10                # wind speed m/s (advection)
D = 50                # diffusion coefficient m²/s
lambda_loss = 1e-6    # loss rate per second (deposition/scavenging)

# Source: ion injection at x=0 (e.g., industrial region)
source_rate = 1e-9    # mol/m³/s injection rate at left boundary

# Initialize concentration array (mol/m³)
C = np.zeros(nx)

# Precompute coefficients for stability (explicit scheme)
adv_coeff = v * dt / dx
diff_coeff = D * dt / dx**2

# Stability check (simple)
if adv_coeff > 1 or diff_coeff > 0.5:
    print("Warning: Time step too large for stability. Reduce dt or increase dx.")

# Time stepping loop
for t in range(nt):
    C_new = np.copy(C)
    
    # Interior points update: explicit scheme
    for i in range(1, nx-1):
        adv_term = -v * (C[i] - C[i-1]) / dx
        diff_term = D * (C[i+1] - 2*C[i] + C[i-1]) / dx**2
        loss_term = -lambda_loss * C[i]
        
        C_new[i] = C[i] + dt * (adv_term + diff_term + loss_term)
    
    # Boundary conditions
    # Left boundary (source)
    C_new[0] = C[0] + dt * (source_rate - v * (C[0] - 0) / dx - lambda_loss * C[0])
    # Right boundary (open, zero gradient)
    C_new[-1] = C_new[-2]
    
    C = C_new

# Plot final concentration profile
x = np.linspace(0, length/1000, nx)  # km
plt.plot(x, C)
plt.xlabel('Distance downwind (km)')
plt.ylabel('Ion molarity (mol/m³)')
plt.title('Ion concentration after 1 day of transport')
plt.grid(True)
plt.show()