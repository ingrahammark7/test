import pandas as pd

countries = [
    {"Country":"UK","Population":3_500_000,"Pilgrims":60_000},
    {"Country":"Germany","Population":13_500_000,"Pilgrims":270_000},
    {"Country":"France","Population":15_000_000,"Pilgrims":200_000},
    {"Country":"Italy","Population":12_000_000,"Pilgrims":250_000},
    {"Country":"Netherlands","Population":1_500_000,"Pilgrims":50_000},
    {"Country":"Switzerland","Population":1_000_000,"Pilgrims":40_000},
    {"Country":"Spain","Population":7_000_000,"Pilgrims":100_000},
    {"Country":"Poland","Population":5_000_000,"Pilgrims":5_000},
    {"Country":"Austria","Population":3_100_000,"Pilgrims":30_000},
    {"Country":"Hungary","Population":1_500_000,"Pilgrims":5_000},
    {"Country":"Portugal","Population":1_000_000,"Pilgrims":5_000},
    {"Country":"Belgium","Population":800_000,"Pilgrims":8_000},
    {"Country":"Russia","Population":10_000_000,"Pilgrims":2_000},
    {"Country":"Ukraine","Population":4_000_000,"Pilgrims":500},
    {"Country":"Romania","Population":4_000_000,"Pilgrims":500},
    {"Country":"Belarus","Population":1_000_000,"Pilgrims":300},
]

df = pd.DataFrame(countries)

# Tourism GDP
df["Tourism_GDP"] = df["Pilgrims"] * 20_000

# Predicted Notables per Million (scaled to max GDP = 70 per million)
max_gdp = df["Tourism_GDP"].max()
df["Predicted_Notables_Per_Million"] = df["Tourism_GDP"] / max_gdp * 70

# Display console output
print(df[["Country","Population","Pilgrims","Tourism_GDP","Predicted_Notables_Per_Million"]])