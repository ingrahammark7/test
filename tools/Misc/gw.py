# integrity_physical.py
import math

# Example Material dataclass (extend your pen.Material or adapt)
class MaterialPhysical:
    def __init__(self, name, density, youngs_modulus, yield_strength,
                 specific_heat, melting_point, thermal_conductivity,
                 strain_rate_C=0.02, ref_strain_rate=1.0, thermal_softening_coeff=0.001):
        self.name = name
        self.density = density
        self.E = youngs_modulus
        self.yield_strength = yield_strength
        self.specific_heat = specific_heat
        self.melting_point = melting_point
        self.thermal_conductivity = thermal_conductivity
        # simple dynamic strengthening coefficient (log form)
        self.strain_rate_C = strain_rate_C
        self.ref_strain_rate = ref_strain_rate
        # simple linear thermal softening % per K (or use Johnson-Cook)
        self.thermal_softening_coeff = thermal_softening_coeff

# Helper: velocity from kinetic energy (MJ->J)
def velocity_from_energy_mj(E_mj, mass_kg):
    E_j = E_mj * 1e6
    if mass_kg <= 0:
        return 0.0
    return math.sqrt(2.0 * E_j / mass_kg)

# Impedance-match pressure estimate (simple)
def impact_pressure_rho_v(rho_p, rho_t, v):
    # symmetric formula: ~ (rho_p * rho_t / (rho_p + rho_t)) * v^2
    denom = (rho_p + rho_t)
    if denom == 0:
        return 0.0
    return (rho_p * rho_t / denom) * v * v

# Dynamic yield (log-strain-rate boost)
def dynamic_yield(yield_strength, strain_rate_C, ref_strain_rate, strain_rate):
    if strain_rate <= 0:
        return yield_strength
    return yield_strength * (1.0 + strain_rate_C * math.log(max(strain_rate / ref_strain_rate, 1e-12)))

# Estimate strain rate approx from impact: v / characteristic_length
def estimate_strain_rate(v, length_m):
    if length_m <= 0:
        return 1.0
    return abs(v) / length_m

# Temperature rise from deposited energy in zone mass
def temperature_rise(energy_j, mass_zone_kg, specific_heat):
    if mass_zone_kg <= 0 or specific_heat <= 0:
        return 0.0
    return energy_j / (mass_zone_kg * specific_heat)

# Compute integrity (0..1)
def integrity_from_pressure(P, sigma_dyn, temp_increase, material: MaterialPhysical):
    # thermal softening: simple multiplicative factor (1 - k * dT)
    softening = 1.0 - material.thermal_softening_coeff * temp_increase
    softening = max(0.01, softening)  # floor to avoid negative
    sigma_effective = sigma_dyn * softening

    # if P <= sigma_effective -> intact (integrity ~1)
    if P <= sigma_effective:
        return 1.0, sigma_effective

    # otherwise integrity decays exponentially with overload ratio
    overload = (P - sigma_effective) / sigma_effective
    integrity = math.exp(-overload)  # can tune base
    integrity = max(0.0, min(1.0, integrity))
    return integrity, sigma_effective

# Example wrapper using the above:
def compute_penetrator_integrity(material_tgt: MaterialPhysical,
                                 projectile_mass_kg, projectile_diameter_m, projectile_energy_mj,
                                 interaction_zone_radius_m = 1e-4):
    """
    - material_tgt: MaterialPhysical object for target
    - projectile_mass_kg, projectile_diameter_m, projectile_energy_mj: projectile params
    - interaction_zone_radius_m: radius of local zone for energy deposition (tunable)
    Returns (integrity, diagnostics dict)
    """

    # 1) Compute impact velocity
    v = velocity_from_energy_mj(projectile_energy_mj, projectile_mass_kg)

    # 2) Estimate peak pressure using impedance-like formula
    rho_p = projectile_mass_kg / (math.pi * (projectile_diameter_m/2)**2 * 1.0)  # crude rod density per meter length
    rho_t = material_tgt.density
    P = impact_pressure_rho_v(rho_p, rho_t, v)

    # 3) estimate strain rate using interaction_zone size
    strain_rate = estimate_strain_rate(v, interaction_zone_radius_m)

    # 4) dynamic yield
    sigma_dyn = dynamic_yield(material_tgt.yield_strength, material_tgt.strain_rate_C, material_tgt.ref_strain_rate, strain_rate)

    # 5) temperature rise (assume fraction f_deposited of energy deposited in zone)
    energy_j = projectile_energy_mj * 1e6
    f_deposited = 0.2  # default fraction of energy locally deposited — you can compute more precisely later
    mass_zone = (4/3) * math.pi * (interaction_zone_radius_m**3) * rho_t
    dT = temperature_rise(energy_j * f_deposited, mass_zone, material_tgt.specific_heat)

    # 6) integrity from pressure and thermal softening
    integrity, sigma_effective = integrity_from_pressure(P, sigma_dyn, dT, material_tgt)

    diagnostics = {
        "v_m_s": v,
        "P_Pa": P,
        "strain_rate_1_s": strain_rate,
        "sigma_dyn_Pa": sigma_dyn,
        "sigma_effective_Pa": sigma_effective,
        "temp_rise_K": dT,
        "integrity": integrity,
        "mass_zone_kg": mass_zone
    }

    return integrity, diagnostics