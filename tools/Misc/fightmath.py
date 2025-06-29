import json

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def estimate_mass(fighter, density_map):
    length_m = fighter["length_cm"] / 100
    width_m = fighter["frontal_width_cm"] / 100
    height_m = fighter["frontal_height_cm"] / 100
    skin_thickness_m = fighter.get("skin_thickness_cm", 0.1) / 100
    center_plate_thickness_m = fighter.get("center_plate_thickness_cm", 0) / 100

    # Wetted area = 2 * (length * height) + 2 * (length * width)
    skin_area = 2 * (length_m * height_m) + 2 * (length_m * width_m)

    skin_volume = skin_area * skin_thickness_m
    center_plate_volume = width_m * height_m * center_plate_thickness_m

    mass_skin = skin_volume * density_map.get("aluminum", 2700)
    mass_center = center_plate_volume * density_map.get("titanium", 4500)

    return mass_skin + mass_center

def main():
    fightermodels = load_json("fightermodels.json")
    materials = load_json("mat.json")

    # Create a dict mapping lowercase material names to densities
    density_map = {mat["name"].lower(): mat.get("density", 0) for mat in materials}

    for name, fighter in fightermodels.items():
        total_mass = estimate_mass(fighter, density_map)
        print(f"{name} estimated mass: {total_mass:.2f} kg")

if __name__ == "__main__":
    main()