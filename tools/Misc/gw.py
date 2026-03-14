import json
import math

# --- Constants ---
g = 9.80665  # m/s^2
rho_20kft = 0.652  # kg/m^3 at 20,000 ft
gamma = 1.4
R = 287.05
T_20kft = 216.65
mach = 0.7
fuel_energy_density = 43e6  # J/kg

# --- Load aircraft JSON ---
with open("rockets.json") as f:
    data = json.load(f)

# --- Speed of sound and cruise velocity ---
a = math.sqrt(gamma * R * T_20kft)
v = mach * a

results = []

for ac in data["aircraft"]:
    # Frontal area
    frontal_area = math.pi * (ac["fuselage_diameter"] / 2)**2
    
    # Air volume & mass per sec
    volume_flow = frontal_area * v
    mass_flow = volume_flow * rho_20kft
    
    # Kinetic power of air
    power_air = 0.5 * mass_flow * v**2
    
    # Fuel power required
    fuel_power = power_air / ac["efficiency"]
    
    # Max fuel energy
    max_fuel_energy = ac["max_fuel"] * fuel_energy_density
    
    # Ferry flight time in seconds and hours
    flight_time_sec = max_fuel_energy / fuel_power
    flight_time_hr = flight_time_sec / 3600
    
    # Average mass
    avg_mass = ((ac["empty_weight"] + ac["max_fuel"]) + ac["empty_weight"]) / 2
    
    # Gravitational work over time
    gravity_work = avg_mass * g * flight_time_sec
    
    # Ratio fuel energy / gravity work
    ratio = max_fuel_energy / gravity_work
    
    # Ferry range
    distance_km = v * flight_time_sec / 1000
    
    results.append({
        "name": ac["name"],
        "frontal_area_m2": round(frontal_area, 1),
        "volume_flow_m3_s": round(volume_flow, 1),
        "mass_flow_kg_s": round(mass_flow, 1),
        "power_air_W": round(power_air, 0),
        "fuel_power_W": round(fuel_power, 0),
        "flight_time_hr": round(flight_time_hr, 2),
        "avg_mass_kg": round(avg_mass, 1),
        "gravity_work_J": round(gravity_work, 0),
        "fuel_to_gravity_ratio": round(ratio, 2),
        "ferry_range_km": round(distance_km, 0)
    })

# --- Output results ---
print(json.dumps(results, indent=2))