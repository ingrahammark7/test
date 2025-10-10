#!/usr/bin/env python3
"""
nose_melting_speed_and_range_with_cap.py

Standalone program:
 - Material limits & stagnation-temperature based max Mach/speed (nose heating)
 - Missile defaults for AMRAAM and APEX (AA-7/R-23 style)
 - Fuel-fraction -> ideal rocket Δv -> coast range at given altitude
 - Quadratic drag coast model (analytical integration) until v <= v_thresh
 - Includes target fleeing at Mach 1: computes target distance during missile coast
 - NEW: optional global speed cap (--speed-cap) to arbitrarily limit speeds (m/s)
 - CLI with options. No plotting.

Note: Speed cap applies to:
 - the initial post-burn horizontal speed v0 (min(delta_v, speed_cap))
 - the reported stagnation-based max speed (used for heating info) is also capped for consistency.
"""

from math import sqrt, log, pi
import argparse
import csv
from typing import Dict, Any, List, Tuple

# ---------- Material database (temperatures in Kelvin)
MATERIALS: Dict[str, Dict[str, Any]] = {
    "steel_typical": {"description": "Typical carbon/low-alloy steel", "melting_point_k": 1673.0},
    "stainless_steel": {"description": "Stainless steel (approx)", "melting_point_k": 1650.0},
    "fiberglass_composite": {
        "description": "Glass-fiber composite (E-glass fibers in epoxy-like resin)",
        "fiber_melting_k": 1573.0,
        "matrix_decomposition_k": 623.0,
    },
}

# ---------- Missile defaults (representative)
MISSILES: Dict[str, Dict[str, Any]] = {
    "amraam": {"material": "fiberglass_composite", "altitude_m": 10000.0, "recovery_factor": 1.0,
               "m0_kg": 150.7, "diam_m": 0.178},
    "apex":   {"material": "steel_typical",      "altitude_m": 10000.0, "recovery_factor": 1.0,
               "m0_kg": 223.0, "diam_m": 0.200},
}

# ---------- Physics constants (SI)
GAMMA = 1.4
R_AIR = 287.05  # J/(kg K)
g0 = 9.80665  # m/s^2

# ---------- Atmosphere helpers
def isa_temperature_at_altitude(alt_m: float) -> float:
    if alt_m <= 11000.0:
        return 288.15 - 0.0065 * alt_m
    else:
        return 216.65

def isa_density_at_altitude(alt_m: float) -> float:
    if alt_m <= 11000.0:
        T0 = 288.15
        p0 = 101325.0
        lapse = -0.0065
        T = T0 + lapse * alt_m
        exponent = -g0 / (R_AIR * lapse)
        p = p0 * (T / T0) ** exponent
        rho = p / (R_AIR * T)
        return rho
    else:
        return 0.4135

def speed_of_sound(temperature_k: float) -> float:
    return sqrt(GAMMA * R_AIR * temperature_k)

# ---------- Stagnation temperature / Mach helpers
def stagnation_temperature_from_mach(M: float, ambient_temp_k: float, recovery_factor: float = 1.0) -> float:
    return ambient_temp_k * (1.0 + recovery_factor * (GAMMA - 1.0) / 2.0 * M * M)

def mach_from_stagnation_temp(T_stag_k: float, ambient_temp_k: float, recovery_factor: float = 1.0) -> float:
    ratio = T_stag_k / ambient_temp_k
    denom = recovery_factor * (GAMMA - 1.0) / 2.0
    if ratio <= 1.0 or denom <= 0.0:
        return 0.0
    return sqrt(max(0.0, (ratio - 1.0) / denom))

def material_operational_limit(material_key: str) -> float:
    if material_key not in MATERIALS:
        raise KeyError(f"Material '{material_key}' not in database.")
    m = MATERIALS[material_key]
    if "melting_point_k" in m:
        return m["melting_point_k"]
    fiber = m.get("fiber_melting_k", 1e6)
    matrix = m.get("matrix_decomposition_k", 1e6)
    return min(fiber, matrix)

# ---------- Range model (instantaneous burn -> coast under quadratic drag)
def delta_v_from_fuel_fraction(m0: float, fuel_fraction: float, Isp_s: float) -> Tuple[float, float]:
    if not (0.0 < fuel_fraction < 1.0):
        raise ValueError("fuel_fraction must be between 0 and 1 (exclusive).")
    mf = m0 * (1.0 - fuel_fraction)
    Ve = Isp_s * g0
    return Ve * log(m0 / mf), mf

