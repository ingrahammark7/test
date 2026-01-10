import math

def max_detection_distance(Q, D, C_th):
    """
    Returns the maximum distance (m) a continuous hormone emission can be detected.
    
    Q: emission rate (µg/s)
    D: diffusion coefficient (m²/s)
    C_th: detector threshold (µg/m³)
    """
    return Q / (4 * math.pi * D * C_th)

# Example values
D = 0.05       # m²/s
C_th = 0.01    # µg/m³
cases = [
    {"name": "Low emission", "Q": 0.1},
    {"name": "Medium emission", "Q": 1},
    {"name": "High emission", "Q": 5},
]

print("Name\tMax Detection Distance (m)")
for case in cases:
    r_max = max_detection_distance(case["Q"], D, C_th)
    print(f"{case['name']}\t{r_max:.2f}")