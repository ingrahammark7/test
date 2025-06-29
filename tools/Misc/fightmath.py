

import json
import math

# Load materials data from mat.json
with open('mat.json') as f:
    materials_list = json.load(f)
materials = {m['name'].lower(): m for m in materials_list}

# Load fighter models data from fightermodels.json
with open('fightermodels.json') as f:
    fighter_models = json.load(f)

# Load fighters data from fighters.json
with open('fighters.json') as f:
    fighters = json.load(f)

STEEL_NAME = 'steel'
AL_NAME = 'aluminum'
TI_NAME = 'titanium'

# Constants
AIR_DENSITY = 1.225  # kg/m3 (sea level)
HEAT_TRANSFER_COEFF = 50  # W/(m2·K) typical forced convection steel-air approx

def estimate_aircraft_mass(name, scale=1.0):
    fm = fighter_models.get(name)
    if not fm:
        print(f"No fighter model for {name}")
        return 0.0

    length = fm.get("length_cm", 0) * scale
    width = fm.get("frontal_width_cm", 0) * scale
    height = fm.get("frontal_height_cm", 0) * scale
    skin_thickness = fm.get("skin_thickness_cm", 0.01) * scale
    center_plate_thickness = fm.get("center_plate_thickness_cm", 0) * scale

    # Wetted area approx: sum of side rectangles (no wings detailed)
    wetted_area = 2 * (length * height + length * width + width * height)  # cm2

    # Volumes in cm3
    skin_volume = wetted_area * skin_thickness
    center_plate_volume = length * width * center_plate_thickness

    density_al = materials.get(AL_NAME, {}).get("density", 2700)  # kg/m3
    density_ti = materials.get(TI_NAME, {}).get("density", 4500)

    # Convert volumes cm3 to m3
    skin_volume_m3 = skin_volume / 1e6
    center_plate_volume_m3 = center_plate_volume / 1e6

    mass_al = skin_volume_m3 * density_al
    mass_ti = center_plate_volume_m3 * density_ti

    total_mass = mass_al + mass_ti

    print(f"Estimating mass for {name}:")
    print(f"Aircraft dimensions (LxWxH): {length} x {width} x {height} cm")
    print(f"Skin thickness: {skin_thickness:.4f} cm, Center plate thickness: {center_plate_thickness:.4f} cm")
    print(f"Wetted area: {wetted_area:.2f} cm^2")
    print(f"Skin volume: {skin_volume:.2f} cm^3, Center plate volume: {center_plate_volume:.2f} cm^3")
    print(f"Density Aluminum: {density_al} kg/m^3, Density Titanium: {density_ti} kg/m^3")
    print(f"Mass Aluminum: {mass_al:.2f} kg, Mass Titanium: {mass_ti:.2f} kg")
    print(f"Estimated total mass: {total_mass:.2f} kg")
    print("----------------------------------------")

    return total_mass

def parse_gun_caliber(gun_name):
    # Extract caliber in mm or cm from gun name by splitting and searching for a number + unit
    parts = gun_name.replace(',', '').split()
    for p in parts:
        if p.lower().endswith("mm"):
            try:
                return float(p[:-2])
            except:
                continue
        else:
            try:
                val = float(p)
                if 5 <= val <= 50:  # plausible caliber mm
                    return val
            except:
                pass
    return None

def calculate_round_mass(caliber_mm, length_over_d=10):
    radius_m = (caliber_mm / 1000) / 2
    length_m = radius_m * 2 * length_over_d
    volume_m3 = math.pi * radius_m ** 2 * length_m
    density_steel = materials.get(STEEL_NAME, {}).get("density", 7850)
    mass = volume_m3 * density_steel
    return mass

def calculate_equilibrium_velocity(round_mass, caliber_mm, max_temp=1510):
    area_m2 = math.pi * (caliber_mm / 1000 / 2) ** 2
    h = HEAT_TRANSFER_COEFF
    rho_air = AIR_DENSITY
    T_air = 300  # K approx
    T_max = max_temp + 273.15  # K
    Cd = 1.0
    v_eq = ((2 * h * (T_max - T_air)) / (rho_air * Cd)) ** (1 / 3)
    return v_eq

def time_to_half_equilibrium(round_mass, caliber_mm, max_temp=1510):
    cp = materials.get(STEEL_NAME, {}).get("specific_heat", 500)
    density = materials.get(STEEL_NAME, {}).get("density", 7850)
    surface_area = 2 * math.pi * (caliber_mm / 1000 / 2) * (caliber_mm / 1000 * 10)
    h = HEAT_TRANSFER_COEFF
    m = round_mass
    tau = m * cp / (h * surface_area)
    t_half = tau * math.log(2)
    return t_half

