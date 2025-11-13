import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_squared_error, r2_score

# Load historical and modern data
with open('F.json', 'r') as f:
    historical = json.load(f)

with open('f1.json', 'r') as f:
    modern = json.load(f)

df_hist = pd.DataFrame(historical)
df_mod = pd.DataFrame(modern)

# Merge on Country
df = pd.merge(df_hist, df_mod, on='Country', how='inner')

# Features and target
X = df[['GDP_Per_Capita', 'Population_Density']].copy()
y = df['Notable_Per_Million'].copy()

# Log-transform features and target to stabilize scale
X_log = np.log1p(X)
y_log = np.log1p(y)

# Leave-One-Out Cross Validation
loo = LeaveOneOut()
lin_preds = []
rf_preds = []

for train_idx, test_idx in loo.split(X_log):
    X_train, X_test = X_log.iloc[train_idx], X_log.iloc[test_idx]
    y_train, y_test = y_log.iloc[train_idx], y_log.iloc[test_idx]
    
    # Linear Regression
    lin_model = LinearRegression()
    lin_model.fit(X_train, y_train)
    lin_pred = lin_model.predict(X_test)
    lin_preds.append(lin_pred[0])
    
    # Random Forest
    rf_model = RandomForestRegressor(n_estimators=200, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_preds.append(rf_pred[0])

# Evaluate Linear Regression
lin_mse = mean_squared_error(y_log, lin_preds)
lin_r2 = r2_score(y_log, lin_preds)
print(f"Linear Regression LOOCV - MSE: {lin_mse:.3f}, R²: {lin_r2:.3f}")

# Evaluate Random Forest
rf_mse = mean_squared_error(y_log, rf_preds)
rf_r2 = r2_score(y_log, rf_preds)
print(f"Random Forest LOOCV - MSE: {rf_mse:.3f}, R²: {rf_r2:.3f}")

# Back-transform predictions to original scale
df['Predicted_Lin'] = np.expm1(lin_preds)
df['Predicted_RF'] = np.expm1(rf_preds)

print(df[['Country', 'Notable_Per_Million', 'Predicted_Lin', 'Predicted_RF']])