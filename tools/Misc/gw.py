import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load JSON
with open("clean.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Compute percent error
df['percent_error'] = df['A_value'] / df['lethal_armor_cm']

# Identify extreme outlier (0.9 cm round)
outliers = df[df['percent_error'] > 1e6]
if not outliers.empty:
    print("=== Removed Outliers ===")
    print(outliers[['diameter_cm', 'mass_kg', 'percent_error']].to_string(index=False))

# Drop only extreme outlier
df_filtered = df[df['percent_error'] <= 1e6]

# Features: exclude direct outcomes like penetration_cm
features_to_exclude = ['percent_error', 'A_value', 'actual_value', 'penetration_cm','lethal_armor_cm']
X = df_filtered.drop(columns=features_to_exclude)
y = df_filtered['percent_error']

# Fill missing values
X = X.fillna(0)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("\nMean Squared Error:", mse)
print("R^2 Score:", r2)

# Row-by-row comparison
df_filtered.loc[:, 'predicted_percent_error'] = model.predict(X)
comparison = df_filtered[['diameter_cm', 'mass_kg', 'percent_error', 'predicted_percent_error']]
print("\n=== Row-by-Row Comparison ===")
print(comparison.to_string(index=False))

# Feature importance
importances = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values(by='importance', ascending=False)
print("\n=== Predictor Contribution Ranking ===")
print(importances.to_string(index=False))