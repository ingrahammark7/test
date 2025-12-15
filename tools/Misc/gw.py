import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# -------------------------------
# 1. Hardcoded real/estimated data
# -------------------------------

data = {
    'country': [
        'USA', 'Sweden', 'Brazil', 'Japan',
        'Russia', 'Thailand', 'Germany', 'Nigeria'
    ],
    # Hypothetical fatal accident rate per million flights
    # (based on global trends; these are NOT real exact figures per country)
    # you would replace with real data from aviation safety sources.
    'accident_rate_per_million_flights': [
        1.4, 0.5, 3.2, 0.3,
        2.8, 4.5, 0.4, 6.1
    ],
    # GDP per capita (USD) hardcoded approximations for 2023
    'gdp_per_capita_usd': [
        65000, 60000, 15000, 50000,
        12000, 7800, 55000, 2500
    ],
    # Estimated prevalence of drug use (percent, general illicit drug use)
    # Proxy indicator from UNODC World Drug Report estimates
    'drug_use_percent': [
        10.5, 6.4, 8.8, 3.2,
        5.5, 9.0, 5.8, 7.5
    ],
    # Estimated average fleet age (years)
    'fleet_age_years': [
        12, 7, 15, 10,
        20, 18, 8, 22
    ],
    # Weather risk index (higher means more weather disruption)
    'weather_risk_index': [
        4, 5, 7, 3,
        5, 8, 4, 9
    ]
}

df = pd.DataFrame(data)

# -----------------------------
# 2. Standardize numeric columns
# -----------------------------
numeric_cols = [
    'accident_rate_per_million_flights',
    'gdp_per_capita_usd',
    'drug_use_percent',
    'fleet_age_years',
    'weather_risk_index'
]

scaler = StandardScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# -----------------------------
# 3. Compute correlation matrix
# -----------------------------
corr = df[numeric_cols].corr()
print("Correlation matrix:\n", corr)

# Show correlations visually
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Correlation between Accident Rates and Factors")
plt.show()

# -----------------------------
# 4. Simple regression model
# -----------------------------
X = df[['gdp_per_capita_usd', 'drug_use_percent', 'fleet_age_years', 'weather_risk_index']]
y = df['accident_rate_per_million_flights']

model = LinearRegression().fit(X, y)
print("\nRegression coefficients:")
for feature, coef in zip(X.columns, model.coef_):
    print(f"{feature}: {coef:.3f}")

print(f"Intercept: {model.intercept_:.3f}")