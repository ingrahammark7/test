import pandas as pd
import seaborn as sns

# ----------------------------
# Step 1: Expanded maximal dataset
# ----------------------------
data = [
    ['China', 0.48, 13000, 153, 35.0, 103.8],
    ['India', 0.20, 2500, 464, 20.0, 78.0],
    ['Brazil', 1.8, 9000, 25, -10.0, -55.0],
    ['South Africa', 0.31, 7000, 48, -30.0, 25.0],
    ['Luxembourg', 4.0, 130000, 250, 49.6, 6.1],
    ['Germany', 1.0, 55000, 232, 51.2, 10.4],
    ['France', 0.9, 53000, 122, 46.2, 2.2],
    ['Japan', 0.7, 45000, 347, 36.2, 138.3],
    ['USA', 0.6, 72000, 36, 37.1, -95.7],
    ['Russia', 0.4, 11000, 9, 61.0, 105.0],
    ['Canada', 0.5, 52000, 4, 56.1, -106.3],
    ['Australia', 0.8, 60000, 3, -25.3, 133.8],
    ['Mexico', 0.9, 10000, 66, 23.6, -102.5],
    ['UK', 1.2, 49000, 275, 55.4, -3.4],
    ['Italy', 1.1, 45000, 206, 41.9, 12.6],
    ['Spain', 1.0, 43000, 94, 40.4, -3.7],
    ['South Korea', 0.9, 42000, 527, 36.5, 127.8],
    ['Argentina', 0.7, 11000, 16, -38.4, -63.6],
    ['Egypt', 0.3, 3600, 103, 26.8, 30.8],
    ['Nigeria', 0.15, 2500, 223, 9.1, 8.7],
    ['Turkey', 0.6, 12000, 109, 38.9, 35.2],
    ['Saudi Arabia', 0.2, 24000, 16, 23.9, 45.0],
    ['Norway', 1.5, 80000, 15, 60.5, 8.5],
    ['Sweden', 1.4, 55000, 25, 60.1, 18.6],
    ['Finland', 1.3, 52000, 18, 61.9, 25.7],
    ['Netherlands', 2.0, 53000, 508, 52.1, 5.3],
    ['Belgium', 1.9, 51000, 383, 50.8, 4.3],
    ['Singapore', 5.0, 72000, 8358, 1.4, 103.8],
    ['Thailand', 0.35, 7000, 137, 15.9, 101.0],
    ['Vietnam', 0.25, 4000, 311, 14.0, 108.3]
]

df = pd.DataFrame(data, columns=[
    'Country', 'Buses_per_1000', 'GDP_per_capita_USD',
    'Population_density_per_km2', 'Latitude', 'Longitude'
])

# ----------------------------
# Step 2: Compute correlation matrix
# ----------------------------
corr = df[['Buses_per_1000', 'GDP_per_capita_USD', 
           'Population_density_per_km2', 'Latitude', 'Longitude']].corr()

# ----------------------------
# Step 3: Print nicely formatted console output
# ----------------------------
print("\n=== Buses per Capita Correlation Matrix ===\n")
print(corr.round(3))

bus_corr = corr['Buses_per_1000'].drop('Buses_per_1000').sort_values(ascending=False)
print("\n--- Buses per 1000 inhabitants correlations ---")
for var, value in bus_corr.items():
    print(f"{var}: {value:.3f}")

# ----------------------------
# Step 4: Optional visualization
# ----------------------------
sns.pairplot(df,
             vars=['Buses_per_1000', 'GDP_per_capita_USD', 
                   'Population_density_per_km2', 'Latitude', 'Longitude'],
             kind='reg', height=2.5, corner=True)

# ----------------------------
# Step 5: Save dataset
# ----------------------------
df.to_csv('buses_per_capita_dataset_expanded.csv', index=False)
print("\nDataset saved as 'buses_per_capita_dataset_expanded.csv'")