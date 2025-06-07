import glob
import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Step 1: Merge all fe*.json files into fe1.json
def merge_fe_json_files():
    all_data = []
    files = glob.glob("fe*.json")
    print(f"Found {len(files)} files matching 'fe*.json'.")
    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.extend(data)
        print(f"Loaded {len(data)} records from {filename}.")
    with open("fe1.json", 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2)
    print(f"Merged data saved to fe1.json, total records: {len(all_data)}")

# Step 2: Load combined data and analyze partial correlations by region
def residuals(y, X):
    model = LinearRegression().fit(X, y)
    return y - model.predict(X)

def analyze_partial_correlation():
    with open("fe1.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    exclude_vars = ['fertility_rate', 'female_education_years', 'country', 'un_geoscheme']

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

if __name__ == "__main__":
    merge_fe_json_files()
    analyze_partial_correlation()