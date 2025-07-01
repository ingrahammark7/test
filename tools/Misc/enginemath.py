import json
import math

# Load materials from mat.json into a dictionary keyed by lowercase material name
with open('mat.json') as f:
    materials_list = json.load(f)
materials = {m['name'].lower(): m for m in materials_list}

def get_material_property(material_name, property_name, default=None):
    mat = materials.get(material_name.lower())
    if mat:
        return mat.get(property_name, default)
    return default

def blade_tip_speed(rpm, blade_radius_m):
    omega = 2 * math.pi * rpm / 60  # rad/s
    return omega * blade_radius_m

def max_blade_radius_for_blade_speed(blade_speed_mps, rpm):
    omega = 2 * math.pi * rpm / 60
    return blade_speed_mps / omega

def blade_mass(blade_radius, chord_thickness, height, density):
    volume = blade_radius * chord_thickness * height  # m^3
    return volume * density  # kg

def air_impact_power_per_blade(blade_speed, area, air_density=1.225):
    return 0.5 * air_density * area * blade_speed ** 3

def estimate_blade_lifetime_seconds(blade_mass_kg, tensile_j_per_kg, impact_power_watts):
    if impact_power_watts <= 0:
        return float('inf')
    return (tensile_j_per_kg * blade_mass_kg) / impact_power_watts

class EngineThermalAnalysis:
    def __init__(self, material_name, rpm=9000, blade_speed_mps=400):
        self.material_name = material_name
        self.rpm = rpm
        self.blade_speed_mps = blade_speed_mps
        self.mat = materials.get(material_name.lower(), {})
        self.density = self.mat.get("density", 4500)
        self.specific_heat = self.mat.get("specific_heat", 520)
        self.melting_point_C = self.mat.get("melting_point", 1600)
        self.hvl_m = self.mat.get("hvl", {}).get("0.5MeV", 1.5) / 100.0  # convert cm to m

    def max_pressure_rise(self, inlet_temp_k, wall_area_m2=1.0):
        gamma = 1.4
        R = 287
        v = self.blade_speed_mps
        rho = 101325 / (R * inlet_temp_k)
        delta_P = 0.5 * rho * v ** 2

        inlet_C = inlet_temp_k - 273.15
        delta_T = max(self.melting_point_C - inlet_C, 50)

        wall_volume = wall_area_m2 * self.hvl_m
        wall_mass = wall_volume * self.density
        wall_heat_capacity = 0.5 * wall_mass * self.specific_heat

        power_input = delta_P * v * wall_area_m2
        time_to_melt = wall_heat_capacity * delta_T / power_input if power_input > 0 else float('inf')

        return delta_P, time_to_melt

    def run_example(self):
        inlet_temp_k = 900
        area = 1.0
        dP, t = self.max_pressure_rise(inlet_temp_k, wall_area_m2=area)
        print(f"Material: {self.material_name}")
        print(f"Inlet Temp: {inlet_temp_k} K")
        print(f"Blade Speed: {self.blade_speed_mps} m/s")
        print(f"ΔP Max: {dP:.1f} Pa")
        print(f"Wall Area: {area} m^2")
        print(f"Wall Thickness (HVL): {self.hvl_m:.4f} m")
        print(f"Thermal Margin: {max(self.melting_point_C - (inlet_temp_k - 273.15), 50):.1f} °C")
        print(f"Time to Melt (Half Capacity): {t:.1f} s")

def example_f100_blade_lifetime():
    material = 'titanium_alloy'
    density = get_material_property(material, 'density', 4500)
    tensile_j_per_kg = get_material_property(material, 'tensile', 9e8)

    blade_speed = 400
    rpm = 9000
    blade_radius = max_blade_radius_for_blade_speed(blade_speed, rpm)

    chord_thickness = 0.025
    height = 0.30

    area = chord_thickness * height
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
    print("\n--- Thermal Pressure Analysis ---")
    analysis = EngineThermalAnalysis("titanium_alloy")
    analysis.run_example()


