# Python program to compute deterministic weapon feasibility and ammo tables
# based on physics limits described in the conversation.
# This code will produce a pandas DataFrame and display it.
# It is self-contained and uses conservative default constants.
# You can modify vehicle list, calibres, or constants below to tune results.

import math
import pandas as pd

# -----------------------------
# Constants and weapon data
# -----------------------------
# Representative projectile data: (mass_kg, muzzle_velocity_m_s)
calibres = {
    "5.56_NATO": {"m": 0.004, "v": 940.0},
    "7.62_NATO": {"m": 0.0095, "v": 800.0},
    ".50_BMG": {"m": 0.045, "v": 890.0},
    "20mm": {"m": 0.125, "v": 1000.0},
    "30mm": {"m": 0.53, "v": 1000.0},
    "120mm": {"m": 10.0, "v": 1600.0},
}

# Derived per-shot momentum and kinetic energy
for name, d in calibres.items():
    d["I"] = d["m"] * d["v"]                       # momentum (kg*m/s)
    d["E"] = 0.5 * d["m"] * d["v"]**2              # kinetic energy (J)
    d["vol_est_m3"] = d["m"] / 8000.0              # crude volume estimate (kg / density 8000 kg/m3)

# -----------------------------
# Vehicle list (example real-ish and conceptual)
# -----------------------------
vehicles = [
    {"name": "toy_rc", "mass": 6.8, "f_ammo": 0.02, "v_int_m3": 0.002},
    {"name": "bike_sidecar", "mass": 420.0, "f_ammo": 0.05, "v_int_m3": 0.5},
    {"name": "ATV", "mass": 200.0, "f_ammo": 0.03, "v_int_m3": 0.2},
    {"name": "UTV_MRZR", "mass": 900.0, "f_ammo": 0.05, "v_int_m3": 0.6},
    {"name": "jeep_light", "mass": 2500.0, "f_ammo": 0.05, "v_int_m3": 2.0},
    {"name": "Wiesel", "mass": 2750.0, "f_ammo": 0.05, "v_int_m3": 2.5},
    {"name": "M1_Abrams", "mass": 70000.0, "f_ammo": 0.05, "v_int_m3": 20.0},
]

# -----------------------------
# Physics / model parameters (defaults from earlier conversation)
# -----------------------------
V_tol_map = {
    "toy_rc": 0.5,          # using a permissive small tolerance for conceptual toy
    "bike_sidecar": 0.5,
    "ATV": 0.5,
    "UTV_MRZR": 0.2,
    "jeep_light": 0.1,
    "Wiesel": 0.05,
    "M1_Abrams": 0.02,
}

v_e = 1000.0               # exhaust gas effective velocity (m/s)
v_c = 10.0                 # countermass ejection velocity (m/s)
k_P = 100.0                # allowed continuous power per kg (W/kg) for thermal budget
C_barrel = 5.0e8           # wear budget constant (J) -> gives 30mm ~2000 rounds
stowage_caps = {
    "120mm": 40,
    "30mm": 400,
    "20mm": 400,
    ".50_BMG": 2000,  # a high cap by mass but will be volume-limited in small vehicles
    "7.62_NATO": 5000,
    "5.56_NATO": 10000,
}

# container sizes (practical): approximate volumes per ammo container (m3) for ready loads
# Example: .50 100-round can volume ~0.02 m3 (very rough), 7.62 drum ~0.01 m3, etc.
container_volumes = {
    ".50_BMG": 0.02,       # per 100-round can, we'll compute by scaling
    "7.62_NATO": 0.008,    # per 200-300 round drum/box
    "5.56_NATO": 0.005,
    "20mm": 0.03,
    "30mm": 0.06,
    "120mm": 0.5,
}

# practical round-per-container for the container volumes above (for converting vol->rounds)
rounds_per_container = {
    ".50_BMG": 100,
    "7.62_NATO": 200,
    "5.56_NATO": 200,
    "20mm": 30,
    "30mm": 20,
    "120mm": 5,
}

# -----------------------------
# Helper functions implementing the physics tests
# -----------------------------
def recoil_min_vehicle_mass(I_p, V_tol):
    """Minimal vehicle mass so that single shot recoil velocity Vrec = I_p / M <= V_tol"""
    if V_tol <= 0:
        return float("inf")
    return I_p / V_tol

def r_max_recoilless(M_v, I_p, v_e_local=v_e, kP_local=k_P):
    """Max sustainable rounds/sec if canceling recoil by venting gas of velocity v_e"""
    P_safe = kP_local * M_v
    # r_max = 2 * P_safe / (I_p * v_e)
    if I_p * v_e_local == 0:
        return float("inf")
    return (2.0 * P_safe) / (I_p * v_e_local)

def countermass_per_shot(I_p, v_c_local=v_c):
    """Mass of countermass to eject per shot at speed v_c to cancel projectile momentum"""
    if v_c_local == 0:
        return float("inf")
    return I_p / v_c_local

def ammo_by_mass(M_v, f_ammo, round_mass):
    return (f_ammo * M_v) / round_mass

def ammo_by_volume(V_int, per_round_volume):
    if per_round_volume <= 0:
        return float("inf")
    return V_int / per_round_volume

