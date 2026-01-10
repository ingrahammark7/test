import math

# Diffusion coefficient (m^2/s)
D = 0.05  

# Detector threshold (µg/m³)
threshold = 0.01  

# Simulation parameters
total_time = 300  # max simulation time in seconds
dt = 1            # time step in seconds
epsilon = 1e-3    # relative change threshold for max concentration

# Define continuous emission cases with distances
cases = [
    {"name": "Low emission", "Q": 0.1, "distance": 1},
    {"name": "Medium emission", "Q": 1, "distance": 2},
    {"name": "High emission", "Q": 5, "distance": 5},
]

def concentration_continuous(Q, r, D, t, dt):
    """Compute concentration at distance r and time t for continuous emission."""
    C = 0
    # Sum contributions from each past pulse
    for t_pulse in range(1, int(t)+1):
        C += (Q*dt) / ((4*math.pi*D*(t - t_pulse + 1))**(3/2)) * math.exp(-r**2 / (4*D*(t - t_pulse + 1)))
    return C

# Run simulation
print("\nSummary of Hormone Detection Simulation\n")
print("Name\tDistance(m)\tEmission(µg/s)\tFirst Detection(s)\tMax Concentration(µg/m³)\tTime to Max(s)")

for case in cases:
    first_detectable = None
    prev_C = 0
    max_C = 0
    time_to_max = total_time
    
    for t in range(1, total_time+1, dt):
        C = concentration_continuous(case["Q"], case["distance"], D, t, dt)
        
        # Check first detection
        if first_detectable is None and C >= threshold:
            first_detectable = t
        
        # Check relative change for max concentration
        if prev_C > 0 and abs(C - prev_C)/prev_C < epsilon:
            max_C = C
            time_to_max = t
            break
        
        prev_C = C
    
    # If max not detected, use last concentration
    if max_C == 0:
        max_C = C
        time_to_max = t
    
    first_detectable_str = str(first_detectable) if first_detectable else "Never"
    
    print(f"{case['name']}\t{case['distance']}\t\t{case['Q']}\t\t{first_detectable_str}\t\t\t{max_C:.5f}\t\t\t{time_to_max}")