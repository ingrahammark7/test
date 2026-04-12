import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

data = [
    {"country":"China","steel":550,"cement":1600,"copper":9.5,"aluminum":25,"tallest":632,"supertalls":35},
    {"country":"USA","steel":320,"cement":300,"copper":8.5,"aluminum":22,"tallest":541,"supertalls":18},
    {"country":"UAE","steel":450,"cement":900,"copper":10.5,"aluminum":30,"tallest":828,"supertalls":25},
    {"country":"South Korea","steel":950,"cement":800,"copper":12,"aluminum":28,"tallest":555,"supertalls":10},
    {"country":"Germany","steel":400,"cement":500,"copper":9,"aluminum":20,"tallest":300,"supertalls":5},
    {"country":"Japan","steel":600,"cement":700,"copper":11,"aluminum":24,"tallest":330,"supertalls":7},
    {"country":"India","steel":90,"cement":280,"copper":3,"aluminum":4,"tallest":320,"supertalls":3}
]

df = pd.DataFrame(data)

X = df.drop(columns=["country"])
X_scaled = StandardScaler().fit_transform(X)

pca = PCA(n_components=1)
factor = pca.fit_transform(X_scaled)

df["physical_factor"] = factor

corr = df[["physical_factor","tallest","steel","cement","copper","aluminum","supertalls"]].corr()
print(corr)