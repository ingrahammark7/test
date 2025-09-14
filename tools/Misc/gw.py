import pandas as pd
import matplotlib.pyplot as plt

# Parameters
years = list(range(2030, 2051))  # 2030 to 2050
revenue_2030 = 400               # B USD in 2030 (example starting revenue)
revenue_growth = 0.05             # 5% per year

dividend_initial = 30             # B USD in 2030
dividend_relative_growth = 0.03   # Net growth relative to revenue

buyback_initial = 110             # B USD in 2030
buyback_relative_growth = 0.03    # Net growth relative to revenue

cash_initial = 80                 # B USD
debt_initial = 100                # B USD
interest_rate_initial = 5 / 100   # interest / debt ratio in 2030

# Lists to store results
revenue_list = []
cash_list = []
debt_list = []
interest_list = []
dividend_list = []
buyback_list = []
total_outflow_list = []

# Initialize values
revenue = revenue_2030
cash = cash_initial
debt = debt_initial
interest = debt_initial * interest_rate_initial
dividends = dividend_initial
buybacks = buyback_initial

for year in years:
    # Record values
    revenue_list.append(revenue)
    cash_list.append(cash)
    debt_list.append(debt)
    interest_list.append(interest)
    dividend_list.append(dividends)
    buyback_list.append(buybacks)
    total_outflow_list.append(interest + dividends + buybacks)
    
    # Calculate cash after obligations
    cash -= (dividends + buybacks)
    if cash < 0:
        # Use debt to cover shortfall
        debt_needed = -cash
        debt += debt_needed
        cash = 0
    
    # Update revenue
    revenue *= (1 + revenue_growth)
    
    # Update dividends and buybacks relative to revenue
    dividends *= (1 + revenue_growth) * (1 + dividend_relative_growth)
    buybacks *= (1 + revenue_growth) * (1 + buyback_relative_growth)
    
    # Update interest proportional to debt
    interest = debt * interest_rate_initial

# Create DataFrame
df = pd.DataFrame({
    "Year": years,
    "Revenue (B USD)": revenue_list,
    "Cash (B USD)": cash_list,
    "Debt (B USD)": debt_list,
    "Interest (B USD)": interest_list,
    "Dividends (B USD)": dividend_list,
    "Buybacks (B USD)": buyback_list,
    "Total Outflow (B USD)": total_outflow_list
})

print(df)

# Plot
plt.figure(figsize=(14,7))
plt.plot(df["Year"], df["Cash (B USD)"], label="Cash")
plt.plot(df["Year"], df["Debt (B USD)"], label="Debt")
plt.plot(df["Year"], df["Interest (B USD)"], label="Interest")
plt.plot(df["Year"], df["Dividends (B USD)"], label="Dividends")
plt.plot(df["Year"], df["Buybacks (B USD)"], label="Buybacks")
plt.plot(df["Year"], df["Revenue (B USD)"], label="Revenue", linestyle="--", color="black")
plt.axhline(y=80, color='red', linestyle='--', label="80B Cash Threshold")

plt.xlabel("Year")
plt.ylabel("Billion USD")
plt.title("Apple Cash, Debt, Dividends, Buybacks vs Revenue (Relative Growth 2030-2050)")
plt.legend()
plt.grid(True)
plt.show()