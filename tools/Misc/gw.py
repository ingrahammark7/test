import math

def naval_energy_scaling_model(trip_km, beam_m, grain_cm):
    # Constants
    sea_energy_density = 1000  # W/m²
    water_density = 1000  # kg/m³
    hvl_thickness_m = grain_cm / 100  # grain size in meters (vertical thickness)

    # 1. Total interaction area
    trip_m = trip_km * 1000
    area_m2 = trip_m * beam_m

    # 2. Total energy intercepted (in Joules, over 1 second)
    total_energy_j = area_m2 * sea_energy_density  # since energy rate is per second

    # 3. Mass of water interacting in the HVL
    volume_m3 = area_m2 * hvl_thickness_m
    mass_kg = volume_m3 * water_density

    # 4. Grain-based base velocity (v ∝ 1/√grain_size)
    # Assume 10 m/s at 1 cm grain size
    v_base = 10 * math.sqrt(1 / grain_cm)

    # 5. Resulting energy-concentrated velocity
    # KE = 0.5 * m * v² → solve for v:
    concentrated_velocity = math.sqrt(2 * total_energy_j)/(water_density*hvl_thickness_m)
    if(concentrated_velocity>200):
    	maxen=(hvl_thickness_m*water_density*200*200*.5)
    	per_m=total_energy_j/maxen
    	print("speed capped at 200m/s")    	
    	print("over ", per_m,"m2")

    print("Trip distance:", trip_km, "km")
    print("Beam width:", beam_m, "m")
    print("Grain size:", grain_cm, "cm")
    print("Water layer (HVL):", round(hvl_thickness_m, 4), "m")
    print("Total area:", f"{area_m2:,.0f}", "m²")
    print("Interacting mass:", f"{mass_kg:,.0f}", "kg")
    print("Total intercepted energy:", f"{total_energy_j:,.0f}", "J")
    print("Base wave velocity (at grain scale):", round(v_base, 2), "m/s")
    print("Concentrated wave velocity (energy-equivalent):", round(concentrated_velocity, 2), "m/s")

# Example usage
naval_energy_scaling_model(trip_km=1000000, beam_m=10, grain_cm=1)