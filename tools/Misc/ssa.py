import numpy as np

start_year = 2023
end_year = 2075
years = end_year - start_year + 1
years_array = np.arange(start_year, end_year + 1)

# Economic assumptions
inflation_rate = 0.023
real_wage_growth = 0.008   # Lower real wage growth (more conservative)
payroll_tax_rate = 0.124   # Statutory rate

# Initial conditions
initial_trust_fund_balance = 2.9e12  # $2.9 trillion
initial_labor_force = 160e6
initial_beneficiaries = 65e6
avg_wage_2023 = 65000
avg_benefit_2023 = 18000

admin_cost_pct = 0.01
improper_payment_rate = 0.0084

def get_fraud_rate(year):
    if year <= 2043:
        return 0.0005 + (0.006 - 0.0005) * (year - 2023) / 20  # Slightly higher start and growth
    else:
        return 0.006

def get_interest_rate(year):
    # Conservative flat rate of 1.75%
    return 0.0175

def get_beneficiary_growth(year):
    # Slightly higher beneficiary growth reflecting aging boomers
    return 0.007 if year < 2040 else 0.002

def get_mortality_rate(year):
    # Slower mortality improvement
    return 0.011 if year < 2040 else 0.009

def get_labor_force_growth(year):
    # Faster labor force decline reflecting demographic shifts
    return 0.001 if year < 2030 else -0.005

def get_effective_payroll_tax_rate(year):
    # Declining effective payroll tax rate due to lower participation and compliance
    if year <= 2050:
        return payroll_tax_rate - (payroll_tax_rate - 0.085) * (year - 2023) / (2050 - 2023)
    else:
        return 0.085

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

# Initial values
trust_fund_balance[0] = initial_trust_fund_balance
labor_force[0] = initial_labor_force
beneficiaries_total[0] = initial_beneficiaries
avg_wage[0] = avg_wage_2023
avg_benefit[0] = avg_benefit_2023

print("Year,PayrollTaxRevenue($B),BenefitOutflow($B),AdminCosts($B),TrustFundBalance($T),Improper($B),Fraud($B),EffectiveTaxRate(%)")

for t in range(1, years):
    year = years_array[t]

    # Wage grows by inflation + real wage growth
    wage_growth_nominal = inflation_rate + real_wage_growth
    avg_wage[t] = avg_wage[t-1] * (1 + wage_growth_nominal)

    # Benefits grow with wage growth (wage-indexed) rather than just inflation
    avg_benefit[t] = avg_benefit[t-1] * (1 + wage_growth_nominal)

    # Update labor force and beneficiaries
    labor_force[t] = labor_force[t-1] * (1 + get_labor_force_growth(year))
    beneficiaries_total[t] = beneficiaries_total[t-1] * (
        1 + get_beneficiary_growth(year) - get_mortality_rate(year)
    )

    # Effective payroll tax rate declines over time (lower participation/compliance)
    effective_tax_rate = get_effective_payroll_tax_rate(year)

    # Payroll tax revenue without wage base cap
    payroll_tax_revenue[t] = avg_wage[t] * labor_force[t] * effective_tax_rate

    # Admin costs
    admin_costs[t] = payroll_tax_revenue[t] * admin_cost_pct

    # Base benefit outflow
    base_outflow = beneficiaries_total[t] * avg_benefit[t]

    # Improper payments and fraud
    improper_amount[t] = base_outflow * improper_payment_rate
    fraud_rate_dynamic = get_fraud_rate(year)
    fraud_amount[t] = base_outflow * fraud_rate_dynamic

    benefit_outflow[t] = base_outflow + improper_amount[t] + fraud_amount[t]

    # Interest on trust fund
    interest = trust_fund_balance[t-1] * get_interest_rate(year)

    # Update trust fund balance
    trust_fund_balance[t] = trust_fund_balance[t-1] + interest + payroll_tax_revenue[t] - benefit_outflow[t] - admin_costs[t]

    print(f"{year},{payroll_tax_revenue[t]/1e9:.2f},{benefit_outflow[t]/1e9:.2f},{admin_costs[t]/1e9:.2f},"
          f"{trust_fund_balance[t]/1e12:.4f},{improper_amount[t]/1e9:.2f},{fraud_amount[t]/1e9:.2f},{effective_tax_rate*100:.3f}")

    if trust_fund_balance[t] <= 0:
        print(f"# Trust fund depleted in {year}")
        break