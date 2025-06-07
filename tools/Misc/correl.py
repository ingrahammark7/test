import glob
import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Function to load and combine JSON files matching fe*.json
def load_all_fe_json():
    all_data = []
    for filename in glob.glob("fe*.json"):
        with open(filename, 'r') as f:
            data = json.load(f)
            all_data.extend(data)
    return all_data

data = load_all_fe_json()
df = pd.DataFrame(data)

exclude_vars = ['fertility_rate', 'female_education_years', 'country', 'un_geoscheme']

def residuals(y, X):
    model = LinearRegression().fit(X, y)
    return y - model.predict(X)

print(f"{'Region':<20} {'N':>3} {'Raw Corr':>10} {'Partial Corr':>15}")
print("-"*55)

for region, group in df.groupby('un_geoscheme'):
    if len(group) < 3:
        print(f"{region:<20} {len(group):>3} {'N/A':>10} {'N/A':>15}  (too few samples)")
        continue
    
    y = group['fertility_rate'].values
    x_edu = group['female_education_years'].values
    
    control_vars = [col for col in group.columns if col not in exclude_vars]
    X_controls = group[control_vars].values
    
    corr_raw = np.corrcoef(y, x_edu)[0,1]
    
    y_resid = residuals(y, X_controls)
    x_resid = residuals(x_edu, X_controls)
    corr_partial = np.corrcoef(y_resid, x_resid)[0,1]
    
    print(f"{region:<20} {len(group):>3} {corr_raw:10.4f} {corr_partial:15.4f}")