def coast_range_quadratic_drag(v0: float, mass_kg: float, rho: float, Cd: float, area_m2: float, v_thresh: float = 10.0) -> Tuple[float, float]:
    if v0 <= v_thresh:
        return 0.0, 0.0
    k = 0.5 * rho * Cd * area_m2 / mass_kg
    if k <= 0.0:
        return float("inf"), float("inf")
    s = (1.0 / k) * log(v0 / v_thresh)
    flight_time = (v0 / v_thresh - 1.0) / (k * v0)
    return s, flight_time

# ---------- Presentation & CSV writer
def format_table(rows: List[Dict[str, Any]]) -> str:
    headers = ["missile", "m0_kg", "dry_mass_kg", "propellant_kg", "delta_v_m_s",
               "speed_cap_m_s", "frontal_area_m2", "drag_k", "range_m", "range_km", "flight_time_s",
               "ambient_temp_K", "material_limit_K", "max_mach", "max_speed_m_s",
               "target_speed_m_s", "target_distance_m", "net_effective_range_m", "net_effective_range_km"]
    col_widths = {h: len(h) for h in headers}
    formatted_rows = []
    for r in rows:
        fr = {
            "missile": str(r.get("missile", "")),
            "m0_kg": f'{r.get("m0_kg",0):.2f}',
            "dry_mass_kg": f'{r.get("dry_mass_kg",0):.3f}',
            "propellant_kg": f'{r.get("propellant_kg",0):.3f}',
            "delta_v_m_s": f'{r.get("delta_v_m_s",0):.1f}',
            "speed_cap_m_s": f'{r.get("speed_cap_m_s", "None") if r.get("speed_cap_m_s", None) is None else f"{r.get("speed_cap_m_s"):.1f}"}',
            "frontal_area_m2": f'{r.get("frontal_area_m2",0):.5f}',
            "drag_k": f'{r.get("drag_k",0):.6f}',
            "range_m": f'{r.get("range_m",0):.1f}',
            "range_km": f'{r.get("range_km",0):.3f}',
            "flight_time_s": f'{r.get("flight_time_s",0):.1f}',
            "ambient_temp_K": f'{r.get("ambient_temp_K",0):.2f}',
            "material_limit_K": f'{r.get("material_limit_K",0):.2f}',
            "max_mach": f'{r.get("max_mach",0):.3f}',
            "max_speed_m_s": f'{r.get("max_speed_m_s",0):.1f}',
            "target_speed_m_s": f'{r.get("target_speed_m_s",0):.1f}',
            "target_distance_m": f'{r.get("target_distance_m",0):.1f}',
            "net_effective_range_m": f'{r.get("net_effective_range_m",0):.1f}',
            "net_effective_range_km": f'{r.get("net_effective_range_km",0):.3f}',
        }
        formatted_rows.append(fr)
        for h in headers:
            col_widths[h] = max(col_widths[h], len(fr[h]))
    sep = " | "
    header_line = sep.join(h.ljust(col_widths[h]) for h in headers)
    divider = "-+-".join("-" * col_widths[h] for h in headers)
    lines = [header_line, divider]
    for fr in formatted_rows:
        lines.append(sep.join(fr[h].ljust(col_widths[h]) for h in headers))
    return "\n".join(lines)

def write_csv(filename: str, rows: List[Dict[str, Any]]):
    fieldnames = list(rows[0].keys()) if rows else []
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

# ---------- CLI
def parse_args():
    p = argparse.ArgumentParser(description="Estimate nose heating limits, coast range and net effective range against a fleeing target (Mach 1).")
    p.add_argument("target", nargs="?", default="all", choices=list(MISSILES.keys()) + ["all"],
                   help="Missile name (amraam, apex) or 'all'")
    p.add_argument("--fuel-fraction", type=float, default=0.90, help="Propellant fraction of launch mass (0..1). Default 0.90")
    p.add_argument("--Isp", type=float, default=250.0, help="Specific impulse (s). Default 250 s")
    p.add_argument("--Cd", type=float, default=0.20, help="Drag coefficient (dimensionless). Default 0.20")
    p.add_argument("--v-thresh", type=float, default=10.0, help="Threshold speed (m/s) to end coast. Default 10 m/s")
    p.add_argument("--altitude", type=float, default=None, help="Override altitude (m). If omitted uses missile default (10 km).")
    p.add_argument("--speed-cap", type=float, default=None, help="Optional global speed cap in m/s. Applies to initial post-burn speed and reported heating speed. Use to trade speed for range.")
    p.add_argument("--csv", type=str, default=None, help="Write results to CSV filename")
    p.add_argument("--show-materials", action="store_true", help="List materials and exit")
    p.add_argument("--show-missiles", action="store_true", help="List missile defaults and exit")
    return p.parse_args()

