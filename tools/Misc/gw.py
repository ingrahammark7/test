import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# -------------------------------
# 1. Hardcoded data
# -------------------------------
data = {
    'country': [
        'USA', 'Sweden', 'Brazil', 'Japan',
        'Russia', 'Thailand', 'Germany', 'Nigeria'
    ],
    'accident_rate_per_million_flights': [
        1.4, 0.5, 3.2, 0.3,
        2.8, 4.5, 0.4, 6.1
    ],
    'gdp_per_capita_usd': [
        65000, 60000, 15000, 50000,
        12000, 7800, 55000, 2500
    ],
    'drug_use_percent': [
        10.5, 6.4, 8.8, 3.2,
        5.5, 9.0, 5.8, 7.5
    ],
    'fleet_age_years': [
        12, 7, 15, 10,
        20, 18, 8, 22
    ],
    'weather_risk_index': [
        4, 5, 7, 3,
        5, 8, 4, 9
    ]
}

df = pd.DataFrame(data)
numeric_cols = [
    'accident_rate_per_million_flights',
    'gdp_per_capita_usd',
    'drug_use_percent',
    'fleet_age_years',
    'weather_risk_index'
]

# -------------------------------
# 2. Standardize numeric columns
# -------------------------------
scaler = StandardScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
print("Step 1: Standardized numeric data:")
print(df[numeric_cols].head(), "\n")  # Partial output

# -------------------------------
# 3. Compute correlation matrix
# -------------------------------
print("Step 2: Correlation matrix:")
corr = df[numeric_cols].corr()
print(corr, "\n")  # Partial output

# -------------------------------
# 4. Linear regression model
# -------------------------------
X = df[['gdp_per_capita_usd', 'drug_use_percent', 'fleet_age_years', 'weather_risk_index']]
y = df['accident_rate_per_million_flights']

model = LinearRegression().fit(X, y)
print("Step 3: Regression coefficients:")
for feature, coef in zip(X.columns, model.coef_):
    print(f"{feature}: {coef:.3f}")

print(f"Intercept: {model.intercept_:.3f}\n")

# -------------------------------
# 5. Predicted accident rates (partial)
# -------------------------------
predictions = model.predict(X)
df['predicted_accident_rate'] = predictions
print("Step 4: Predicted accident rates (first 5 countries):")
print(df[['country','predicted_accident_rate']].head())