import pandas as pd

# ---------------------------
# Step 1: Sample “weak” country data (approximate)
# ---------------------------
data = {
    'Country': ['Zimbabwe', 'Haiti', 'South Sudan', 'Afghanistan', 'Venezuela'],
    'GDP_per_capita': [1500, 1300, 900, 500, 5000],      # USD
    'GDP_growth': [-2, 1, 2, -1, -3],                    # % annual
    'External_debt_GDP': [60, 30, 50, 30, 150],         # % of GDP
    'Fiscal_deficit_GDP': [5, 4, 10, 15, 20],           # % of GDP
    'Governance_score': [30, 25, 20, 15, 35]            # 0-100 scale
}

df = pd.DataFrame(data)

# ---------------------------
# Step 2: Global realistic ranges for normalization
# ---------------------------
global_ranges = {
    'GDP_per_capita': (500, 150000),      # USD
    'GDP_growth': (-5, 10),               # % annual
    'External_debt_GDP': (0, 250),        # % of GDP
    'Fiscal_deficit_GDP': (-10, 20),      # % of GDP
    'Governance_score': (0, 100)          # 0-100 scale
}

# ---------------------------
# Step 3: Scorecard weights
# ---------------------------
weights = {'GDP_per_capita':0.3, 'GDP_growth':0.2, 'External_debt_GDP':0.2,
           'Fiscal_deficit_GDP':0.2, 'Governance_score':0.1}

# ---------------------------
# Step 4: Normalize metrics
# ---------------------------
for metric in weights.keys():
    min_val, max_val = global_ranges[metric]
    if metric in ['External_debt_GDP', 'Fiscal_deficit_GDP']:
        df[f'{metric}_norm'] = (max_val - df[metric]) / (max_val - min_val) * 100
    else:
        df[f'{metric}_norm'] = (df[metric] - min_val) / (max_val - min_val) * 100

# ---------------------------
# Step 5: Compute baseline score
# ---------------------------
df['Baseline_score'] = sum(df[f'{m}_norm']*w for m,w in weights.items())

# ---------------------------
# Step 6: Map to hypothetical rating
# ---------------------------
def score_to_rating(score):
    if score >= 90: return 'AAA'
    elif score >= 80: return 'AA'
    elif score >= 70: return 'A'
    elif score >= 60: return 'BBB'
    elif score >= 50: return 'BB'
    elif score >= 40: return 'B'
    elif score >= 30: return 'CCC'
    else: return 'CC'

df['Hypothetical_rating'] = df['Baseline_score'].apply(score_to_rating)

# ---------------------------
# Step 7: Output results
# ---------------------------
df_sorted = df.sort_values(by='Baseline_score')
print(df_sorted[['Country','Baseline_score','Hypothetical_rating']])