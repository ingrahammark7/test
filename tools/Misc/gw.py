import numpy as np

# Updated parameters
power_line_length_km = 250_000
corridor_width_m = 10
corridor_width_km = corridor_width_m / 1000

bird_density_per_km2 = 20
bird_flight_speed_km_per_day = 50

prob_landing_per_encounter = 0.05
prob_short_per_landing = 0.001
prob_fire_per_short = 0.05
fire_risk_days_fraction = 60 / 365
vegetation_density_factor = 0.7
days_per_year = 365
simulation_years = 10

corridor_area_km2 = power_line_length_km * corridor_width_km
birds_in_corridor = bird_density_per_km2 * corridor_area_km2

def simulate_bird_landings():
    fires_per_year = []
    
    for year in range(simulation_years):
        total_bird_km_traveled = birds_in_corridor * bird_flight_speed_km_per_day
        
        encounters = total_bird_km_traveled * corridor_width_km
        
        landings = np.random.binomial(n=int(encounters), p=prob_landing_per_encounter)
        
        shorts = np.random.binomial(n=landings, p=prob_short_per_landing)
        
        shorts_during_risk = np.random.binomial(n=shorts, p=fire_risk_days_fraction)
        
        expected_fires = shorts_during_risk * prob_fire_per_short * vegetation_density_factor
        
        fires_per_year.append(expected_fires)
        
        print(f"Year {year+1}: Encounters={int(encounters)}, Landings={landings}, Shorts={shorts}, Fire-risk shorts={shorts_during_risk}, Estimated fires={expected_fires:.2f}")
    
    avg_fires = np.mean(fires_per_year)
    print(f"\nAverage estimated fires per year: {avg_fires:.2f}")

simulate_bird_landings()