def barrel_life_rounds(E_muzzle, C_local=C_barrel):
    if E_muzzle <= 0:
        return float("inf")
    return C_local / E_muzzle

# crude estimate of per-round packing volume: use density ~8000 kg/m3 for steel-like round ~ projectile volume
def per_round_volume_est(round_mass, density=8000.0):
    return round_mass / density

# -----------------------------
# Build table
# -----------------------------
rows = []
for v in vehicles:
    name = v["name"]
    M_v = v["mass"]
    f_ammo = v["f_ammo"]
    V_int = v["v_int_m3"]
    V_tol = V_tol_map.get(name, 0.1)
    for cal_name, cal in calibres.items():
        I_p = cal["I"]
        E = cal["E"]
        round_m = cal["m"]
        # recoil single-shot feasibility
        M_min = recoil_min_vehicle_mass(I_p, V_tol)
        single_shot_feasible = M_v >= M_min
        # countermass per shot (for recoilless)
        cm_per_shot = countermass_per_shot(I_p)
        # r_max if trying to vent gas continuously
        rmax = r_max_recoilless(M_v, I_p)
        # ammo capacity by mass and by volume (est)
        N_mass = math.floor(ammo_by_mass(M_v, f_ammo, round_m))
        per_round_vol = per_round_volume_est(round_m)
        N_vol = math.floor(ammo_by_volume(V_int, per_round_vol))
        # realistic stowage cap by calibre (if provided)
        stow_cap = stowage_caps.get(cal_name, None)
        if stow_cap is None:
            # default large cap
            stow_cap = 100000
        # container-based vol cap estimate (translate container vol to rounds)
        cont_vol = container_volumes.get(cal_name, None)
        cont_rounds = None
        if cont_vol:
            # how many such containers fit in V_int?
            containers_fit = math.floor(V_int / cont_vol)
            cont_rounds = containers_fit * rounds_per_container.get(cal_name, 1)
        # practical N before barrel wear / stowage
        N_barrel = math.floor(barrel_life_rounds(E))
        N_practical = min(N_mass, N_vol, N_barrel, stow_cap if stow_cap is not None else N_mass)
        # additional metadata for decision
        # classify mode: auto if rmax >= 5 rps (300 rpm) (very permissive), burst if > 0.1 rps, single if single feasible but rmax tiny
        if not single_shot_feasible:
            mode = "infeasible_single"
            # check recoilless countermass feasibility: if cm_per_shot < round mass * 0.5 accept recoilless_possible
            recoilless_possible = cm_per_shot <= 0.5 * round_m
            if recoilless_possible:
                mode = "recoilless_possible_single"
        else:
            if rmax >= 5.0:  # >= 5 rps (300 rpm) allow auto
                mode = "auto_possible"
            elif rmax >= 0.1:  # >=0.1 rps (6 rpm) allow burst-limited
                mode = "burst_limited"
            else:
                mode = "single_shot_only"
        # summary comment
        comment_parts = []
        if not single_shot_feasible:
            comment_parts.append("single-shot recoil exceeds V_tol")
        if cm_per_shot > round_m * 2.0:  # very large countermass per shot
            comment_parts.append("countermass per shot impractically large")
        if cont_rounds is not None and cont_rounds < N_practical:
            comment_parts.append("volume-limited by container packing")
        comment = "; ".join(comment_parts) if comment_parts else ""
        rows.append({
            "vehicle": name,
            "vehicle_mass_kg": M_v,
            "calibre": cal_name,
            "round_mass_kg": round_m,
            "momentum_Ip": round(I_p, 6),
            "muzzle_energy_J": int(E),
            "V_tol_m_s": V_tol,
            "M_min_for_single_kg": round(M_min, 3),
            "single_shot_feasible": single_shot_feasible,
            "countermass_per_shot_kg": round(cm_per_shot, 4),
            "r_max_rps_recoilless": round(rmax, 4),
            "N_mass_est": N_mass,
            "N_vol_est": N_vol,
            "N_barrel_est": N_barrel,
            "stowage_cap": stow_cap,
            "N_practical": N_practical,
            "practical_mode": mode,
            "comment": comment,
            "container_rounds_est": cont_rounds
        })

df = pd.DataFrame(rows)

# order & nice column names
cols = [
    "vehicle", "vehicle_mass_kg", "calibre", "round_mass_kg", "momentum_Ip", "muzzle_energy_J",
    "V_tol_m_s", "M_min_for_single_kg", "single_shot_feasible", "countermass_per_shot_kg",
    "r_max_rps_recoilless", "N_mass_est", "N_vol_est", "container_rounds_est", "stowage_cap",
    "N_barrel_est", "N_practical", "practical_mode", "comment"
]
df = df[cols]


# also print a short plaintext summary for quick glance
summary = df.groupby(["vehicle", "calibre"]).agg({
    "single_shot_feasible": "first",
    "practical_mode": "first",
    "N_practical": "first"
}).reset_index()
print("Summary (vehicle x calibre):")
print(summary.to_string(index=False))

# Save CSV for download if desired (not required)
df.to_csv("/mnt/data/weapon_feasibility_table.csv", index=False)
print("\nSaved full table to /mnt/data/weapon_feasibility_table.csv")