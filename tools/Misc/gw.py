import numpy as np

# Hose properties
hose_melting_C = 180
hose_emissivity = 0.95

# Environmental parameters (realistic for lab)
T_ambient_K = 298         # 25°C
T_hot_gas_K = 323         # 50°C, hot gas near hose
h_conv = 50                # W/m²K, convective coefficient
Q_rad_base = 5             # W/m², small radiation contribution

# Distances from flame (m)
distances = np.linspace(0.01, 0.2, 10)  # 1 cm to 20 cm

print("Distance (cm) | Hose Temp (°C) | Safe?")
print("-----------------------------------------")
for d in distances:
    # Radiative flux decays slightly with distance (rough estimate)
    Q_rad = Q_rad_base * (0.05 / d)  # reference distance 5 cm
    # Convective flux
    Q_conv = h_conv * (T_hot_gas_K - T_ambient_K)
    
    # Total heat flux
    Q_total = Q_rad + Q_conv
    
    # Hose temperature
    sigma = 5.67e-8
    T_hose_K = (Q_total / (hose_emissivity * sigma))**0.25
    T_hose_C = T_hose_K - 273.15
    
    safe = "Yes" if T_hose_C < hose_melting_C else "No"
    
    print(f"{d*100:10.1f} | {T_hose_C:13.1f} | {safe}")