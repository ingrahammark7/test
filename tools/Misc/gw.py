#!/usr/bin/env python3
"""
nose_melting_speed_full.py

Standalone program to estimate maximum flight speed (and Mach) for a missile nose
based on material temperature limits using stagnation/recovery temperature.

Features:
 - built-in materials (steel, stainless, fiberglass composite)
 - missile defaults (amraam, apex)
 - ISA ambient temperature vs altitude (troposphere + simple stratosphere)
 - stagnation temperature model with recovery factor
 - CLI: compute for a named missile or all missiles, optional CSV output

Units: SI (meters, seconds, Kelvin)
"""

from math import sqrt
import argparse
import csv
from typing import Dict, Any, List

# ---------- Material database (default values). Temperatures in Kelvin.
MATERIALS: Dict[str, Dict[str, Any]] = {
    "steel_typical": {
        "description": "Typical carbon/low-alloy steel",
        "melting_point_k": 1673.0,  # ~1400 °C
    },
    "stainless_steel": {
        "description": "Stainless steel (approx)",
        "melting_point_k": 1650.0,
    },
    "fiberglass_composite": {
        "description": "Glass-fiber composite (E-glass fibers in epoxy-like resin)",
        # Fiber melts very high but resin matrix decomposes much lower -> limiting.
        "fiber_melting_k": 1573.0,
        "matrix_decomposition_k": 623.0,  # ~350 °C
    },
}

# ---------- Missile defaults (used for convenience)
MISSILES: Dict[str, Dict[str, Any]] = {
    # Default altitude chosen as a representative operational altitude in meters.
    "amraam": {"material": "fiberglass_composite", "altitude_m": 5000.0, "recovery_factor": 1.0},
    "apex": {"material": "steel_typical", "altitude_m": 10000.0, "recovery_factor": 1.0},
}

# ---------- Physics constants
GAMMA = 1.4  # ratio of specific heats (air)
R_AIR = 287.05  # J/(kg K) gas constant for air


# ---------- Atmosphere / helper functions
def isa_temperature_at_altitude(alt_m: float) -> float:
    """
    Return ambient temperature (K) at given geopotential altitude (m) using
    a simple ISA model (troposphere lapse to 11 km, then isothermal 216.65 K).
    """
    if alt_m <= 11000.0:
        return 288.15 - 0.0065 * alt_m
    else:
        return 216.65


def speed_of_sound(temperature_k: float) -> float:
    """Speed of sound (m/s) at temperature (K)."""
    return sqrt(GAMMA * R_AIR * temperature_k)


def stagnation_temperature_from_mach(M: float, ambient_temp_k: float, recovery_factor: float = 1.0) -> float:
    """
    Stagnation (recovery) temperature for Mach M:
      T0 = Ta * (1 + r*(gamma-1)/2 * M^2)
    """
    return ambient_temp_k * (1.0 + recovery_factor * (GAMMA - 1.0) / 2.0 * M * M)


def mach_from_stagnation_temp(T_stag_k: float, ambient_temp_k: float, recovery_factor: float = 1.0) -> float:
    """
    Invert stagnation temperature to get Mach:
      M = sqrt( 2/(r*(gamma-1)) * (T0/Ta - 1) )
    """
    ratio = T_stag_k / ambient_temp_k
    denom = recovery_factor * (GAMMA - 1.0) / 2.0
    if ratio <= 1.0 or denom <= 0.0:
        return 0.0
    val = (ratio - 1.0) / denom
    return sqrt(max(0.0, val))


def material_operational_limit(material_key: str) -> float:
    """
    Return an operational temperature limit (K) for the given material.
    For composites returns the lower of fiber melt and matrix decomposition.
    For metals returns melting point.
    """
    if material_key not in MATERIALS:
        raise KeyError(f"Material '{material_key}' not found in database.")
    m = MATERIALS[material_key]
    if "melting_point_k" in m:
        return m["melting_point_k"]
    fiber = m.get("fiber_melting_k", 1e6)
    matrix = m.get("matrix_decomposition_k", 1e6)
    return min(fiber, matrix)