def main():
    args = parse_args()
    if args.show_materials:
        print("Materials:")
        for k, v in MATERIALS.items():
            print(f" - {k}: {v}")
        return
    if args.show_missiles:
        print("Missiles (defaults):")
        for k, v in MISSILES.items():
            print(f" - {k}: {v}")
        return

    targets = [args.target] if args.target != "all" else list(MISSILES.keys())
    results: List[Dict[str, Any]] = []

    for t in targets:
        params = MISSILES[t].copy()
        if args.altitude is not None:
            params["altitude_m"] = float(args.altitude)

        m0 = float(params["m0_kg"])
        diam = float(params["diam_m"])
        fuel_frac = float(args.fuel_fraction)
        Isp = float(args.Isp)
        Cd = float(args.Cd)
        altitude = float(params["altitude_m"])
        recovery = float(params.get("recovery_factor", 1.0))
        speed_cap = float(args.speed_cap) if args.speed_cap is not None else None

        # Atmosphere
        Ta = isa_temperature_at_altitude(altitude)
        rho = isa_density_at_altitude(altitude)

        # Material limit and max stagnation-based speed & Mach (informational)
        mat_key = params["material"]
        Tlimit = material_operational_limit(mat_key)
        max_mach = mach_from_stagnation_temp(Tlimit, Ta, recovery)
        max_speed_m_s = max_mach * speed_of_sound(Ta)
        # Apply speed cap to heating info as well (informational)
        if speed_cap is not None:
            max_speed_m_s = min(max_speed_m_s, speed_cap)
            max_mach = max_speed_m_s / speed_of_sound(Ta)

        # Delta-v and dry mass after fuel burn (instantaneous ideal rocket)
        delta_v, mf = delta_v_from_fuel_fraction(m0, fuel_frac, Isp)
        dry_mass = mf
        propellant_kg = m0 - mf

        # Apply speed cap to initial post-burn v0 (to intentionally limit top speed and extend range)
        v0_uncapped = delta_v
        v0 = delta_v if speed_cap is None else min(delta_v, speed_cap)

        # Frontal area and drag constant k
        area = pi * (diam / 2.0) ** 2
        k = 0.5 * rho * Cd * area / dry_mass

        # Coast range using analytic formula until v_thresh
        s_m, t_s = coast_range_quadratic_drag(v0, dry_mass, rho, Cd, area, args.v_thresh)

        # Target fleeing at Mach 1 at the same altitude
        v_target = speed_of_sound(Ta) * 1.0  # Mach 1
        target_distance_m = v_target * t_s

        # Net effective range: missile coast range minus distance target flees during missile coast
        net_effective_range_m = s_m - target_distance_m
        net_effective_range_km = net_effective_range_m / 1000.0

        result = {
            "missile": t,
            "m0_kg": round(m0, 2),
            "dry_mass_kg": round(dry_mass, 3),
            "propellant_kg": round(propellant_kg, 3),
            "delta_v_m_s": round(delta_v, 1),
            "speed_cap_m_s": None if speed_cap is None else round(speed_cap, 1),
            "v0_uncapped_m_s": round(v0_uncapped, 1),
            "v0_used_m_s": round(v0, 1),
            "frontal_area_m2": round(area, 5),
            "drag_k": round(k, 6),
            "range_m": round(s_m, 1),
            "range_km": round(s_m / 1000.0, 3),
            "flight_time_s": round(t_s, 1),
            "ambient_temp_K": round(Ta, 2),
            "material_limit_K": round(Tlimit, 2),
            "max_mach": round(max_mach, 3),
            "max_speed_m_s": round(max_speed_m_s, 1),
            "target_speed_m_s": round(v_target, 1),
            "target_distance_m": round(target_distance_m, 1),
            "net_effective_range_m": round(net_effective_range_m, 1),
            "net_effective_range_km": round(net_effective_range_km, 3),
        }
        results.append(result)

    if not results:
        print("No results (check inputs).")
        return

    print("\nAssumptions:")
    print(f" - Fuel fraction (propellant/m0): {args.fuel_fraction}")
    print(f" - Isp: {args.Isp} s, g0: {g0} m/s^2")
    print(f" - Drag model: quadratic, Cd = {args.Cd}")
    print(f" - Coast ends when speed <= {args.v_thresh} m/s")
    if args.speed_cap is not None:
        print(f" - Global speed cap applied: {args.speed_cap} m/s (limits v0 and reported heating speed).")
    else:
        print(" - No global speed cap applied.")
    print(" - Instantaneous-burn ideal-rocket Δv, no burn losses, horizontal coast at listed altitude")
    print(" - Target is fleeing at Mach 1 at the same altitude (target distance = Mach1_speed * missile_coast_time)\n")

    # print table (table format includes speed_cap column)
    print(format_table(results))

    if args.csv:
        write_csv(args.csv, results)
        print(f"\nWrote results to {args.csv}")

if __name__ == "__main__":
    main()