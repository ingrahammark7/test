import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load historical data (F.json)
with open('f.json', 'r') as f:
    historical = json.load(f)

# Load modern GDP & density data (f1.json)
with open('f1.json', 'r') as f:
    modern = json.load(f)

# Convert to DataFrames
df_hist = pd.DataFrame(historical)
df_mod = pd.DataFrame(modern)

# Merge on Country
df = pd.merge(df_hist, df_mod, on='Country', how='inner')

# Features: modern GDP & density
X = df[['GDP_Per_Capita', 'Population_Density']]
y = df['Notable_Per_Million']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Random Forest Regressor
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred):.3f}")
print(f"R^2 Score: {r2_score(y_test, y_pred):.3f}")

# Predict for all countries
df['Predicted_Notable_Per_Million'] = model.predict(X)
print(df[['Country', 'Notable_Per_Million', 'Predicted_Notable_Per_Million']])