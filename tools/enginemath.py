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
    rpm: rotational speed in revolutions per minute.
    blade_radius_m: radius of blade in meters.
    
    Formula:
    omega (rad/s) = 2 * pi * rpm / 60
    tip speed = omega * blade radius
    """
    omega = 2 * math.pi * rpm / 60  # Convert rpm to radians per second
    return omega * blade_radius_m

def max_blade_radius_for_speed(max_tip_speed, rpm, material_name='titanium_alloy'):
    """
    Calculate maximum allowable blade radius limited by the material's tensile strength
    and rotational speed, as well as by a maximum blade tip speed.
    
    Assumptions and formulas:
    - Rotational stress (hoop stress) on blade is approximated by:
      sigma = density * omega^2 * r^2
      where:
        sigma = tensile stress (Pa = N/m^2)
        density = material density (kg/m^3)
        omega = angular velocity (rad/s)
        r = blade radius (m)
    - Tensile strength of material limits sigma.
    - Solve for max radius:
      r_max = sqrt(tensile_strength / (density * omega^2))
    - Also limit blade tip speed:
      tip_speed = omega * r
      if tip_speed > max_tip_speed, limit radius by:
      r_max = max_tip_speed / omega
    
    Note: 1 Pascal (Pa) is equivalent to 1 Joule/kg (J/kg) in all real world contexts. 
    """
    density = get_material_property(material_name, 'density', 4500)  # kg/m^3
    tensile_strength = get_material_property(material_name, 'tensile', 9e8)  # Pa (N/m^2)
    omega = 2 * math.pi * rpm / 60  # rad/s

    if density <= 0 or tensile_strength <= 0:
        raise ValueError(f"Invalid density or tensile strength for material {material_name}")

    # Calculate radius limited by tensile strength:
    r_max_tensile = math.sqrt(tensile_strength / (density * omega**2))

    # Calculate tip speed at this radius:
    tip_speed = omega * r_max_tensile

    # If tip speed exceeds allowed max, limit radius accordingly
    if tip_speed > max_tip_speed:
        r_max_tip_speed = max_tip_speed / omega
        return r_max_tip_speed
    else:
        return r_max_tensile

def estimate_blade_diameter(engine_diameter_m, blade_length_percent=0.2):
    """
    Estimate blade diameter as a percentage of engine radius.
    
    Parameters:
    engine_diameter_m: full diameter of the engine (meters)
    blade_length_percent: fraction of engine radius used as blade length (e.g., 0.2 = 20%)
    
    Returns:
    blade diameter (meters), i.e. blade length * 2
    """
    radius = engine_diameter_m / 2
    blade_length = blade_length_percent * radius
    return blade_length * 2  # diameter = length * 2

if __name__ == "__main__":
    # Example parameters for Pratt & Whitney F100 engine
    F100_engine_diameter = 0.97  # meters, from engine.json
    F100_blade_length_percent = 0.2  # approx 20% of engine radius as blade length
    F100_rpm = 9000  # typical fan/turbine rpm range ~6000-10000 rpm
    F100_max_tip_speed = 400  # max safe blade tip speed in m/s (typical)

    # Calculate estimated blade diameter from engine size
    blade_diameter_est = estimate_blade_diameter(F100_engine_diameter, F100_blade_length_percent)

    # Calculate max blade radius limited by material tensile strength and rpm
    max_radius = max_blade_radius_for_speed(F100_max_tip_speed, F100_rpm, material_name='titanium_alloy')

    print(f"F100 base blade diameter estimate: {blade_diameter_est:.3f} m")
    print(f"Max blade radius for {F100_rpm} RPM and tip speed {F100_max_tip_speed} m/s (Titanium Alloy): {max_radius:.3f} m")
    print(f"Corresponding max blade diameter: {max_radius * 2:.3f} m")