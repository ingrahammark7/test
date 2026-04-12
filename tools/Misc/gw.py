import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# -------------------------
# Dataset
# -------------------------
data = [
    {"country":"China","steel":550,"cement":1600,"copper":9.5,"aluminum":25,"tallest":632,"supertalls":35,"gdp":18},
    {"country":"USA","steel":320,"cement":300,"copper":8.5,"aluminum":22,"tallest":541,"supertalls":18,"gdp":27},
    {"country":"UAE","steel":450,"cement":900,"copper":10.5,"aluminum":30,"tallest":828,"supertalls":25,"gdp":0.5},
    {"country":"South Korea","steel":950,"cement":800,"copper":12,"aluminum":28,"tallest":555,"supertalls":10,"gdp":1.7},
    {"country":"Germany","steel":400,"cement":500,"copper":9,"aluminum":20,"tallest":300,"supertalls":5,"gdp":4.5},
    {"country":"Japan","steel":600,"cement":700,"copper":11,"aluminum":24,"tallest":330,"supertalls":7,"gdp":4.2},
    {"country":"India","steel":90,"cement":280,"copper":3,"aluminum":4,"tallest":320,"supertalls":3,"gdp":3.7}
]

df = pd.DataFrame(data)

# -------------------------
# Feature engineering
# -------------------------
df["material_index"] = (
    df["steel"] +
    df["cement"] +
    50*df["copper"] +
    20*df["aluminum"]
)

df["skyscraper_index"] = df["tallest"] + 10*df["supertalls"]

# log GDP control
df["log_gdp"] = np.log(df["gdp"])

# -------------------------
# Regression: skyscrapers ~ materials + GDP
# -------------------------
X = df[["material_index","log_gdp"]]
y = df["skyscraper_index"]

model = LinearRegression().fit(X, y)

df["predicted"] = model.predict(X)
df["residual"] = df["skyscraper_index"] - df["predicted"]

# -------------------------
# Outlier detection (z-score on residuals)
# -------------------------
df["residual_z"] = (df["residual"] - df["residual"].mean()) / df["residual"].std()

outliers = df[np.abs(df["residual_z"]) > 1.2]

# -------------------------
# PCA (physical intensity factor)
# -------------------------
X_phys = df[["steel","cement","copper","aluminum"]]
X_scaled = StandardScaler().fit_transform(X_phys)

pca = PCA(n_components=1)
df["physical_factor"] = pca.fit_transform(X_scaled)

print(df[["country","skyscraper_index","material_index","predicted","residual_z"]])
print("\nOutliers:\n", outliers[["country","residual_z"]])