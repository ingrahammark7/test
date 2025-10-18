import pandas as pd
from scipy.stats import pearsonr

# ---------------------------
# Step 1: Sample macroeconomic data
# ---------------------------
data = {
    'Country': [
        'Austria', 'Belgium', 'France', 'Germany', 'Italy', 'Netherlands', 'Portugal', 'Spain',
        'South Africa', 'Nigeria', 'Kenya', 'Egypt', 'Ghana'
    ],
    'GDP_per_capita': [
        534791, 664564, 450000, 620000, 1370000, 530000, 250000, 350000,
        6670, 1200, 2000, 5000, 1500
    ],
    'GDP_growth': [
        1.1, 1.0, 1.2, 1.3, 0.5, 1.4, 1.0, 1.1,
        0.5, 2.5, 5.0, 3.0, 4.0
    ],
    'External_debt_GDP': [
        81.8, 104.7, 98.0, 69.0, 137.0, 50.0, 60.0, 100.0,
        76.36, 35.0, 40.0, 30.0, 55.0
    ],
    'Fiscal_deficit_GDP': [
        4.7, 4.5, 3.0, 2.9, 3.4, 2.5, 3.0, 3.5,
        5.0, 4.0, 5.0, 6.0, 4.5
    ],
    'Governance_score': [
        85, 80, 75, 90, 70, 85, 65, 60,
        60, 50, 55, 65, 60
    ],
    'S&P_rating_numeric': [
        100, 98, 95, 100, 85, 95, 80, 85,
        60, 50, 55, 60, 65
    ]
}

df = pd.DataFrame(data)

# ---------------------------
# Step 2: Scorecard weights
# ---------------------------
weights = {
    'GDP_per_capita': 0.3,
    'GDP_growth': 0.2,
    'External_debt_GDP': 0.2,
    'Fiscal_deficit_GDP': 0.2,
    'Governance_score': 0.1
}

# ---------------------------
# Step 3: Normalize data 0-100
# ---------------------------
df['GDP_per_capita_norm'] = (df['GDP_per_capita'] - df['GDP_per_capita'].min()) / (df['GDP_per_capita'].max() - df['GDP_per_capita'].min()) * 100
df['GDP_growth_norm'] = (df['GDP_growth'] - df['GDP_growth'].min()) / (df['GDP_growth'].max() - df['GDP_growth'].min()) * 100
df['External_debt_GDP_norm'] = (df['External_debt_GDP'] - df['External_debt_GDP'].min()) / (df['External_debt_GDP'].max() - df['External_debt_GDP'].min()) * 100
df['Fiscal_deficit_GDP_norm'] = (df['Fiscal_deficit_GDP'] - df['Fiscal_deficit_GDP'].min()) / (df['Fiscal_deficit_GDP'].max() - df['Fiscal_deficit_GDP'].min()) * 100
df['Governance_score_norm'] = (df['Governance_score'] - df['Governance_score'].min()) / (df['Governance_score'].max() - df['Governance_score'].min()) * 100

# ---------------------------
# Step 4: Calculate baseline score
# ---------------------------
df['Baseline_score'] = (
    df['GDP_per_capita_norm'] * weights['GDP_per_capita'] +
    df['GDP_growth_norm'] * weights['GDP_growth'] +
    df['External_debt_GDP_norm'] * weights['External_debt_GDP'] +
    df['Fiscal_deficit_GDP_norm'] * weights['Fiscal_deficit_GDP'] +
    df['Governance_score_norm'] * weights['Governance_score']
)

# ---------------------------
# Step 5: Map score to rating
# ---------------------------
def score_to_rating(score):
    if score >= 90:
        return 'AAA'
    elif score >= 80:
        return 'AA'
    elif score >= 70:
        return 'A'
    elif score >= 60:
        return 'BBB'
    elif score >= 50:
        return 'BB'
    else:
        return 'B'

df['Hypothetical_rating'] = df['Baseline_score'].apply(score_to_rating)

# ---------------------------
# Step 6: Add actual vs projected difference
# ---------------------------
df['Difference'] = df['S&P_rating_numeric'] - df['Baseline_score']

# ---------------------------
# Step 7: Correlation
# ---------------------------
correlation, _ = pearsonr(df['Baseline_score'], df['S&P_rating_numeric'])

# ---------------------------
# Step 8: Output results
# ---------------------------
print(df[['Country', 'Baseline_score', 'Hypothetical_rating', 'S&P_rating_numeric', 'Difference']])
print(f"\nCorrelation between baseline score and actual S&P rating: {correlation:.2f}")