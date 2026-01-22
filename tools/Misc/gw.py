import numpy as np

# Assumptions
total_debt = 40_000_000_000_000  # $40T
short_term_pct = 0.10            # 10% is 6-month debt
short_term_maturity_months = 6
annual_rate = 0.25               # 25% annual
ceiling_margin = 2_000_000_000_000  # $2T margin

# Derived
short_term_debt = total_debt * short_term_pct
monthly_rate = annual_rate / 12

# Simulation
debt = total_debt
month = 0
ceiling_used = 0

while ceiling_used < ceiling_margin:
    month += 1

    # Interest on total debt
    interest = debt * monthly_rate

    # Assume interest is borrowed (added to debt)
    debt += interest
    ceiling_used += interest

    # Rollover short-term debt every 6 months
    if month % short_term_maturity_months == 0:
        # Short-term portion is rolled over
        # (It has already accumulated interest in debt)
        rollover = short_term_debt * (1 + annual_rate/2)
        debt += rollover - short_term_debt
        ceiling_used += rollover - short_term_debt
        short_term_debt = rollover

    if month > 24:  # prevent infinite loop
        break

print(f"Months until ceiling consumed: {month}")
print(f"Debt at that time: ${debt/1e12:.2f}T")
print(f"Ceiling used: ${ceiling_used/1e12:.2f}T")