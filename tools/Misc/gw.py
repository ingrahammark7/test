import pandas as pd
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression

# ----------------------------
# Step 1: Dataset
# ----------------------------
data = [
    ['China', 0.48, 13000, 153],
    ['India', 0.20, 2500, 464],
    ['Brazil', 1.8, 9000, 25],
    ['South Africa', 0.31, 7000, 48],
    ['Luxembourg', 4.0, 130000, 250],
    ['Germany', 1.0, 55000, 232],
    ['France', 0.9, 53000, 122],
    ['Japan', 0.7, 45000, 347],
    ['USA', 0.6, 72000, 36],
    ['Russia', 0.4, 11000, 9],
    ['Canada', 0.5, 52000, 4],
    ['Australia', 0.8, 60000, 3],
    ['Mexico', 0.9, 10000, 66],
    ['UK', 1.2, 49000, 275],
    ['Italy', 1.1, 45000, 206],
    ['Spain', 1.0, 43000, 94],
    ['South Korea', 0.9, 42000, 527],
    ['Argentina', 0.7, 11000, 16],
    ['Egypt', 0.3, 3600, 103],
    ['Nigeria', 0.15, 2500, 223],
    ['Turkey', 0.6, 12000, 109],
    ['Saudi Arabia', 0.2, 24000, 16],
    ['Norway', 1.5, 80000, 15],
    ['Sweden', 1.4, 55000, 25],
    ['Finland', 1.3, 52000, 18],
    ['Netherlands', 2.0, 53000, 508],
    ['Belgium', 1.9, 51000, 383],
    ['Singapore', 5.0, 72000, 8358],
    ['Thailand', 0.35, 7000, 137],
    ['Vietnam', 0.25, 4000, 311]
]

df = pd.DataFrame(data, columns=[
    'Country', 'Buses_per_1000', 'GDP_per_capita_USD', 'Population_density_per_km2'
])

# ----------------------------
# Step 2: Fit linear regression plane
# ----------------------------
X = df[['Population_density_per_km2', 'GDP_per_capita_USD']]
y = df['Buses_per_1000']
model = LinearRegression()
model.fit(X, y)

# Grid for plane
x_surf = np.linspace(df['Population_density_per_km2'].min(), df['Population_density_per_km2'].max(), 20)
y_surf = np.linspace(df['GDP_per_capita_USD'].min(), df['GDP_per_capita_USD'].max(), 20)
x_surf, y_surf = np.meshgrid(x_surf, y_surf)
z_surf = model.intercept_ + model.coef_[0]*x_surf + model.coef_[1]*y_surf

# ----------------------------
# Step 3: Interactive 3D plot
# ----------------------------
fig = go.Figure()

# Scatter points (actual countries)
fig.add_trace(go.Scatter3d(
    x=df['Population_density_per_km2'],
    y=df['GDP_per_capita_USD'],
    z=df['Buses_per_1000'],
    mode='markers+text',
    text=df['Country'],
    textposition='top center',
    marker=dict(size=5, color='blue'),
    name='Countries'
))

# Regression plane
fig.add_trace(go.Surface(
    x=x_surf,
    y=y_surf,
    z=z_surf,
    colorscale='Oranges',
    opacity=0.5,
    name='Regression Plane'
))

# Layout
fig.update_layout(
    scene=dict(
        xaxis_title='Population Density (per km²)',
        yaxis_title='GDP per Capita (USD)',
        zaxis_title='Buses per 1000'
    ),
    title='Interactive 3D: Buses per Capita vs Density & GDP'
)

fig.show()