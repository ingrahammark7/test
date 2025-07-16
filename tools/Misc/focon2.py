import pandas as pd
from sklearn.linear_model import LinearRegression

# Data with 'Nationality' column
data = {
    'Aircraft': ['F-16', 'Su-27', 'MiG-29', 'F/A-18', 'Tornado', 'F-15', 'Jaguar'],
    'Wing Area (m²)': [27.9, 62.0, 38.0, 38.0, 26.6, 56.0, 24.18],
    'Ctrl Surface Area (m²)': [5.5, 11.0, 6.5, 6.0, 3.8, 6.5, 2.6],
    'Ctrl/Wing Ratio': [5.5/27.9, 11.0/62.0, 6.5/38.0, 6.0/38.0, 3.8/26.6, 6.5/56.0, 2.6/24.18],
    'Mass (kg)': [12000, 30000, 18000, 14500, 23000, 14500, 13000],
    'Instability Factor': [0.9, 0.7, 0.85, 0.8, 0.6, 0.5, 0.4],
    'Sustained Turn Rate (°/s)': [18.0, 22.5, 20.5, 19.2, 15.0, 16.0, 14.0],
    'Instantaneous Turn Rate (°/s)': [24.9, 28.0, 28.0, 24.0, 26.0, 28.0, 23.8],
    'Nationality': ['US', 'Russia', 'Russia', 'US', 'UK', 'US', 'UK']
}

df = pd.DataFrame(data)

def calc_combined_r2(df_sub, target):
    X = df_sub[['Mass (kg)', 'Instability Factor']].values
    y = df_sub[target].values
    model = LinearRegression().fit(X, y)
    return model.score(X, y)

def calculate_r2_with_exclusions(df, excluded_aircraft=None):
    if excluded_aircraft is None:
        excluded_aircraft = []
    # Filter out excluded aircraft
    df_filtered = df[~df['Aircraft'].isin(excluded_aircraft)]
    
    # Split datasets by nationality
    df_british = df_filtered[df_filtered['Nationality'] == 'UK']
    df_non_british = df_filtered[df_filtered['Nationality'] != 'UK']
    
    results = {
        'British Sustained': calc_combined_r2(df_british, 'Sustained Turn Rate (°/s)'),
        'British Instantaneous': calc_combined_r2(df_british, 'Instantaneous Turn Rate (°/s)'),
        'Non-British Sustained': calc_combined_r2(df_non_british, 'Sustained Turn Rate (°/s)'),
        'Non-British Instantaneous': calc_combined_r2(df_non_british, 'Instantaneous Turn Rate (°/s)')
    }
    
    return results

# Calculate with all aircraft
all_results = calculate_r2_with_exclusions(df)

# Calculate excluding the F-15
exclusion_results = calculate_r2_with_exclusions(df, excluded_aircraft=['F-15','F-18','MiG-29'])

print("R² with all aircraft included:")
for key, val in all_results.items():
    print(f"{key}: {val:.3f}")

print("\nR² excluding F-15:")
for key, val in exclusion_results.items():
    print(f"{key}: {val:.3f}")