def calculate_rha_penetration_finite_block(round_mass, velocity, tensile_j_per_kg, hvl_cm, target_density, target_thickness_cm):
    # Kinetic Energy
    KE = 0.5 * round_mass * velocity ** 2  # Joules

    # Calculate volume of impacted cylinder:
    # Diameter = HVL (steel), Thickness = target thickness (cm)
    hvl_m = hvl_cm / 100  # cm to m
    thickness_m = target_thickness_cm / 100
    volume_m3 = math.pi * (hvl_m / 2) ** 2 * thickness_m

    # Mass of target impacted volume
    mass_target = volume_m3 * target_density  # kg
    print(tensile_j_per_kg)
    print(mass_target)

    # Energy required to fail impacted volume:
    # tensile_j_per_kg = J/kg energy to fail
    energy_required = tensile_j_per_kg * mass_target  # Joules
    print("em ",energy_required)

    # Calculate penetration ratio (energy ratio)
    penetration_ratio = KE / energy_required if energy_required > 0 else 0.0

    # Penetration in cm = penetration_ratio * thickness
    penetration_cm = penetration_ratio * target_thickness_cm

    # Remaining KE after penetration
    KE_remaining = max(0, KE - energy_required)

    return penetration_cm, energy_required, KE_remaining, mass_target

def main():
    # Constants for materials
    tensile_steel = materials.get(STEEL_NAME, {}).get("tensile", 400e6)  # Pa (N/m2)
    density_steel = materials.get(STEEL_NAME, {}).get("density", 7850)  # kg/m3

    tensile_al = materials.get(AL_NAME, {}).get("tensile", 310e6)
    density_al = materials.get(AL_NAME, {}).get("density", 2700)

    tensile_ti = materials.get(TI_NAME, {}).get("tensile", 900e6)
    density_ti = materials.get(TI_NAME, {}).get("density", 4500)

    # Convert tensile strength Pa to J/kg = tensile / density
    tensile_j_per_kg_steel = tensile_steel 
    tensile_j_per_kg_al = tensile_al 
    tensile_j_per_kg_ti = tensile_ti 

    hvl_steel = materials.get(STEEL_NAME, {}).get("hvl", {}).get("0.5MeV", 1.8)  # cm

    for attacker in fighter_models.keys():
        # Mass estimate (not used in pen calc but useful)
        estimate_aircraft_mass(attacker)

        gun = fighters.get(attacker, {}).get('gun')
        if not gun:
            print(f"No gun info for {attacker}")
            continue

        caliber_mm = parse_gun_caliber(gun)
        if caliber_mm is None:
            print(f"Could not parse caliber from gun '{gun}' for {attacker}")
            continue

        round_mass = calculate_round_mass(caliber_mm)

        # Thermal equilibrium velocity and time (just for info)
        eq_velocity = calculate_equilibrium_velocity(round_mass, caliber_mm)
        t_half = time_to_half_equilibrium(round_mass, caliber_mm)

        # Firing speed limit based on steel tensile strength (simplified)
        firing_speed_limit = math.sqrt(2 * tensile_j_per_kg_steel)

        # SU-35 target parameters
        su35 = fighter_models.get("Su-35")
        if not su35:
            print("Su-35 model missing")
            break

        skin_thickness_cm = su35.get("skin_thickness_cm", 0.1)
        center_plate_thickness_cm = su35.get("center_plate_thickness_cm", 0.0)

        # Penetrate Su-35 skin (Aluminum)
        pen_skin_cm, energy_req_skin, KE_after_skin, mass_skin = calculate_rha_penetration_finite_block(
            round_mass, firing_speed_limit, tensile_j_per_kg_al, hvl_steel, density_al, skin_thickness_cm)

        # Penetrate Su-35 center plate (Titanium) if any KE left and plate exists
        pen_center_cm = 0.0
        energy_req_center = 0.0
        KE_after_center = KE_after_skin
        mass_center = 0.0
        if center_plate_thickness_cm > 0 and KE_after_skin > 0:
            # velocity after skin penetration
            v_after_skin = math.sqrt(2 * KE_after_skin / round_mass)
            pen_center_cm, energy_req_center, KE_after_center, mass_center = calculate_rha_penetration_finite_block(
                round_mass, v_after_skin, tensile_j_per_kg_ti, hvl_steel, density_ti, center_plate_thickness_cm)

        print(f"Attacker: {attacker}")
        print(f"Gun: {gun}, Caliber: {caliber_mm} mm")
        print(f"Round mass: {round_mass:.4f} kg")
        print(f"Thermal equilibrium velocity (m/s): {eq_velocity:.2f}")
        print(f"Time to half equilibrium (s): {t_half:.2f}")
        print(f"Firing speed limit (m/s): {firing_speed_limit:.2f}")
        print(f"Su-35 skin penetration (cm): {pen_skin_cm:.4f}")
        print(f"Energy required to penetrate skin (J): {energy_req_skin:.2f}")
        print(f"Remaining KE after skin (J): {KE_after_skin:.2f}")
        if center_plate_thickness_cm > 0:
            print(f"Su-35 center plate penetration (cm): {pen_center_cm:.4f}")
            print(f"Energy required to penetrate center plate (J): {energy_req_center:.2f}")
            print(f"Remaining KE after center plate (J): {KE_after_center:.2f}")
        print("========================================")

if __name__ == "__main__":
    main()


