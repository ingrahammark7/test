import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Constants
v_escape = 11200  # m/s, Earth surface escape velocity
N_people = 8e9    # total humanity
N_half = N_people / 2
NPP_annual = 4e20 # Joules/year, global NPP

# Launcher definitions: mass, delta-v achievable
launchers = {
    'Redstone': {'mass_payload': 75, 'delta_v': 7500},
    'Atlas': {'mass_payload': 100, 'delta_v': 9300},
    'Soyuz': {'mass_payload': 200, 'delta_v': 9500},
    'Ideal_laser': {'mass_payload': 100, 'delta_v': 11200}
}

# Payload scenarios (mass in kg)
payloads = {
    'Minimal': 75,
    'Lean_capsule': 100,
    'Balloon_sail': 170,
    'Crew_capsule': 370,
    'Full_system': 870
}

# Gravity reductions (fractional reduction)
gravity_reduction = np.linspace(0, 0.6, 50)  # 0% to 60% reduction

# Multivariate analysis
rows = []
for launcher_name, launcher in launchers.items():
    for payload_name, payload_mass in payloads.items():
        for g_red in gravity_reduction:
            v_escape_eff = v_escape * np.sqrt(1 - g_red)
            success = launcher['delta_v'] >= v_escape_eff
            E_per_person = 0.5 * payload_mass * v_escape_eff**2
            E_total = E_per_person * N_half
            frac_NPP = E_total / NPP_annual
            rows.append({
                'launcher': launcher_name,
                'payload_scenario': payload_name,
                'gravity_reduction': g_red,
                'v_escape_eff': v_escape_eff,
                'delta_v_launcher': launcher['delta_v'],
                'success': success,
                'E_per_person_J': E_per_person,
                'E_total_J': E_total,
                'frac_NPP': frac_NPP
            })

# Convert to DataFrame
df = pd.DataFrame(rows)

# Pivot table for heatmap (gravity reduction vs payload) per launcher
for launcher_name in launchers.keys():
    pivot = df[df['launcher']==launcher_name].pivot_table(
        index='payload_scenario',
        columns='gravity_reduction',
        values='success',
        aggfunc='max'
    )
    plt.figure(figsize=(12,6))
    plt.imshow(pivot, origin='lower', aspect='auto', cmap='Greens')
    plt.colorbar(label='Launch Success (1=True, 0=False)')
    plt.xticks(ticks=np.arange(0,len(gravity_reduction),5),
               labels=np.round(gravity_reduction[::5]*100,1))
    plt.yticks(ticks=np.arange(len(payloads)),
               labels=list(payloads.keys()))
    plt.title(f'Mass Ejection Feasibility vs Gravity Reduction - {launcher_name}')
    plt.xlabel('Gravity Reduction (%)')
    plt.ylabel('Payload Scenario')
    plt.show()

# Export full DataFrame for detailed multivariate analysis
df.to_csv('multivariate_mass_ejection_analysis.csv', index=False)


