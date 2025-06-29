import json

# Load materials and fighters data
with open('mat.json', 'r') as f:
    materials = json.load(f)

with open('fightermodels.json', 'r') as f:
    fighters = json.load(f)


def get_material_property(name, prop):
    for mat in materials:
        if mat.get("name", "").lower() == name.lower():
            return mat.get(prop)
    return None


def estimate_aircraft_mass_simple(fighter_data, thickness_scale=1.0):
    L = fighter_data.get("length_cm", 0)
    W = fighter_data.get("frontal_width_cm", 0)
    H = fighter_data.get("frontal_height_cm", 0)
    skin_thickness = fighter_data.get("skin_thickness_cm", 0.1) * thickness_scale
    center_thickness = fighter_data.get("center_plate_thickness_cm", 0.0)

    density_aluminum = get_material_property("Aluminum", "density") or 2700
    density_titanium = get_material_property("Titanium", "density") or 4500

    # Wetted area approximation (cm^2)
    wetted_area = 2 * L * (W + H)

    skin_volume = wetted_area * skin_thickness       # in cm^3
    center_volume = W * H * center_thickness if center_thickness > 0 else 0  # in cm^3

    # Convert cm^3 to m^3 by dividing by 1,000,000 for mass in kg
    mass_aluminum = skin_volume * density_aluminum / 1_000_000
    mass_titanium = center_volume * density_titanium / 1_000_000

    print(f"Aircraft dimensions (LxWxH): {L} x {W} x {H} cm")
    print(f"Scaled skin thickness: {skin_thickness} cm (scale factor {thickness_scale})")
    print(f"Wetted area: {wetted_area:.2f} cm^2")
    print(f"Skin volume: {skin_volume:.2f} cm^3, Center plate volume: {center_volume:.2f} cm^3")
    print(f"Density Aluminum: {density_aluminum} kg/m^3, Density Titanium: {density_titanium} kg/m^3")
    print(f"Mass Aluminum: {mass_aluminum:.2f} kg, Mass Titanium: {mass_titanium:.2f} kg\n")

    return mass_aluminum + mass_titanium


if __name__ == "__main__":
    # Use thickness_scale < 1 to better approximate real skin thickness
    thickness_scale = 0.1  # Example: 10% of given skin thickness (e.g. 0.1 cm * 0.1 = 0.01 cm)

    for name, data in fighters.items():
        print(f"Estimating mass for {name}:")
        mass = estimate_aircraft_mass_simple(data, thickness_scale=thickness_scale)
        print(f"Estimated total mass: {mass:.2f} kg")
        print('-' * 40)