import numpy as np

# Projection years
start_year = 2023
end_year = 2075
years = end_year - start_year + 1
years_array = np.arange(start_year, end_year + 1)

# SSA baseline assumptions
inflation_rate = 0.023
real_wage_growth = 0.011
payroll_tax_rate = 0.124
wage_base_2023 = 160700  # taxable maximum earnings

# Initial values
initial_trust_fund_balance = 2.9e12
initial_labor_force = 160e6
initial_beneficiaries = 65e6
avg_wage_2023 = 65000
avg_benefit_2023 = 18000

# Admin cost (1% of revenue)
admin_cost_pct = 0.01

# Improper payments (fixed)
improper_payment_rate = 0.0084  # 0.84% of outflow

# Dynamic fraud rate (grows to 0.5% by 2043)
def get_fraud_rate(year):
    if year <= 2043:
        return 0.0003 + (0.005 - 0.0003) * (year - 2023) / 20
    else:
        return 0.005

# SSA interest rate assumptions
def get_interest_rate(year):
    if year < 2030:
        return 0.03
    elif year < 2040:
        return 0.035
    else:
        return 0.04

# Beneficiary growth assumptions
def get_beneficiary_growth(year):
    return 0.005 if year < 2040 else 0.001

def get_mortality_rate(year):
    return 0.012 if year < 2040 else 0.008

# Labor force growth
def get_labor_force_growth(year):
    return 0.002 if year < 2030 else -0.003

# Initialize arrays
trust_fund_balance = np.zeros(years)
payroll_tax_revenue = np.zeros(years)
benefit_outflow = np.zeros(years)
admin_costs = np.zeros(years)
labor_force = np.zeros(years)
beneficiaries_total = np.zeros(years)
avg_wage = np.zeros(years)
avg_benefit = np.zeros(years)
fraud_amount = np.zeros(years)
improper_amount = np.zeros(years)

# Initial conditions
trust_fund_balance[0] = initial_trust_fund_balance
labor_force[0] = initial_labor_force
beneficiaries_total[0] = initial_beneficiaries
avg_wage[0] = avg_wage_2023
avg_benefit[0] = avg_benefit_2023

# Print header
print("Year,PayrollTaxRevenue($B),BenefitOutflow($B),AdminCosts($B),TrustFundBalance($T),Improper($B),Fraud($B)")

for t in range(1, years):
    year = years_array[t]

    # Economic adjustments
    wage_growth_nominal = inflation_rate + real_wage_growth
    avg_wage[t] = avg_wage[t-1] * (1 + wage_growth_nominal)
    avg_benefit[t] = avg_benefit[t-1] * (1 + inflation_rate)
    labor_force[t] = labor_force[t-1] * (1 + get_labor_force_growth(year))
    beneficiaries_total[t] = beneficiaries_total[t-1] * (
        1 + get_beneficiary_growth(year) - get_mortality_rate(year)
    )

    # Taxable earnings
    wage_base = wage_base_2023 * (1 + wage_growth_nominal) ** t
    taxable_earnings = min(avg_wage[t], wage_base) * labor_force[t]
    payroll_tax_revenue[t] = taxable_earnings * payroll_tax_rate

    # Admin costs
    admin_costs[t] = payroll_tax_revenue[t] * admin_cost_pct

    # Base outflow and payment errors
    base_outflow = beneficiaries_total[t] * avg_benefit[t]
    improper_amount[t] = base_outflow * improper_payment_rate
    fraud_rate_dynamic = get_fraud_rate(year)
    fraud_amount[t] = base_outflow * fraud_rate_dynamic
    benefit_outflow[t] = base_outflow + improper_amount[t]

    # Trust fund interest
    interest = trust_fund_balance[t-1] * get_interest_rate(year)

    # Update trust fund
    trust_fund_balance[t] = trust_fund_balance[t-1] + interest + payroll_tax_revenue[t] - benefit_outflow[t] - admin_costs[t]

    # Output year result
    print(f"{year},{payroll_tax_revenue[t]/1e9:.2f},{benefit_outflow[t]/1e9:.2f},{admin_costs[t]/1e9:.2f},"
          f"{trust_fund_balance[t]/1e12:.4f},{improper_amount[t]/1e9:.2f},{fraud_amount[t]/1e9:.2f}")

    if trust_fund_balance[t] <= 0:
        print(f"# Trust fund depleted in {year}")
        break