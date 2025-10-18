import pandas as pd

# ---------------------------
# Step 1: Sample macroeconomic data for EU15 + top OECD
# Values are approximate
# ---------------------------
data = {
    'Country': [
        'Luxembourg', 'Switzerland', 'Norway', 'Germany', 'Austria', 'Netherlands', 'France', 'Italy', 'Spain', 'Belgium',
        'Denmark', 'Sweden', 'Finland', 'Ireland', 'Portugal', 'United States', 'Singapore', 'Canada', 'Australia', 'Japan'
    ],
    'GDP_per_capita': [
        140000, 90000, 100000, 62000, 53000, 53000, 45000, 35000, 35000, 50000,
        60000, 55000, 50000, 85000, 25000, 76000, 105000, 65000, 70000, 42000
    ],
    'GDP_growth': [
        2.0, 1.5, 1.2, 1.3, 1.1, 1.4, 1.2, 0.5, 1.1, 1.0,
        1.0, 1.1, 1.0, 3.5, 1.0, 2.0, 3.0, 1.8, 2.2, 0.8
    ],
    'External_debt_GDP': [
        20, 180, 40, 69, 81, 50, 98, 137, 100, 105,
        30, 35, 40, 100, 60, 130, 180, 90, 60, 250
    ],
    'Fiscal_deficit_GDP': [
        0, 2, -1, 3, 4, 3, 3, 3.5, 3.5, 4.5,
        1, 1.5, 2, 0, 3, 5, 2, 3, 2.5, 6
    ],
    'Governance_score': [
        95, 92, 93, 90, 85, 85, 75, 70, 60, 80,
        90, 88, 87, 90, 65, 90, 92, 88, 89, 85
    ]
}

df = pd.DataFrame(data)

# ---------------------------
# Step 2: Global realistic ranges
# ---------------------------
global_ranges = {
    'GDP_per_capita': (1000, 150000),
    'GDP_growth': (-5, 10),
    'External_debt_GDP': (0, 250),
    'Fiscal_deficit_GDP': (-10, 20),
    'Governance_score': (0, 100)
}

# ---------------------------
# Step 3: Weights
# ---------------------------
weights = {'GDP_per_capita':0.3, 'GDP_growth':0.2, 'External_debt_GDP':0.2,
           'Fiscal_deficit_GDP':0.2, 'Governance_score':0.1}

# ---------------------------
# Step 4: Normalize metrics
# ---------------------------
for metric in weights.keys():
    min_val, max_val = global_ranges[metric]
    if metric in ['External_debt_GDP','Fiscal_deficit_GDP']:
        df[f'{metric}_norm'] = (max_val - df[metric]) / (max_val - min_val) * 100
    else:
        df[f'{metric}_norm'] = (df[metric] - min_val) / (max_val - min_val) * 100

# ---------------------------
# Step 5: Compute baseline score
# ---------------------------
df['Baseline_score'] = sum(df[f'{m}_norm']*w for m,w in weights.items())

# ---------------------------
# Step 6: Map to rating
# ---------------------------
def score_to_rating(score):
    if score >= 90: return 'AAA'
    elif score >= 80: return 'AA'
    elif score >= 70: return 'A'
    elif score >= 60: return 'BBB'
    elif score >= 50: return 'BB'
    else: return 'B'

df['Hypothetical_rating'] = df['Baseline_score'].apply(score_to_rating)

# ---------------------------
# Step 7: Output top scorers
# ---------------------------
df_sorted = df.sort_values(by='Baseline_score', ascending=False)
print(df_sorted[['Country','Baseline_score','Hypothetical_rating']])