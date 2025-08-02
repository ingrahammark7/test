import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Extended dataset: 2010-2030 with real + simulated crisis years
data = {
    'Year': list(range(2010, 2031)),
    'Hearings_Present': [
        1,1,0,1,0,1,1,1,1,0,1,1,0,1,1,0,1,1,1,0,1
    ],
    'Shutdown': [
        0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,1,1,1,1
    ],
    'Default': [
        0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1
    ],
    'US_10yr_Treasury_Yield': [
        3.2,2.0,1.8,2.5,2.0,2.1,1.9,2.3,3.0,2.4,0.9,1.3,1.6,2.8,3.9,
        4.2,5.5,7.0,8.5,9.8,11.0
    ],
    'US_CDS_Spread': [
        65,60,55,70,65,62,58,63,75,70,50,55,58,85,250,
        310,600,750,900,1100,1300
    ],
    'Debt_to_GDP': [
        90,95,98,101,104,106,108,110,112,114,130,135,138,142,145,
        150,160,165,170,175,180
    ],
    'Global_EM_CDS_Avg': [
        240,250,260,270,280,290,300,310,320,330,350,340,345,360,400,
        420,480,510,550,580,600
    ],
    'Commodity_Index': [
        125,120,115,110,108,105,102,105,108,110,115,118,114,110,102,
        98,90,85,80,75,70
    ]
}

# Load data into DataFrame
df = pd.DataFrame(data)

# Features and target
features = [
    'Hearings_Present', 'Shutdown', 'US_10yr_Treasury_Yield', 
    'US_CDS_Spread', 'Debt_to_GDP', 'Global_EM_CDS_Avg', 'Commodity_Index'
]
X = df[features]
y = df['Default']

# Scale features for logistic regression
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train logistic regression model
model = LogisticRegression()
model.fit(X_scaled, y)

# Predict default probabilities
df['Default_Prob'] = model.predict_proba(X_scaled)[:, 1]

# Print the results
print(df[['Year', 'Default', 'Default_Prob']])

# Plot predicted default probability over time
plt.figure(figsize=(12,6))
plt.plot(df['Year'], df['Default_Prob'], label='Predicted Default Probability', marker='o')
plt.scatter(df['Year'], df['Default'], color='red', label='Actual Default (1=yes)', zorder=5)
plt.xlabel('Year')
plt.ylabel('Default Probability')
plt.title('Default Probability Prediction (2010-2030)')
plt.legend()
plt.grid(True)
plt.show()