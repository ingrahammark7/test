import pandas as pd
import seaborn as sns


# ----------------------------
# Step 1: Create maximal dataset
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
    ['Russia', 0.4, 11000, 9, 61.0, 105.0]
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
print(corr.round(3))  # rounded for console readability

# Highlight strongest correlations for quick console insight
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
             kind='reg', height=2.5)


# ----------------------------
# Step 5: Save dataset
# ----------------------------
df.to_csv('buses_per_capita_dataset.csv', index=False)
print("\nDataset saved as 'buses_per_capita_dataset.csv'")