# ---------- Core computation
def estimate_max_speed(material_key: str, altitude_m: float, recovery_factor: float = 1.0) -> Dict[str, Any]:
    """
    Estimate maximum Mach and speed (m/s) at given altitude such that the stagnation
    temperature does not exceed the material operational limit.
    Returns a dict containing numeric results and inputs.
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


# ---------- Presentation helpers
def format_table(rows: List[Dict[str, Any]]) -> str:
    """Return a simple aligned ASCII table string for supplied result rows."""
    headers = ["missile", "material", "altitude_m", "ambient_temp_K", "material_limit_K", "max_mach", "max_speed_m_s", "max_speed_km_h"]
    col_widths = {h: len(h) for h in headers}
    # compute formatted strings first
    formatted_rows = []
    for r in rows:
        fr = {
            "missile": str(r.get("missile", "")),
            "material": str(r.get("material", "")),
            "altitude_m": f'{r.get("altitude_m", 0):.0f}',
            "ambient_temp_K": f'{r.get("ambient_temp_k", 0.0):.2f}',
            "material_limit_K": f'{r.get("limit_temp_k", 0.0):.2f}',
            "max_mach": f'{r.get("max_mach", 0.000):.3f}',
            "max_speed_m_s": f'{r.get("max_speed_m_s", 0.0):.1f}',
            "max_speed_km_h": f'{r.get("max_speed_km_h", 0.0):.1f}',
        }
        formatted_rows.append(fr)
        for h in headers:
            col_widths[h] = max(col_widths[h], len(fr[h]))
    # build table
    sep = " | "
    header_line = sep.join(h.ljust(col_widths[h]) for h in headers)
    divider = "-+-".join("-" * col_widths[h] for h in headers)
    lines = [header_line, divider]
    for fr in formatted_rows:
        lines.append(sep.join(fr[h].ljust(col_widths[h]) for h in headers))
    return "\n".join(lines)


def write_csv(filename: str, rows: List[Dict[str, Any]]):
    """Write rows list to CSV (selected columns)."""
    fieldnames = ["missile", "material", "altitude_m", "ambient_temp_k", "limit_temp_k", "recovery_factor", "max_mach", "max_speed_m_s", "max_speed_km_h"]
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            # normalize keys to expected CSV names
            writer.writerow({
                "missile": r.get("missile", ""),
                "material": r.get("material", ""),
                "altitude_m": r.get("altitude_m", 0.0),
                "ambient_temp_k": r.get("ambient_temp_k", 0.0),
                "limit_temp_k": r.get("limit_temp_k", 0.0),
                "recovery_factor": r.get("recovery_factor", 1.0),
                "max_mach": r.get("max_mach", 0.0),
                "max_speed_m_s": r.get("max_speed_m_s", 0.0),
                "max_speed_km_h": r.get("max_speed_km_h", 0.0),
            })


# ---------- CLI
def parse_args():
    parser = argparse.ArgumentParser(
        description="Estimate maximum speed for missile nose material limits (stagnation temperature model)."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="all",
        help="Missile name (amraam, apex) or 'all' (default).",
        choices=list(MISSILES.keys()) + ["all"],
    )
    parser.add_argument(
        "--altitude",
        type=float,
        help="Override altitude in meters (overrides missile default).",
    )
    parser.add_argument(
        "--material",
        type=str,
        help="Override material key (use a key from MATERIALS).",
        choices=list(MATERIALS.keys()),
    )
    parser.add_argument(
        "--recovery",
        type=float,
        default=None,
        help="Override recovery factor r (0..1). If omitted uses missile default.",
    )
    parser.add_argument(
        "--csv",
        type=str,
        help="Write results to CSV file (filename).",
    )
    parser.add_argument(
        "--show-materials",
        action="store_true",
        help="List known materials and their properties, then exit.",
    )
    parser.add_argument(
        "--show-missiles",
        action="store_true",
        help="List known missile defaults and exit.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.show_materials:
        print("Known materials:")
        for k, v in MATERIALS.items():
            print(f" - {k}: {v.get('description','')} -> {v}")
        return

    if args.show_missiles:
        print("Known missile defaults:")
        for k, v in MISSILES.items():
            print(f" - {k}: {v}")
        return

    targets = [args.target] if args.target != "all" else list(MISSILES.keys())
    results = []

    for t in targets:
        params = MISSILES[t].copy()
        # apply overrides if provided
        if args.altitude is not None:
            params["altitude_m"] = float(args.altitude)
        if args.material is not None:
            params["material"] = args.material
        if args.recovery is not None:
            params["recovery_factor"] = float(args.recovery)

        # compute
        try:
            res = estimate_max_speed(params["material"], params["altitude_m"], params.get("recovery_factor", 1.0))
            # add missile name and original param values for clarity
            res["missile"] = t
            res["recovery_factor"] = params.get("recovery_factor", 1.0)
            results.append(res)
        except KeyError as e:
            print(f"Error for target '{t}': {e}")

    if not results:
        print("No results generated.")
        return

    # Print table
    print(format_table(results))

    # Optional CSV output
    if args.csv:
        write_csv(args.csv, results)
        print(f"\nWrote results to {args.csv}")


if __name__ == "__main__":
    main()