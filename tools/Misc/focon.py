import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Aircraft data with added control surface estimates
data = {
    'WingArea': [56, 27.9, 38, 38, 62, 26.6, 24.18],
    'Sustained': [16, 18, 19.2, 20.5, 22.5, 15, 14],
    'Instantaneous': [28, 24.9, 24, 28, 28, 26, 23.8],
    'EstControlSurfaceArea': [6.5, 5.5, 6.0, 6.5, 11.0, 3.8, 2.6],  # estimated in m²
    'ControlSurfaceRatio': [6.5/56, 5.5/27.9, 6.0/38, 6.5/38, 11.0/62, 3.8/26.6, 2.6/24.18],
    'UnusualSurface': [0, 1, 1, 1, 1, 1, 0]  # binary flag for design outliers
}

idx = ['F-15', 'F-16', 'F/A-18', 'MiG-29', 'Su-27', 'Tornado', 'Jaguar']
df = pd.DataFrame(data, index=idx)

# Correlation matrix
corr = df.corr()

# Plot correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix: Wing, Turn, and Control Surface Traits")
plt.show()

df[['WingArea', 'EstControlSurfaceArea', 'ControlSurfaceRatio', 'UnusualSurface']]