import numpy as np

start_year = 1980
end_year = 2075
years = end_year - start_year + 1
years_array = np.arange(start_year, end_year + 1)

annual_inflation_rate = 0.035

# Initial values
initial_labor_force = 110e6
initial_beneficiaries = 30e6
initial_trust_fund_balance = 0.5e12  # ~peak late 90s

base_avg_wage_1980 = 12513
base_avg_benefit_1980 = 6000

def get_payroll_tax_rate(year):
    # SSA rates: 11.7% before 1983, then stepped up
    if year < 1983:
        return 0.117
    elif year < 1990:
        return 0.132  # 1983 increase (approx)
    elif year < 2000:
        return 0.142  # 1990 increase
    else:
        return 0.142  # steady since 2000 for simplicity

def adjusted_beneficiary_growth(year):
    # Reflect raised FRA and eligibility changes
    if year < 1983:
        return 0.015
    elif year < 2000:
        return 0.007
    elif year < 2020:
        return 0.003
    else:
        return 0.0

def adjusted_real_benefit_growth(year):
    # Real benefit growth frozen after 2000 (COLA only)
    if year < 2000:
        return 0.01
    else:
        return 0.0

def get_mortality_rate(year):
    if year < 2007:
        return 0.005
    elif year < 2020:
        return 0.01
    else:
        return 0.015

def get_disability_growth(year):
    if year < 2000:
        return 0.002
    elif year < 2020:
        return 0.007
    else:
        return 0.01

def get_ssn_fraud_inflation(year):
    start, peak = 1980, 2025
    min_f, max_f = 0.001, 0.05
    if year < start:
        return min_f
    elif year > peak:
        return max_f
    else:
        return min_f + (max_f - min_f)*(year - start)/(peak - start)

def get_interest_rate(year):
    # Historical SSA trust fund interest rate approximations
    if year < 1990:
        return 0.12
    elif year < 2000:
        return 0.07
    elif year < 2010:
        return 0.04
    elif year < 2020:
        return 0.03
    else:
        return 0.025

def get_claiming_rate(year):
    # Gradual claiming increase from 65% in 1980 to 90% in 2020
    if year < 1980:
        return 0.65
    elif year <= 2020:
        return 0.65 + 0.25 * (year - 1980) / (2020 - 1980)
    else:
        return 0.90

# Labor force growth rates (reflecting baby boom and beyond)
def get_labor_force_growth(year):
    if year < 2000:
        return 0.012
    elif year < 2020:
        return -0.002
    else:
        return -0.005

# Initialize arrays
inflation_index = np.zeros(years)
labor_force = np.zeros(years)
beneficiaries = np.zeros(years)
avg_wage = np.zeros(years)
avg_benefit = np.zeros(years)
trust_fund_balance = np.zeros(years)
payroll_tax_revenue = np.zeros(years)
benefit_outflow = np.zeros(years)

inflation_index[0] = 1.0
labor_force[0] = initial_labor_force
beneficiaries[0] = initial_beneficiaries
avg_wage[0] = base_avg_wage_1980
avg_benefit[0] = base_avg_benefit_1980
trust_fund_balance[0] = initial_trust_fund_balance

print("Year,PayrollTaxRevenue($B),BenefitOutflow($B),TrustFundBalance($T)")

for t in range(1, years):
    year = years_array[t]
    inflation_index[t] = inflation_index[t-1] * (1 + annual_inflation_rate)

    lf_growth = get_labor_force_growth(year)
    ben_growth = adjusted_beneficiary_growth(year)
    real_benefit_growth_rate = adjusted_real_benefit_growth(year)
    mortality_rate = get_mortality_rate(year)
    disability_growth = get_disability_growth(year)
    fraud_inflation = get_ssn_fraud_inflation(year)
    interest_rate = get_interest_rate(year)
    claiming_rate = get_claiming_rate(year)
    payroll_tax_rate = get_payroll_tax_rate(year)

    # Labor force calculation
    labor_force[t] = labor_force[t-1] * (1 + lf_growth)
    mortality_effect = labor_force[t-1] * mortality_rate
    disability_effect = labor_force[t-1] * disability_growth
    labor_force[t] -= (mortality_effect + disability_effect)
    labor_force[t] *= (1 - fraud_inflation)

    # Beneficiary count
    beneficiaries[t] = beneficiaries[t-1] * (1 + ben_growth)

    # Wage & benefit calculations
    avg_wage[t] = base_avg_wage_1980 * inflation_index[t]
    avg_benefit[t] = avg_benefit[t-1] * (1 + annual_inflation_rate + real_benefit_growth_rate)

    # Revenues and payouts
    payroll_tax_revenue[t] = labor_force[t] * avg_wage[t] * payroll_tax_rate
    actual_beneficiaries = beneficiaries[t] * claiming_rate
    benefit_outflow[t] = actual_beneficiaries * avg_benefit[t]

    # Trust fund balance update
    trust_fund_balance[t] = trust_fund_balance[t-1] * (1 + interest_rate) + payroll_tax_revenue[t] - benefit_outflow[t]

    if trust_fund_balance[t] <= 0:
        trust_fund_balance[t:] = 0
        print(f"{year},{payroll_tax_revenue[t]/1e9:.2f},{benefit_outflow[t]/1e9:.2f},{trust_fund_balance[t]/1e12:.4f}")
        print(f"# Trust fund depleted in {year}")
        break

    print(f"{year},{payroll_tax_revenue[t]/1e9:.2f},{benefit_outflow[t]/1e9:.2f},{trust_fund_balance[t]/1e12:.4f}")