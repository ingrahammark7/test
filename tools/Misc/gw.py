import math

# -----------------------------
# Physical constants (silicon wafer)
# -----------------------------
wafer_diameter_m = 5e-9
wafer_radius_m = wafer_diameter_m / 2
wafer_area = math.pi * wafer_radius_m**2

wafer_thickness_m = 0.000775  # ~775 µm
silicon_density = 2330        # kg/m^3
silicon_cp = 700              # J/kg·K

wafer_volume = wafer_area * wafer_thickness_m
wafer_mass = wafer_volume * silicon_density
wafer_heat_capacity = wafer_mass * silicon_cp  # J/K

# -----------------------------
# Etch energy input (your earlier result)
# -----------------------------
E_etch = 1e-5 # Joules per etch step (typical mid-range)

# Initial temperature rise if no cooling during step
delta_T_initial = E_etch / wafer_heat_capacity

# -----------------------------
# Gas thermal conductance model (effective lumped parameter)
# -----------------------------
# These are EFFECTIVE coupling coefficients (not bulk gas physics)
# tuned to represent backside + chamber coupling differences

h_helium = 25   # W/K (effective helium-assisted cooling)
h_argon  = 5    # W/K (effective argon-assisted cooling)

# -----------------------------
# Cooling model
# T(t) = T0 * exp(-t / tau)
# tau = C / h
# -----------------------------
tau_he = wafer_heat_capacity / h_helium
tau_ar = wafer_heat_capacity / h_argon

def cooling_time_to_fraction(tau, fraction=0.01):
    """
    time to cool to given fraction of initial temperature rise
    fraction = 0.01 means 99% cooled
    """
    return -tau * math.log(fraction)

t_he_99 = cooling_time_to_fraction(tau_he, 0.01)
t_ar_99 = cooling_time_to_fraction(tau_ar, 0.01)

# -----------------------------
# Optional: atomic normalization
# -----------------------------
avogadro = 6.022e23
silicon_atomic_mass = 28.085  # g/mol

wafer_moles = (wafer_mass * 1000) / silicon_atomic_mass
wafer_atoms = wafer_moles * avogadro

energy_per_atom = E_etch / wafer_atoms

# -----------------------------
# Output
# -----------------------------
print("=== 5nm Etch Thermal Model ===")
print(f"Wafer heat capacity: {wafer_heat_capacity:.2f} J/K")
print(f"Energy per etch: {E_etch} J")
print(f"Initial ΔT (no cooling): {delta_T_initial:.2f} K")

print("\n--- Cooling constants ---")
print(f"Helium tau: {tau_he:.2f} s")
print(f"Argon tau: {tau_ar:.2f} s")

print("\n--- Time to 99% cooldown ---")
print(f"Helium: {t_he_99:.2f} s")
print(f"Argon: {t_ar_99:.2f} s")

print("\n--- Atomic scale ---")
print(f"Atoms per wafer: {wafer_atoms:.3e}")
print(f"Energy per atom per etch: {energy_per_atom:.3e} J")