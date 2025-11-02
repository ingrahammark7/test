import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------------
# Step 1: Expanded dataset with continent
# ----------------------------
data = [
    ['China', 0.48, 13000, 153, 35.0, 103.8, 'Asia'],
    ['India', 0.20, 2500, 464, 20.0, 78.0, 'Asia'],
    ['Brazil', 1.8, 9000, 25, -10.0, -55.0, 'South America'],
    ['South Africa', 0.31, 7000, 48, -30.0, 25.0, 'Africa'],
    ['Luxembourg', 4.0, 130000, 250, 49.6, 6.1, 'Europe'],
    ['Germany', 1.0, 55000, 232, 51.2, 10.4, 'Europe'],
    ['France', 0.9, 53000, 122, 46.2, 2.2, 'Europe'],
    ['Japan', 0.7, 45000, 347, 36.2, 138.3, 'Asia'],
    ['USA', 0.6, 72000, 36, 37.1, -95.7, 'North America'],
    ['Russia', 0.4, 11000, 9, 61.0, 105.0, 'Europe/Asia'],
    ['Canada', 0.5, 52000, 4, 56.1, -106.3, 'North America'],
    ['Australia', 0.8, 60000, 3, -25.3, 133.8, 'Oceania'],
    ['Mexico', 0.9, 10000, 66, 23.6, -102.5, 'North America'],
    ['UK', 1.2, 49000, 275, 55.4, -3.4, 'Europe'],
    ['Italy', 1.1, 45000, 206, 41.9, 12.6, 'Europe'],
    ['Spain', 1.0, 43000, 94, 40.4, -3.7, 'Europe'],
    ['South Korea', 0.9, 42000, 527, 36.5, 127.8, 'Asia'],
    ['Argentina', 0.7, 11000, 16, -38.4, -63.6, 'South America'],
    ['Egypt', 0.3, 3600, 103, 26.8, 30.8, 'Africa'],
    ['Nigeria', 0.15, 2500, 223, 9.1, 8.7, 'Africa'],
    ['Turkey', 0.6, 12000, 109, 38.9, 35.2, 'Europe/Asia'],
    ['Saudi Arabia', 0.2, 24000, 16, 23.9, 45.0, 'Asia'],
    ['Norway', 1.5, 80000, 15, 60.5, 8.5, 'Europe'],
    ['Sweden', 1.4, 55000, 25, 60.1, 18.6, 'Europe'],
    ['Finland', 1.3, 52000, 18, 61.9, 25.7, 'Europe'],
    ['Netherlands', 2.0, 53000, 508, 52.1, 5.3, 'Europe'],
    ['Belgium', 1.9, 51000, 383, 50.8, 4.3, 'Europe'],
    ['Singapore', 5.0, 72000, 8358, 1.4, 103.8, 'Asia'],
    ['Thailand', 0.35, 7000, 137, 15.9, 101.0, 'Asia'],
    ['Vietnam', 0.25, 4000, 311, 14.0, 108.3, 'Asia']
]

df = pd.DataFrame(data, columns=[
    'Country', 'Buses_per_1000', 'GDP_per_capita_USD',
    'Population_density_per_km2', 'Latitude', 'Longitude', 'Continent'
])

# ----------------------------
# Step 2: Scatterplot matrix with regression
# ----------------------------
sns.set(style="whitegrid")
plot_vars = ['Buses_per_1000', 'GDP_per_capita_USD', 'Population_density_per_km2']

pairplot = sns.pairplot(df, 
                        vars=plot_vars, 
                        hue='Continent', 
                        kind='reg', 
                        height=3, 
                        corner=True,
                        palette='tab10')

pairplot.fig.suptitle("Buses per 1000 vs GDP and Population Density", y=1.02)

plt.show()