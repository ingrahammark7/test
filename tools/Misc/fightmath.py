import json
import math
import re

# Load data
with open("mat.json") as f:
    materials = json.load(f)
with open("fightermodels.json") as f:
    fighter_models = json.load(f)
with open("fighters.json") as f:
    fighters_info = json.load(f)

# Get material properties
def get_mat(name, prop):
    mat = next((m for m in materials if m["name"].lower() == name.lower()), None)
    return mat.get(prop) if mat else None

# Material constants
rho_steel = get_mat("Steel", "density")
T_melt_steel = get_mat("Steel", "melting_point") + 273.15
cp_steel = get_mat("Steel", "specific_heat")
sigma_steel = get_mat("Steel", "tensile")
rho_air = 1.225
T_air = 300
h = 100  # W/m^2K

rho_al = get_mat("Aluminum", "density") or 2700
rho_ti = get_mat("Titanium", "density") or 4500

# Regex to extract caliber
caliber_re = re.compile(r"(\d+(\.\d+)?)\s*mm")

def extract_caliber(gun_name):
    m = caliber_re.search(gun_name or "")
    return (float(m.group(1)) / 1000) if m else None

# Gun physics

def v_eq():
    return ((2 * h * (T_melt_steel - T_air)) / rho_air) ** (1/3)

def time_to_half(caliber):
    d = caliber
    L = 10 * d
    mass = math.pi * (d/2)**2 * L * rho_steel
    surface = math.pi * d * L
    T_target = (T_melt_steel + T_air) / 2
    Q = mass * cp_steel * (T_target - T_air)
    Qdot = h * surface * (T_melt_steel - T_air)
    return Q / Qdot

def v_firing_limit():
    return math.sqrt(2 * sigma_steel / rho_steel)

results = {}
for name, model in fighter_models.items():
    gun = fighters_info.get(name, {}).get("gun")
    calib = extract_caliber(gun)

    length = model.get("length_cm", 0)
    width = model.get("frontal_width_cm", 0)
    height = model.get("frontal_height_cm", 0)
    skin_thickness = model.get("skin_thickness_cm", 0)
    center_plate = model.get("center_plate_thickness_cm", 0)

    area = width * height
    skin_volume = area * skin_thickness
    center_volume = (width * height) * center_plate

    mass_al = (skin_volume / 1e6) * rho_al
    mass_ti = (center_volume / 1e6) * rho_ti

    # Internal structure mass estimation (not shown but preserved in structure)

    if calib:
        d = calib
        L = 10 * d
        proj_vol = math.pi * (d/2)**2 * L
        proj_mass = proj_vol * rho_steel
        teq = time_to_half(calib)
        vthermal = v_eq()
        vfail = v_firing_limit()
    else:
        proj_mass = teq = vthermal = vfail = None

    results[name] = {
        "gun": gun,
        "skin_mass_kg": mass_al,
        "center_plate_mass_kg": mass_ti,
        "projectile_mass_kg": proj_mass,
        "steady_state_v_eq_m_s": vthermal,
        "time_to_50pc_melt_s": teq,
        "firing_speed_limit_m_s": vfail
    }

print(json.dumps(results, indent=2))


