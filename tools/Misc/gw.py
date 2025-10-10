"""
nose_melting_speed.py

Program to estimate maximum flight speed (and Mach) for a missile nose based on
material temperature limits (melting point, matrix decomposition) using
stagnation/adiabatic recovery temperature as the limiting factor.

Assumptions / model:
 - Ideal-gas stagnation temperature for compressible flow around a blunt body:
      T0 = Ta * (1 + r*(gamma-1)/2 * M^2)
   where r is the recovery factor (0..1). For high-speed blunt bodies r~1.
 - Uses a simple ISA atmosphere model to get ambient temperature vs altitude.
 - Material limit for composites is the lower of matrix decomposition temp and
   fiber melting temp.
 - Outputs both Mach and speed (m/s and km/h).

This is a tool meant to be iterated on — tell me the features you want and I
will add them (ablation model, real material datasets, convective heating
estimates, nose radius/heat flux-based limits, stagnation-point heat flux,
transient heating, radiation, etc.).

Units: SI (meters, seconds, Kelvin).
"""

from math import sqrt

# ---------- Material database (default values). These are typical/approximate.
# Temperatures are in Kelvin.
MATERIALS = {
    "steel_typical": {
        "description": "Typical carbon/low-alloy steel (melting range varies by alloy)",
        "melting_point_k": 1673.0,  # ~1400°C (typical mid-range)
    },
    "stainless_steel": {
        "description": "Stainless steel (approximate)",
        "melting_point_k": 1650.0,
    },
    "fiberglass_composite": {
        "description": "Glass-fiber composite (E-glass fibers in an epoxy-like resin)",
        # Fiber melting (glass) is very high, but matrix (resin) decomposes much lower.
        # Use matrix decomposition / softening as practical limit for structural integrity.
        "fiber_melting_k": 1573.0,  # ~1300°C (glass fiber softens/melts at very high T)
        "matrix_decomposition_k": 623.0,  # ~350°C typical epoxy decomposition
    },
}

# ---------- Physics / atmosphere helpers
GAMMA = 1.4  # ratio of specific heats for air (approx)
R_AIR = 287.05  # J/(kg K)

def isa_temperature_at_altitude(alt_m: float) -> float:
    """Simple ISA layer: returns ambient temperature (K) at given geopotential
    altitude in meters. Valid for troposphere (alt <= 11 km) and a simple
    stratosphere approximation beyond that.
    """
    if alt_m <= 11000:
        # Troposphere lapse rate -6.5 K/km
        T0 = 288.15
        lapse = -0.0065
        return T0 + lapse * alt_m
    else:
        # Isothermal layer approx (11-20 km): ~216.65 K
        return 216.65


def speed_of_sound(temperature_k: float) -> float:
    """Speed of sound in air at temperature T (K)."""
    return sqrt(GAMMA * R_AIR * temperature_k)


def stagnation_temperature_from_mach(M: float, ambient_temp_k: float, recovery_factor: float = 1.0) -> float:
    """Compute stagnation (recovery) temperature for a given Mach number.
    T0 = Ta * (1 + r*(gamma-1)/2 * M^2)
    r = recovery_factor (0..1). r near 1 for high-speed stagnation.
    """
    return ambient_temp_k * (1.0 + recovery_factor * (GAMMA - 1.0) / 2.0 * M * M)


def mach_from_stagnation_temp(T_stag_k: float, ambient_temp_k: float, recovery_factor: float = 1.0) -> float:
    """Invert stagnation temperature formula to get Mach number (>=0).
    M = sqrt( 2/(r*(gamma-1)) * (T0/Ta - 1) )
    """
    ratio = T_stag_k / ambient_temp_k
    denom = recovery_factor * (GAMMA - 1.0) / 2.0
    if ratio <= 1.0 or denom <= 0:
        return 0.0
    return sqrt(max(0.0, (ratio - 1.0) / denom))

# ---------- High-level utility functions

def material_operational_limit(material_key: str) -> float:
    """Return an operational temperature limit (K) for the material.
    For composites, returns the lower of matrix decomposition and fiber melt.
    For metals, returns the melting_point_k.
    If key not found, raises KeyError.
    """
    m = MATERIALS[material_key]
    if "melting_point_k" in m:
        return m["melting_point_k"]
    # composite-like
    fiber = m.get("fiber_melting_k", 1e6)
    matrix = m.get("matrix_decomposition_k", 1e6)
    return min(fiber, matrix)


def max_speed_for_material_at_altitude(material_key: str, altitude_m: float, recovery_factor: float = 1.0) -> dict:
    """Estimate the maximum Mach and speed (m/s) at a given altitude such that
    the stagnation temperature does not exceed the material operational limit.

    Returns a dict with keys: material_key, alt_m, ambient_temp_k, limit_temp_k,
    max_mach, max_speed_m_s, max_speed_km_h, recovery_factor
    """
    Ta = isa_temperature_at_altitude(altitude_m)
    Tlimit = material_operational_limit(material_key)
    M_max = mach_from_stagnation_temp(Tlimit, Ta, recovery_factor)
    a = speed_of_sound(Ta)
    v = M_max * a
    return {
        "material": material_key,
        "altitude_m": altitude_m,
        "ambient_temp_k": Ta,
        "limit_temp_k": Tlimit,
        "recovery_factor": recovery_factor,
        "max_mach": M_max,
        "max_speed_m_s": v,
        "max_speed_km_h": v * 3.6,
    }

# ---------- Example CLI usage when run as script
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Estimate maximum speed before material temperature limit is exceeded.")
    parser.add_argument("material", type=str, choices=list(MATERIALS.keys()), help="Material key (see defaults in file)")
    parser.add_argument("-a", "--altitude", type=float, default=0.0, help="Altitude in meters (default sea level)")
    parser.add_argument("-r", "--recovery", type=float, default=1.0, help="Recovery factor r (0..1). Default 1.0 for conservative stagnation temp")
    args = parser.parse_args()

    out = max_speed_for_material_at_altitude(args.material, args.altitude, args.recovery)
    print(f"Material: {out['material']} \nDescription: {MATERIALS[out['material']].get('description','')}")
    print(f"Altitude: {out['altitude_m']} m")
    print(f"Ambient temperature: {out['ambient_temp_k']:.1f} K")
    print(f"Material limit temperature: {out['limit_temp_k']:.1f} K")
    print(f"Recovery factor: {out['recovery_factor']}")
    print(f"Max Mach (limit): {out['max_mach']:.3f}")
    print(f"Max speed: {out['max_speed_m_s']:.1f} m/s  ({out['max_speed_km_h']:.1f} km/h)")

    # Example note
    print("\nNote: For fiberglass composites the limiting temperature is usually the resin\nmatrix decomposition/softening temperature (much lower than fiber melting).\nThis simple model uses stagnation temperature only and ignores transient heating,\nablative mass loss, and detailed heat-flux-based thermal protection design.")

