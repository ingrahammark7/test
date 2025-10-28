# Python code to generate tank specs from just length and name.
# This is a high-level simulation for modeling/speciation purposes.
# Penetration is given as a dimensionless "penetration_score" (relative), not an absolute real-world mm value.
# Tune coefficients as needed for your in-pen calibration.

import pandas as pd, math, json
import jupyter

# Tuning coefficients (can be adjusted)
COEFF = {
    "width_frac": 0.5,
    "height_frac": 0.5,
    "hull_density": 600,     # kg/m^3 effective structural+armor density (tunable)
    "hull_mass_factor": 0.53, # mass fraction from earlier example scaling
    "engine_mass_per_volume": 94, # kg engine per m^3 hull volume approx (tunable)
    "engine_power_density": 180, # W/kg for engine mass -> rough (tunable) (i.e., 180 W/kg)
    "stroke_frac_of_width": 3.15, # stroke ~ stroke_frac * piston_width (from dataset rough)
    "piston_width_frac": 0.68, # piston width relative to width fraction mapping (tunable)
    "barrel_mass_coeff": 0.03, # barrel mass from engine_mass (tunable)
    "shell_from_barrel_k": 0.02, "shell_from_barrel_alpha": 0.9,
    "muzzle_v_default": 1600, # m/s default high-performance APFSDS-like
    "recoil_time": 0.06,
    "turret_mass_coeff": 10.0, # turret mass multiplier on barrel mass (tunable)
    "turret_recoil_coeff": 400, # scales recoil contribution
    "ring_frac": 0.2,
    "ammo_rounds": 40,
    "propellant_frac": 0.15,
    "reinforce_frac": 0.08,
    "penetration_ref_ke": 1e6, # reference kinetic energy for normalization (arbitrary)
    "penetration_scale": 1.0
}

def build_turret_from_barrel(m_barrel, muzzle_v=None, recoil_time=None, rounds=None, coeffs=COEFF):
    if muzzle_v is None:
        muzzle_v = coeffs["muzzle_v_default"]
    if recoil_time is None:
        recoil_time = coeffs["recoil_time"]
    if rounds is None:
        rounds = coeffs["ammo_rounds"]
    # estimate shell mass
    k = coeffs["shell_from_barrel_k"]; a = coeffs["shell_from_barrel_alpha"]
    m_shell = max(0.05, k * (m_barrel ** a))  # kg, floor to avoid tiny numbers
    # recoil impulse and force
    I = m_shell * muzzle_v
    F_recoil = I / recoil_time
    # turret mass (empirical)
    m_turret = coeffs["turret_mass_coeff"] * m_barrel + coeffs["turret_recoil_coeff"] * (F_recoil/1e5)
    m_ring = coeffs["ring_frac"] * m_turret
    m_ammo_stow = rounds * (m_shell + coeffs["propellant_frac"] * m_shell)
    m_reinforce = coeffs["reinforce_frac"] * m_turret
    return {
        "barrel_mass": m_barrel,
        "shell_mass": m_shell,
        "muzzle_velocity": muzzle_v,
        "recoil_force_N": F_recoil,
        "turret_mass": m_turret,
        "ring_mass": m_ring,
        "ammo_stow_mass": m_ammo_stow,
        "reinforce_mass": m_reinforce,
        "rounds": rounds
    }

def generate_tank(length_m, name="Tank", role="general", coeffs=COEFF):
    # geometry
    width = coeffs["width_frac"] * length_m
    height = coeffs["height_frac"] * width
    volume = length_m * width * height
    # hull mass (coarse)
    hull_mass = coeffs["hull_mass_factor"] * volume * coeffs["hull_density"] / 1000.0  # in tonnes
    hull_mass_kg = hull_mass * 1000.0
    # engine sizing roughly per earlier example: engine mass scales with hull volume
    engine_mass = coeffs["engine_mass_per_volume"] * volume
    engine_power = engine_mass * coeffs["engine_power_density"]  # watts
    # stroke/piston approximations
    # piston width scaled to hull width fractionally but limited by dataset patterns
    piston_width = max(0.01, coeffs["piston_width_frac"] * width)  # m
    stroke = coeffs["stroke_frac_of_width"] * piston_width
    # RPM capped using realistic piston tip speed (v_max)
    # choose v_max by role / size
    if length_m <= 8:
        v_max = 20.0  # m/s for small/mid
    elif length_m <= 12:
        v_max = 15.0
    else:
        v_max = 12.0
    rpm_rev_per_s = v_max / (2.0 * stroke)
    rpm = rpm_rev_per_s * 60.0
    # cap to realistic engine RPM ranges
    # compute engine mass correction to ensure minimal mass
    total_mass_kg = hull_mass_kg + engine_mass
    # barrel mass estimate from engine_mass (empirical)
    barrel_mass = coeffs["barrel_mass_coeff"] * engine_mass
    turret = build_turret_from_barrel(barrel_mass, coeffs=coeffs)
    # add turret mass to total
    total_mass_kg += turret["turret_mass"] + turret["ammo_stow_mass"] + turret["reinforce_mass"]
    
    # penetration score (dimensionless)
    KE = 0.5 * turret["shell_mass"] * (turret["muzzle_velocity"]**2)
    penetration_score = coeffs["penetration_scale"] * (KE / coeffs["penetration_ref_ke"])**(1/3)
    # power in MW
    power_MW = engine_power / 1e6
    
    return {
        "name": name,
        "length_m": length_m,
        "width_m": width,
        "height_m": height,
        "hull_volume_m3": volume,
        "hull_mass_t": hull_mass,
        "engine_mass_kg": engine_mass,
        "engine_power_MW": round(power_MW, 3),
        "piston_width_m": round(piston_width,4),
        "stroke_m": round(stroke,4),
        "rpm": int(round(rpm)),
        "total_mass_t": round(total_mass_kg/1000.0, 2),
        "turret": turret,
        "penetration_score": round(penetration_score,3),
        "shell_mass_kg": round(turret["shell_mass"],3),
        "muzzle_velocity_m_s": turret["muzzle_velocity"]
    }

# Demo: generate several tanks
lengths = [6,8,10,12,15]
names = ["Scout","Striker","Panther","Titan","Colossus"]
rows = []
for L,N in zip(lengths,names):
    rows.append(generate_tank(L,N))

df = pd.DataFrame(rows)
# present dataframe to user


# Also print JSON for quick copy/paste
print(df.to_json(orient="records", indent=2))