# Historical truck estimate for Russia

# US steel production (tons) and percentage used for trucks
us_steel_prod = 5_000_000
pct_truck = 0.3
tons_per_truck = 1

# Calculate trucks produced per year
trucks_per_year = pct_truck * us_steel_prod / tons_per_truck

# Years of production considered
start_year = 1929
end_year = 1937
years = end_year - start_year  # 8 years

# Total trucks produced in the period
total_trucks = trucks_per_year * years

# Fraction sent to Russia
pctrussia = 0.9
russian_trucks = total_trucks * pctrussia
print("In 1937, Russia had trucks:", int(russian_trucks))

# Estimate how many trucks survive today
pct_recycled = 0.4
trucks_today = russian_trucks * pct_recycled
print("Estimated trucks remaining today:", int(trucks_today))

# Lend-Lease trucks contribution
lend_lease_trucks = 300_000
lend_lease_percent = lend_lease_trucks / russian_trucks * 100
print("Lend-Lease contribution as percent of 1937 Russian fleet:", round(lend_lease_percent, 2), "%")