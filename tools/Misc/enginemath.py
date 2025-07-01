import json
import math

# Load materials from mat.json into a dictionary keyed by lowercase material name
with open('mat.json') as f:
    materials_list = json.load(f)
materials = {m['name'].lower(): m for m in materials_list}

def get_material_property(material_name, property_name, default=None):
    """
    Retrieve a material property from mat.json data.
    material_name: string, case-insensitive.
    property_name: string key of the property to retrieve.
    default: value to return if material or property not found.
    """
    mat = materials.get(material_name.lower())
    if mat:
        return mat.get(property_name, default)
    return default

def blade_tip_speed(rpm, blade_radius_m):
    """
    Calculate blade tip speed in meters per second.
    rpm: revolutions per minute.
    blade_radius_m: blade radius in meters.
    Returns tip speed in m/s.
    """
    omega = 2 * math.pi * rpm / 60  # rad/s
    return omega * blade_radius_m

def max_blade_radius_for_blade_speed(blade_speed_mps, rpm):
    """
    Given a desired blade tip speed (m/s) and RPM, calculate the corresponding blade radius (m).
    This is used instead of tensile limit.
    """
    omega = 2 * math.pi * rpm / 60
    return blade_speed_mps / omega

def blade_mass(blade_radius, chord_thickness, height, density):
    """
    Compute mass of a rectangular blade treated as a thin plate.
    - blade_radius: front-to-back length (m)
    - chord_thickness: thickness of blade (m)
    - height: radial blade length (m)
    - density: material density (kg/m^3)
    """
    volume = blade_radius * chord_thickness * height  # m^3
    return volume * density  # kg

def air_impact_power_per_blade(blade_speed, area, air_density=1.225):
    """
    Estimate air kinetic power impacting the blade per second:
    Power = 0.5 * rho * A * v^3
    """
    return 0.5 * air_density * area * blade_speed ** 3

def estimate_blade_lifetime_seconds(blade_mass_kg, tensile_j_per_kg, impact_power_watts):
    """
    How long until the blade reaches failure energy:
    time = (tensile_energy_per_mass * mass) / power
    """
    if impact_power_watts <= 0:
        return float('inf')
    return (tensile_j_per_kg * blade_mass_kg) / impact_power_watts

def example_f100_blade_lifetime():
    material = 'titanium_alloy'
    density = get_material_property(material, 'density', 4500)
    tensile_j_per_kg = get_material_property(material, 'tensile', 9e8)  # Pa interpreted as J/kg

    blade_speed = 400  # m/s (fixed)
    rpm = 9000  # rotational speed
    blade_radius = max_blade_radius_for_blade_speed(blade_speed, rpm)  # ~max allowable length

    chord_thickness = 0.025  # 25 mm assumed front-to-back thickness
    height = 0.30  # 30 cm blade height (radial)

    area = chord_thickness * height  # impact face area (m^2)
    mass = blade_mass(blade_radius, chord_thickness, height, density)
    impact_power = air_impact_power_per_blade(blade_speed, area)

    lifetime_sec = estimate_blade_lifetime_seconds(mass, tensile_j_per_kg, impact_power)

    print(f"Material: {material}")
    print(f"Blade Speed: {blade_speed:.1f} m/s")
    print(f"Blade Radius (max from speed): {blade_radius:.3f} m")
    print(f"Blade Dimensions: {blade_radius:.3f} m x {chord_thickness:.3f} m x {height:.3f} m")
    print(f"Blade Mass: {mass:.2f} kg")
    print(f"Impact Power: {impact_power:.1f} W")
    print(f"Tensile Strength: {tensile_j_per_kg:.1e} J/kg")
    print(f"Estimated Lifetime: {lifetime_sec:.1f} seconds")

if __name__ == "__main__":
    example_f100_blade_lifetime()