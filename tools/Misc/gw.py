import pandas as pd

# Parameters
years = list(range(2030, 2051))  # 2030 to 2050
revenue_growth = 0.05            # 5% per year
dividend_growth_net = 0.03       # 3% net growth
initial_debt = 100                # B USD in 2030
debt_growth = 30                  # B per year
initial_interest = 5              # B USD in 2030
initial_dividends = 30            # B USD in 2030

# Initialize lists to store results
debt_list = []
interest_list = []
dividend_list = []
total_outflow_list = []

# Starting values
debt = initial_debt
interest = initial_interest
dividends = initial_dividends

for year in years:
    debt_list.append(debt)
    interest_list.append(interest)
    dividend_list.append(dividends)
    total_outflow = interest + dividends
    total_outflow_list.append(total_outflow)

    # Update for next year
    debt += debt_growth
    interest = debt * (initial_interest / initial_debt)  # interest grows proportionally to debt
    dividends *= (1 + dividend_growth_net)

# Create DataFrame
df = pd.DataFrame({
    "Year": years,
    "Debt (B USD)": debt_list,
    "Interest (B USD)": interest_list,
    "Dividends (B USD)": dividend_list,
    "Total Outflow (B USD)": total_outflow_list
})

# Display results
print(df)

# Optional: plot results
import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
plt.plot(df["Year"], df["Debt (B USD)"], label="Debt")
plt.plot(df["Year"], df["Interest (B USD)"], label="Interest")
plt.plot(df["Year"], df["Dividends (B USD)"], label="Dividends")
plt.plot(df["Year"], df["Total Outflow (B USD)"], label="Total Outflow", linestyle="--")
plt.xlabel("Year")
plt.ylabel("Billion USD")
plt.title("Apple Debt, Interest, Dividends, and Total Outflow (2030-2050)")
plt.legend()
plt.grid(True)
plt.show()