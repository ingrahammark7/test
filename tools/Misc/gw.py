import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from scipy.optimize import minimize

# ---------------------------
# Step 1: Sample data
# ---------------------------
data = {
    'Country': [
        'Austria', 'Belgium', 'France', 'Germany', 'Italy', 'Netherlands', 'Portugal', 'Spain',
        'South Africa', 'Nigeria', 'Kenya', 'Egypt', 'Ghana'
    ],
    'GDP_per_capita': [534791, 664564, 450000, 620000, 1370000, 530000, 250000, 350000,
                       6670, 1200, 2000, 5000, 1500],
    'GDP_growth': [1.1, 1.0, 1.2, 1.3, 0.5, 1.4, 1.0, 1.1,
                   0.5, 2.5, 5.0, 3.0, 4.0],
    'External_debt_GDP': [81.8, 104.7, 98.0, 69.0, 137.0, 50.0, 60.0, 100.0,
                          76.36, 35.0, 40.0, 30.0, 55.0],
    'Fiscal_deficit_GDP': [4.7, 4.5, 3.0, 2.9, 3.4, 2.5, 3.0, 3.5,
                           5.0, 4.0, 5.0, 6.0, 4.5],
    'Governance_score': [85, 80, 75, 90, 70, 85, 65, 60,
                         60, 50, 55, 65, 60],
    'S&P_rating_numeric': [100, 98, 95, 100, 85, 95, 80, 85,
                           60, 50, 55, 60, 65]
}

df = pd.DataFrame(data)

# ---------------------------
# Step 2: UN geoscheme mapping
# ---------------------------
country_region_map = {
    'Austria': 'Western Europe', 'Belgium': 'Western Europe', 'France': 'Western Europe', 
    'Germany': 'Western Europe', 'Italy': 'Southern Europe', 'Netherlands': 'Western Europe', 
    'Portugal': 'Southern Europe', 'Spain': 'Southern Europe',
    'South Africa': 'Sub-Saharan Africa', 'Nigeria': 'Sub-Saharan Africa', 'Kenya': 'Sub-Saharan Africa',
    'Egypt': 'Northern Africa', 'Ghana': 'Sub-Saharan Africa'
}
df['Region'] = df['Country'].map(country_region_map)

regions = df['Region'].unique()

# ---------------------------
# Step 3: Scorecard weights and normalization
# ---------------------------
weights = {'GDP_per_capita':0.3, 'GDP_growth':0.2, 'External_debt_GDP':0.2,
           'Fiscal_deficit_GDP':0.2, 'Governance_score':0.1}
metrics = ['GDP_per_capita','GDP_growth','External_debt_GDP','Fiscal_deficit_GDP','Governance_score']

for m in metrics:
    df[f'{m}_norm'] = (df[m] - df[m].min())/(df[m].max()-df[m].min())*100

df['Baseline_score'] = sum(df[f'{m}_norm']*w for m,w in weights.items())

# ---------------------------
# Step 4: Optimization function
# ---------------------------
def negative_corr(fixed_effects_array):
    fixed_effects_dict = dict(zip(regions, fixed_effects_array))
    df['Adjusted_score'] = df['Baseline_score'] + df['Region'].map(fixed_effects_dict)
    corr = pearsonr(df['Adjusted_score'], df['S&P_rating_numeric'])[0]
    return -corr  # minimize negative correlation to maximize correlation

# Initial guess: zeros
initial_guess = np.zeros(len(regions))

# Run optimizer
result = minimize(negative_corr, initial_guess, method='BFGS')

optimized_effects = dict(zip(regions, result.x))

# Apply optimized fixed effects
df['Baseline_score_adj'] = df['Baseline_score'] + df['Region'].map(optimized_effects)

def score_to_rating(score):
    if score >= 90: return 'AAA'
    elif score >= 80: return 'AA'
    elif score >= 70: return 'A'
    elif score >= 60: return 'BBB'
    elif score >= 50: return 'BB'
    else: return 'B'

df['Hypothetical_rating_adj'] = df['Baseline_score_adj'].apply(score_to_rating)
df['Difference_adj'] = df['S&P_rating_numeric'] - df['Baseline_score_adj']

# ---------------------------
# Step 5: Output results
# ---------------------------
print("Optimized regional fixed effects:")
for r,v in optimized_effects.items():
    print(f"{r}: {v:.2f}")

corr_final = pearsonr(df['Baseline_score_adj'], df['S&P_rating_numeric'])[0]
print(f"\nMax correlation after optimization: {corr_final:.2f}\n")

print(df[['Country','Region','Baseline_score','Baseline_score_adj',
          'Hypothetical_rating_adj','S&P_rating_numeric','Difference_adj']])