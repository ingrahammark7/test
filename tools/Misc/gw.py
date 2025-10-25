import pandas as pd
import matplotlib.pyplot as plt

# Realistic dataset of 50 countries (2021 estimates)
data = {
    'Country': [
        'USA','India','Brazil','China','Australia','Russia','Canada','Argentina','Mexico','Indonesia',
        'France','Germany','UK','Italy','Spain','Turkey','Iran','Egypt','South Africa','Nigeria',
        'Kenya','Ethiopia','Sudan','Saudi Arabia','Pakistan','Bangladesh','Thailand','Vietnam','Philippines','Japan',
        'South Korea','New Zealand','Norway','Sweden','Finland','Poland','Ukraine','Belarus','Chile','Peru',
        'Colombia','Venezuela','Morocco','Algeria','Tunisia','Iraq','Syria','Afghanistan','Nepal','Sri Lanka'
    ],
    'Arable_Land_per_Capita_ha': [
        0.21,0.12,0.36,0.10,1.01,0.14,0.31,0.45,0.13,0.06,
        0.18,0.12,0.10,0.12,0.13,0.10,0.08,0.03,0.09,0.04,
        0.06,0.05,0.10,0.02,0.05,0.01,0.06,0.05,0.04,0.01,
        0.01,0.56,0.15,0.18,0.14,0.12,0.12,0.10,0.21,0.11,
        0.09,0.12,0.03,0.08,0.07,0.02,0.01,0.01,0.02,0.02
    ],
    'Livestock_per_Capita_LU': [
        1.2,0.5,1.5,0.8,2.0,1.0,1.3,1.8,0.7,0.4,
        1.1,1.0,0.9,1.0,1.0,0.7,0.5,0.3,0.6,0.4,
        0.8,0.5,0.7,0.2,0.5,0.3,0.6,0.5,0.4,0.7,
        0.6,1.5,1.2,1.3,1.2,1.0,0.9,0.8,1.1,0.9,
        0.8,0.7,0.5,0.6,0.5,0.4,0.3,0.4,0.4,0.4
    ]
}

df = pd.DataFrame(data)

# Calculate Pearson correlation coefficient
correlation = df['Arable_Land_per_Capita_ha'].corr(df['Livestock_per_Capita_LU'])
print(f"Pearson Correlation Coefficient: {correlation:.2f}")

# Scatter plot
plt.figure(figsize=(10,6))
plt.scatter(df['Arable_Land_per_Capita_ha'], df['Livestock_per_Capita_LU'])
plt.title('Arable Land per Capita vs Livestock per Capita (50 Countries)')
plt.xlabel('Arable Land per Capita (ha)')
plt.ylabel('Livestock per Capita (LU)')
plt.grid(True)

# Annotate a few countries for clarity
for i, row in df.iterrows():
    if row['Arable_Land_per_Capita_ha'] > 0.5 or row['Livestock_per_Capita_LU'] > 1.8:
        plt.text(row['Arable_Land_per_Capita_ha'], row['Livestock_per_Capita_LU'], row['Country'], fontsize=8)

plt.show()