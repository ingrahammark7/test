import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import LeaveOneOut

# Load data
with open('F.json', 'r') as f:
    historical = json.load(f)
with open('f1.json', 'r') as f:
    modern = json.load(f)

df_hist = pd.DataFrame(historical)
df_mod = pd.DataFrame(modern)

df = pd.merge(df_hist, df_mod, on='Country', how='inner')

# Features and target
X = df[['GDP_Per_Capita', 'Population_Density']].copy()
y = df['Notable_Per_Million'].copy()

# Log-transform
X_log = np.log1p(X)
y_log = np.log1p(y)

# LOOCV
loo = LeaveOneOut()
lin_preds = []
rf_preds = []

for train_idx, test_idx in loo.split(X_log):
    X_train, X_test = X_log.iloc[train_idx], X_log.iloc[test_idx]
    y_train, y_test = y_log.iloc[train_idx], y_log.iloc[test_idx]

    # Linear Regression
    lin_model = LinearRegression()
    lin_model.fit(X_train, y_train)
    lin_preds.append(lin_model.predict(X_test)[0])

    # Random Forest
    rf_model = RandomForestRegressor(n_estimators=200, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_preds.append(rf_model.predict(X_test)[0])

# Back-transform predictions
df['Predicted_Lin'] = np.expm1(lin_preds)
df['Predicted_RF'] = np.expm1(rf_preds)

# Predicted vs Actual
print("\n=== Predicted vs Actual Notable Per Million ===")
print(df[['Country', 'Notable_Per_Million', 'Predicted_Lin', 'Predicted_RF']].to_string(index=False))

# Feature importance

# Linear Regression coefficients
lin_model_final = LinearRegression()
lin_model_final.fit(X_log, y_log)
lin_coefs = dict(zip(X.columns, lin_model_final.coef_))

# Random Forest feature importance
rf_model_final = RandomForestRegressor(n_estimators=200, random_state=42)
rf_model_final.fit(X_log, y_log)
rf_importance = dict(zip(X.columns, rf_model_final.feature_importances_))

print("\n=== Feature Importance (Linear Regression Coefficients) ===")
for feature, coef in lin_coefs.items():
    print(f"{feature}: {coef:.4f}")

print("\n=== Feature Importance (Random Forest) ===")
for feature, importance in rf_importance.items():
    print(f"{feature}: {importance:.4f}")