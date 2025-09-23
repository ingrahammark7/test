import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# Planetary data
planets = ['Earth', 'Venus', 'Mars', 'Titan', 'Pluto']
M = [28.96, 44.01, 43.34, 28.67, 28.02]         # Mean molecular mass (g/mol)
c_p = [1005, 520, 520, 1040, 1000]             # Specific heat J/(kg·K)
m_atm = [1e5, 9.2e6, 2.5e4, 1.5e5, 6.5e-5]    # Atmospheric mass per unit area kg/m^2
T_s = [288, 735, 210, 94, 40]                  # Surface temperature K
z_trop = [12, 55, 40, 40, 4]                   # Troposphere height km

# Create DataFrame
data = pd.DataFrame({
    'Planet': planets,
    'M': M,
    'c_p': c_p,
    'm_atm': m_atm,
    'T_s': T_s,
    'z_trop': z_trop
})

# Log-transform variables where appropriate
X = np.log(data[['M','c_p','m_atm']].replace(0,1e-10))  # Avoid log(0)
X['T_s'] = data['T_s']
y = data['z_trop']

# Standardize predictors
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit linear regression
model = LinearRegression()
model.fit(X_scaled, y)

# Get absolute value of coefficients and rank
coef_abs = np.abs(model.coef_)
predictors = X.columns
importance = pd.DataFrame({'Predictor': predictors, 'Coefficient': coef_abs})
importance = importance.sort_values(by='Coefficient', ascending=False).reset_index(drop=True)

print("Predictor importance ranking:")
print(importance)