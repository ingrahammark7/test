import math

# Function to compute residual stress using LEFM
def residual_stress(K_IC, a, Y=1.0):
    """
    K_IC : fracture toughness in MPa*m^0.5
    a : crack length in meters
    Y : geometric factor (dimensionless)
    returns residual stress in MPa
    """
    return K_IC / (Y * math.sqrt(math.pi * a))

# Function to compute residual load ratio
def residual_load_ratio(K_IC, a, sigma_nominal, Y=1.0):
    sigma_res = residual_stress(K_IC, a, Y)
    return sigma_res / sigma_nominal

# Fixed scenario
crack_length = 30  # meters (10 cm)
sigma_nominal_steel = 300.0  # MPa
sigma_nominal_ceramic = 300.0  # MPa

# Material fracture toughness
K_IC_steel = 60.0   # MPa*m^0.5
K_IC_ceramic = 5.0  # MPa*m^0.5

# Compute residual stresses
sigma_res_steel = residual_stress(K_IC_steel, crack_length)
sigma_res_ceramic = residual_stress(K_IC_ceramic, crack_length)

# Compute residual load ratios
ratio_steel = residual_load_ratio(K_IC_steel, crack_length, sigma_nominal_steel)
ratio_ceramic = residual_load_ratio(K_IC_ceramic, crack_length, sigma_nominal_ceramic)

# Display results
print(f"Crack length: {crack_length*100:.1f} cm")
print("Residual Stress:")
print(f"  Steel: {sigma_res_steel:.2f} MPa")
print(f"  Ceramic: {sigma_res_ceramic:.2f} MPa")
print("Residual Load Ratio (σ_res / σ_nominal):")
print(f"  Steel: {ratio_steel:.20f}")
print(f"  Ceramic: {ratio_ceramic:.20f}")
print(ratio_steel/ratio_ceramic)