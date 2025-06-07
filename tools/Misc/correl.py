import glob
import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def country_name_to_flag(country_name, country_code_map=None):
    """
    Convert country name to flag emoji if mapping available.
    country_code_map: dict mapping country name -> ISO2 code.
    Returns flag emoji or empty string.
    """
    if not country_code_map:
        return ''
    iso2 = country_code_map.get(country_name)
    if not iso2 or len(iso2) != 2:
        return ''
    # Unicode Regional Indicator Symbols for flags start at 0x1F1E6
    return chr(0x1F1E6 + ord(iso2[0].upper()) - ord('A')) + chr(0x1F1E6 + ord(iso2[1].upper()) - ord('A'))

# Extended country code map - add as many as needed
country_code_map = {
    "Kenya": "KE",
    "Egypt": "EG",
    "South Africa": "ZA",
    "Ethiopia": "ET",
    "Nigeria": "NG",
    "Brazil": "BR",
    "Canada": "CA",
    "Mexico": "MX",
    "Thailand": "TH",
    "Malaysia": "MY",
    "South Korea": "KR",
    "Japan": "JP",
    "Philippines": "PH",
    "Bangladesh": "BD",
    "India": "IN",
    "Vietnam": "VN",
    "Indonesia": "ID",
    "Poland": "PL",
    "Czech Republic": "CZ",
    "United Kingdom": "GB",
    "Germany": "DE",
    "Sweden": "SE",
    "France": "FR",
    "Netherlands": "NL",
    "Russia": "RU",
}

exclude_vars = ['fertility_rate', 'female_education_years', 'country', 'un_geoscheme']

def residuals(y, X):
    model = LinearRegression().fit(X, y)
    return y - model.predict(X)

def explained_variance(y, X):
    model = LinearRegression().fit(X, y)
    return model.score(X, y)

def analyze_subgroup(subgroup, label):
    n_sub = len(subgroup)
    countries = subgroup['country'].tolist()
    # Deduplicate countries
    unique_countries = []
    seen = set()
    for c in countries:
        if c not in seen:
            unique_countries.append(c)
            seen.add(c)
    # Prepare country list string with optional flags
    countries_with_flags = []
    for c in unique_countries:
        flag = country_name_to_flag(c, country_code_map)
        countries_with_flags.append(f"{flag} {c}" if flag else c)
    countries_str = ", ".join(countries_with_flags)

    print(f" Subgroup: {label} (N={n_sub})")
    print(f"  Countries: {countries_str}")

    if n_sub == 0:
        print("  No data in this subgroup.\n")
        return
    if n_sub < 2:
        print("  Too few samples to analyze reliably.\n")
        return

    y = subgroup['fertility_rate'].values
    x_edu = subgroup['female_education_years'].values
    control_vars = [col for col in subgroup.columns if col not in exclude_vars]
    X_controls = subgroup[control_vars].values if control_vars else np.empty((n_sub, 0))

    try:
        corr_raw = np.corrcoef(y, x_edu)[0,1]
    except Exception:
        corr_raw = np.nan

    if np.isnan(corr_raw):
        corr_raw_str = "nan"
    else:
        corr_raw_str = f"{corr_raw: .4f}"

    if X_controls.shape[1] > 0:
        try:
            y_resid = residuals(y, X_controls)
            x_resid = residuals(x_edu, X_controls)
            corr_partial = np.corrcoef(y_resid, x_resid)[0,1]
        except Exception:
            corr_partial = np.nan
        if np.isnan(corr_partial):
            corr_partial_str = "nan"
        else:
            corr_partial_str = f"{corr_partial: .4f}"
    else:
        corr_partial = corr_raw
        corr_partial_str = corr_raw_str

    try:
        edu_only_var = explained_variance(y, x_edu.reshape(-1,1))
    except Exception:
        edu_only_var = np.nan
    edu_only_var_str = f"{edu_only_var: .4f}" if not np.isnan(edu_only_var) else "nan"

    control_vars_r2 = {}
    for var in control_vars:
        try:
            X_var = subgroup[[var]].values
            r2 = explained_variance(y, X_var)
            control_vars_r2[var] = r2
        except Exception:
            control_vars_r2[var] = np.nan

    top_controls = sorted(control_vars_r2.items(), key=lambda x: (x[1] if not np.isnan(x[1]) else -1), reverse=True)[:3]

    print(f"  Raw correlation (fertility vs education): {corr_raw_str}")
    print(f"  Partial correlation (controlling others): {corr_partial_str}")
    print(f"  Explained variance by education only (R²): {edu_only_var_str}")
    print(f"  Top 3 controls by explained variance (R²):")
    for var, r2 in top_controls:
        r2_str = f"{r2: .4f}" if not np.isnan(r2) else "nan"
        print(f"    - {var}: {r2_str}")

    if n_sub < 6:
        print("  [Note: Small sample size — interpret results with caution]")
    print()

def load_all_fe_json():
    all_data = []
    for filename in glob.glob("fe*.json"):
        with open(filename, 'r') as f:
            data = json.load(f)
            all_data.extend(data)
    return all_data

def main():
    data = load_all_fe_json()
    df = pd.DataFrame(data)

    print(f"Found {len(glob.glob('fe*.json'))} files matching 'fe*.json'.")
    print(f"Loaded {len(df)} total records.\n")

    for region, group in df.groupby('un_geoscheme'):
        n = len(group)
        print("="*40)
        print(f"Region: {region}")
        print(f"Total Sample Size: {n}")

        if n < 2:
            print("Too few samples to analyze.\n")
            continue

        median_fertility = group['fertility_rate'].median()
        lower_fertility = group[group['fertility_rate'] <= median_fertility]
        higher_fertility = group[group['fertility_rate'] > median_fertility]

        analyze_subgroup(lower_fertility, "Lower Fertility")
        analyze_subgroup(higher_fertility, "Higher Fertility")

if __name__ == "__main__":
    main()