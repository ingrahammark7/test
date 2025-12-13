import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# -----------------------------
# State list
# -----------------------------
states = [
    "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut",
    "Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa",
    "Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan",
    "Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada",
    "New Hampshire","New Jersey","New Mexico","New York","North Carolina",
    "North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island",
    "South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont",
    "Virginia","Washington","West Virginia","Wisconsin","Wyoming"
]

df = pd.DataFrame({"State": states})

# -----------------------------
# Predictors
# -----------------------------
df["Population_Density"] = [
    97,1,64,58,253,57,741,500,414,190,222,23,232,189,57,36,113,108,43,626,
    884,177,72,63,89,7,25,29,153,1210,412,420,218,11,286,57,44,286,1021,
    170,12,170,115,40,68,218,117,77,108,6
]

df["Pct_Hispanic"] = [
    .05,.07,.31,.08,.40,.22,.17,.10,.27,.10,.11,.13,.19,.09,.07,.13,.04,.05,
    .02,.11,.22,.06,.06,.03,.04,.11,.11,.30,.04,.22,.49,.20,.11,.04,.05,
    .11,.14,.08,.17,.06,.04,.06,.39,.15,.02,.10,.14,.13,.07,.10
]

df["ICE_Cooperation_Index"] = [
    .9,.6,.8,.8,.2,.4,.3,.4,.8,.9,.3,.7,.3,.6,.5,.6,.7,.9,.4,.4,
    .3,.4,.4,.9,.6,.6,.6,.5,.3,.3,.4,.3,.6,.6,.5,.7,.3,.5,.3,
    .8,.7,.9,.8,.6,.2,.4,.3,.8,.4,.6
]

df["Border_State"] = df["State"].isin(
    ["California","Arizona","New Mexico","Texas"]
).astype(int)

df["Sanctuary_State"] = df["State"].isin(
    ["California","New York","Illinois","Oregon","Washington","New Jersey","Colorado"]
).astype(int)

df["Deep_South"] = df["State"].isin(
    ["Alabama","Mississippi","Louisiana","Tennessee","Georgia","South Carolina"]
).astype(int)

# -----------------------------
# Outcome: independent enforcement index (proxy for per-Hispanic deportation)
# -----------------------------
df["Enforcement_Index"] = [
    0.78,0.30,0.65,0.60,0.25,0.40,0.32,0.35,0.70,0.72,0.33,0.55,0.30,0.45,
    0.40,0.50,0.48,0.80,0.35,0.42,0.33,0.38,0.36,0.82,0.50,0.28,0.45,0.55,
    0.32,0.30,0.62,0.28,0.55,0.30,0.45,0.58,0.27,0.47,0.34,0.75,0.30,
    0.77,0.70,0.52,0.25,0.48,0.27,0.60,0.42,0.35
]

# -----------------------------
# Regression
# -----------------------------
X = df[
    ["Population_Density","Pct_Hispanic","ICE_Cooperation_Index",
     "Border_State","Sanctuary_State","Deep_South"]
]
y = df["Enforcement_Index"]

model = LinearRegression()
model.fit(X, y)

df["Predicted"] = model.predict(X)
df["Residual"] = y - df["Predicted"]

r2 = r2_score(y, df["Predicted"])

# -----------------------------
# Ranking
# -----------------------------
ranked = df.sort_values("Enforcement_Index", ascending=False)

print("\n=== TOP 15 STATES: ACTUAL vs PREDICTED ===")
print(ranked.head(15)[[
    "State","Enforcement_Index","Predicted","Residual"
]])

print("\n=== MODEL COEFFICIENTS ===")
for name, coef in zip(X.columns, model.coef_):
    print(f"{name}: {coef:.4f}")
print(f"Intercept: {model.intercept_:.4f}")
print(f"R²: {r2:.3f}")

print("""
Interpretation:
• Positive residual → state enforces more than model predicts
• Negative residual → state enforces less
• Coefficients show which predictors increase/decrease expected intensity
""")