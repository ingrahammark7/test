import numpy as np
import matplotlib.pyplot as plt

# Initial conditions
initial_refugee_population_2021 = 2_000_000  # 500k refugees in 2021
final_refugee_population_2024 = 8_000_000  # 2 million refugees in 2024
# 4x for IDPs (Internally Displaced Persons)
years_to_grow = 3  # From 2021 to 2024
growth_rate = ((final_refugee_population_2024 / initial_refugee_population_2021)-1) / years_to_grow  # Calculate annual growth rate
faster = growth_rate  # Doubling the growth rate after 2024

# Project Africa population growth rate
africa_population_2024 = 1_500_000_000  # approx 1.5 billion in 2024
africa_growth_rate = 0.025  # 2.5% annual growth rate
life_span=60
mort=1/life_span
pyramid_factor=0.8
tfr=4.5
tfr_dec=-.2
tfr_pyramid=0.25

# Timeframe
years = 30  # From 2021 to 2051

# Lists to store values for each year
refugee_population = [initial_refugee_population_2021]
africa_population = [africa_population_2024]

# Simulation loop
for year in range(1, years + 1):
    # Refugee population growth calculation
    if year <= years_to_grow:  # From 2021 to 2024
        new_refugees = refugee_population[-1] * (1 + growth_rate)
    else:  # After 2024, with faster growth
        new_refugees = refugee_population[-1] * (1 + faster) 
    
    refugee_population.append(new_refugees)
    tfr=tfr+tfr_dec
    if year > 7:
    	faster =0
    if year > 20:
    		refugee_population[-1]=0
    		tfr_dec=0
    gap=(life_span-year)/life_span
    pyramid_factor=pyramid_factor*gap
    mort=mort*(1-pyramid_factor)
    tfr_gap=tfr_pyramid*gap
    bir=tfr/life_span/2*(1-tfr_gap)/(refugee_population[-1]/africa_population[-1]+1)
    # Africa population growth calculation with decreasing growth rate over time
    africa_growth_rate=bir-mort  # Slight decrease in growth rate per year (reflecting slowing growth)
    new_africa_population = africa_population[-1] * (1 + africa_growth_rate)
    africa_population.append(new_africa_population)
    
    # Refugee deaths impact
    refugee_deaths = new_refugees * 0.05  # 5% death rate per year
    africa_population_adjusted = africa_population[-1] - refugee_deaths
    africa_population[-1] = africa_population_adjusted  # Adjust Africa population after refugee deaths

# Convert to arrays for easier manipulation
refugee_population = np.array(refugee_population)
africa_population = np.array(africa_population)

# Plotting the results
plt.figure(figsize=(12, 8))
plt.plot(range(2021, 2021 + len(refugee_population)), refugee_population, label='Displaced Population', color='orange', linestyle='--')
plt.plot(range(2021, 2021 + len(africa_population)), africa_population, label='Africa Population (Projected)', color='blue')
plt.title("Displaced Population Growth and its Impact on Africa's Population (2021-2051)")
plt.xlabel("Year")
plt.ylabel("Population billion")
plt.legend()
plt.grid(True)
plt.show()

# Output the calculated growth rate for reference
growth_rate
