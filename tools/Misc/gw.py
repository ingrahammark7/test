import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns

# -------------------------
# Countries & Initial Data
# -------------------------
countries = [
    "UK","Germany","France","Italy","Netherlands","Switzerland","Spain",
    "Poland","Austria","Hungary","Portugal","Belgium","Russia","Ukraine","Romania","Belarus"
]

# Initial 1500 populations (millions)
pop_1500 = np.array([3.5,13.5,15,12,1.5,1,7,5,3.1,1.5,1,0.8,10,4,4,1])
# Population growth rate per year (0.001–0.01)
growth_rate = np.array([0.006,0.007,0.006,0.005,0.007,0.006,0.005,0.006,0.006,0.006,0.005,0.006,0.007,0.005,0.005,0.004])
# Initial pilgrimage counts
pilgrims_1500 = np.array([60000,270000,200000,250000,50000,40000,100000,5000,30000,5000,5000,8000,2000,500,500,300])

years = np.arange(1500, 1851, 10)  # decades

# -------------------------
# Simulate Population & Pilgrims
# -------------------------
pop_matrix = np.zeros((len(countries), len(years)))
pilgrim_matrix = np.zeros_like(pop_matrix)

for i, (p0, r, pilgrim0) in enumerate(zip(pop_1500, growth_rate, pilgrims_1500)):
    for j, year in enumerate(years):
        t = year - 1500
        pop_matrix[i,j] = p0 * (1 + r) ** t
        pilgrim_matrix[i,j] = pilgrim0 * (1 + 0.002)**t  # slight growth in pilgrimage

# Convert to DataFrame
df_list = []
for i, country in enumerate(countries):
    for j, year in enumerate(years):
        df_list.append({
            "Country": country,
            "Year": year,
            "Population": pop_matrix[i,j],
            "Pilgrims": pilgrim_matrix[i,j]
        })
df_time = pd.DataFrame(df_list)

# -------------------------
# Monte Carlo Simulations
# -------------------------
np.random.seed(42)
simulations = 1000
tourism_gdp_per_pilgrim = 20000

pred_matrix = np.zeros((len(df_time), simulations))

for s in range(simulations):
    # Perturb pilgrim numbers ±10%
    df_time["Pilgrims_sim"] = df_time["Pilgrims"] * np.random.uniform(0.9,1.1,len(df_time))
    df_time["Pilgrims_per_Capita"] = df_time["Pilgrims_sim"] / df_time["Population"]
    df_time["Tourism_Index"] = df_time["Pilgrims_per_Capita"] * tourism_gdp_per_pilgrim
    # Sectoral allocation: Arts 50%, Science 30%, Politics 20%
    df_time["Notable_Arts"] = df_time["Tourism_Index"] * 0.5 / 1000  # scaled per million
    df_time["Notable_Science"] = df_time["Tourism_Index"] * 0.3 / 1000
    df_time["Notable_Politics"] = df_time["Tourism_Index"] * 0.2 / 1000
    # Total Notable per million
    df_time["Notable_Total"] = df_time["Notable_Arts"] + df_time["Notable_Science"] + df_time["Notable_Politics"]
    pred_matrix[:,s] = df_time["Notable_Total"].values

# Compute mean and CI
df_time["Predicted_Mean"] = pred_matrix.mean(axis=1)
df_time["Predicted_Lower"] = np.percentile(pred_matrix, 5, axis=1)
df_time["Predicted_Upper"] = np.percentile(pred_matrix, 95, axis=1)