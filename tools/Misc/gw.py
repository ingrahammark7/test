import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# --- Load JSON ---
with open("clean.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# --- Compute percent error ---
df['percent_error'] = df['A_value'] / df['lethal_armor_cm']

# --- Identify extreme outliers ---
outlier_threshold = 100_000
outliers = df[df['percent_error'] > outlier_threshold]
if not outliers.empty:
    print("=== Removed Outliers (percent_error > {:,}) ===".format(outlier_threshold))
    print(outliers[['diameter_cm', 'mass_kg', 'percent_error']].to_string(index=False))

# --- Keep only reasonable data ---
df_filtered = df[df['percent_error'] <= outlier_threshold].copy()

# --- Features ---
features_to_exclude = ['percent_error', 'A_value', 'actual_value', 'penetration_cm','lethal_armor_cm']
X = df_filtered.drop(columns=features_to_exclude)
y = np.log1p(df_filtered['percent_error'])  # log-transform target

# --- Fill missing values ---
X = X.fillna(0)

# --- Train/test split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Train model ---
model = RandomForestRegressor(n_estimators=500, max_depth=None, random_state=42)
model.fit(X_train, y_train)

# --- Predictions ---
y_pred_test = model.predict(X_test)
y_pred_all = model.predict(X)

# --- Evaluation ---
mse = mean_squared_error(y_test, y_pred_test)
r2 = r2_score(y_test, y_pred_test)
print("\nMean Squared Error:", mse)
print("R^2 Score:", r2)

# --- Row-by-row comparison ---
df_filtered['predicted_percent_error'] = np.expm1(y_pred_all)  # revert log-transform
comparison = df_filtered[['diameter_cm', 'mass_kg', 'percent_error', 'predicted_percent_error']]
print("\n=== Row-by-Row Comparison ===")
print(comparison.to_string(index=False))

# --- Feature importance ---
importances = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values(by='importance', ascending=False)
print("\n=== Predictor Contribution Ranking ===")
print(importances.to_string(index=False))