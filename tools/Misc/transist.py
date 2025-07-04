import math

# === Physical Constants ===
PLANCK_CONSTANT = 6.62607015e-34  # J·s
SPEED_OF_LIGHT = 299792458        # m/s
ATOMIC_DIAMETER_SI = 2.2e-10      # m

# Constants for fine structure calculation (your refined formula)
PHI = (1 + math.sqrt(5)) / 2
FINE_STRUCTURE_ALPHA = 4 * math.pi - 6
FINE_STRUCTURE_ALPHA = math.pow(FINE_STRUCTURE_ALPHA, PHI**2)

# === Transit Time and Power Calculations ===
transit_time = ATOMIC_DIAMETER_SI / SPEED_OF_LIGHT
crossings_per_second = 1 / transit_time
geometric_crossings = crossings_per_second ** (1/3)
power = crossings_per_second * PLANCK_CONSTANT
power_density = power / (ATOMIC_DIAMETER_SI ** 2)

# === Atom Density Over 1 m² ===
atoms_per_meter_side = 1 / ATOMIC_DIAMETER_SI
atoms_per_m2 = atoms_per_meter_side ** 2

# === Fine Structure Constant Calculations ===
alpha_phi = FINE_STRUCTURE_ALPHA ** PHI

# === Logic Unit Size Estimation Based on Thermal Budget ===
thermal_margin_ratio = 3**3  # 27, from previous empirical data
atoms_per_transistor_2d = round(alpha_phi)  # ~2900 atoms per transistor in 2D
total_atoms_per_logic_unit = thermal_margin_ratio * atoms_per_transistor_2d
logic_unit_side_atoms = total_atoms_per_logic_unit ** (1/3)

# === Error Margin and Failure Model ===
ERROR_MARGIN = 50  # Fixed atom count margin before failure
error_free_unit_size = atoms_per_transistor_2d - ERROR_MARGIN

# Calculate halvings to failure (base 2 logarithm of error_free_unit_size)
halvings_to_logic_unit_failure = math.log2(error_free_unit_size)

# Number of logic units (depth dimension from thermal margin ratio)
logic_units = thermal_margin_ratio

# Additional halvings needed to kill CPU after one logic unit fails (depth dimension)
additional_halvings_cpu_failure = math.log2(thermal_margin_ratio)

# Total halvings to CPU failure (logic unit + extra)
total_halvings_to_cpu_failure = halvings_to_logic_unit_failure + additional_halvings_cpu_failure

# === True FLOPS (serial logic ops per second) ===
true_flops = geometric_crossings * thermal_margin_ratio

# === Function to calculate compute power remaining given hits ===
def compute_power_remaining(hits: int) -> float:
    """
    Compute the fraction of compute power remaining after a given number of hits.
    
    Parameters:
        hits (int): Number of hits the CPU experienced.

    Returns:
        float: Fraction of compute power remaining (1.0 = full power, 0.0 = destroyed).
    """
    if hits <= halvings_to_logic_unit_failure:
        # No performance loss before logic unit failure threshold
        return 1.0
    else:
        excess_hits = hits - halvings_to_logic_unit_failure
        # Compute power halves with each additional hit beyond threshold
        return 1 / (2 ** excess_hits)

# === Output ===
print("=== Single Silicon Transistor Quantum Model ===")
print(f"Atomic diameter:                  {ATOMIC_DIAMETER_SI:.2e} m")
print(f"Transit time per atom:            {transit_time:.2e} s")
print(f"Crossings per second:             {crossings_per_second:.2e}")
print(f"Geometric crossings (per axis):  {geometric_crossings:.2e}")
print(f"Power (crossings × h):            {power:.2e} W")
print(f"Power density over 1 m²:          {power_density:.2e} W/m²")
print(f"Atoms over 1 m² area:             {atoms_per_m2:.2e}")

print("\n=== Fine Structure Constant and Phi ===")
print(f"Fine structure constant (alpha): {FINE_STRUCTURE_ALPHA:.8f}")
print(f"Golden ratio (phi):               {PHI:.8f}")
print(f"Alpha to the power of phi (α^φ): {alpha_phi:.8e}")

print("\n=== Logic Unit Atom Count Estimate ===")
print(f"Thermal margin ratio (depth):     {thermal_margin_ratio}")
print(f"Atoms per transistor (2D logic):  {atoms_per_transistor_2d}")
print(f"Total atoms per logic unit:       {total_atoms_per_logic_unit}")
print(f"Approx. cube side (atoms):        {logic_unit_side_atoms:.1f}")

print("\n=== Error Tolerance and Failure Model ===")
print(f"Error margin (atoms):             {ERROR_MARGIN}")
print(f"Error-free logic unit size:       {error_free_unit_size}")
print(f"Halvings to logic unit failure:  {halvings_to_logic_unit_failure:.2f}")
print(f"Additional halvings for CPU fail: {additional_halvings_cpu_failure:.2f}")
print(f"Total halvings to CPU failure:   {total_halvings_to_cpu_failure:.2f}")

print("\n=== True FLOPS Unit ===")
print(f"Actual logic operations per second (serial FLOPS): {true_flops:.2e}")

# === Example Usage of compute_power_remaining ===
example_hits = 12  # Example number of hits
remaining_power = compute_power_remaining(example_hits)
print(f"\nWith {example_hits} hits, remaining compute power fraction: {remaining_power:.4f}")