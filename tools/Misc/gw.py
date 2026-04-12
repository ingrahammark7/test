import pandas as pd

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

# --- Build composite indices ---

df["material_index"] = (
    df["steel"] +
    df["cement"] +
    50*df["copper"] +
    20*df["aluminum"]
)

df["skyscraper_index"] = (
    df["tallest"] +
    10*df["supertalls"]
)

# --- Correlation matrix ---
corr = df.drop(columns=["country"]).corr()

print("Correlation Matrix:\n")
print(corr)

print("\nCorrelation between material_index and skyscraper_index:")
print(df["material_index"].corr(df["skyscraper_index"]))