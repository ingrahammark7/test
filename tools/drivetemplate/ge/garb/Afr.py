import numpy as np
import matplotlib.pyplot as plt

# Initial conditions
initial_refugee_population_2021 = 2_000_000  # 500k refugees in 2021
final_refugee_population_2024 = 8_000_000  # 2 million refugees in 2024
years_to_grow = 3  # From 2021 to 2024
growth_rate = ((final_refugee_population_2024 / initial_refugee_population_2021)-1) / years_to_grow  # Calculate annual growth rate
faster = growth_rate  # Doubling the growth rate after 2024

# Project Africa population growth rate
africa_population_2024 = 1_500_000_000  # approx 1.5 billion in 2024
africa_growth_rate = 0.025  # 2.5% annual growth rate
life_span = 60
mort = 1 / life_span
initial_mort = mort
pyramid_factor = 0.8
tfr = 4.5
tfr_dec = -0.2
tfr_pyramid = 0.25

# Timeframe
years = 50  # From 2021 to 2051

# Lists to store values for each year
refugee_population = [initial_refugee_population_2021]
africa_population = [africa_population_2024]
tfr_values = [tfr]  # List to store TFR values over time
bir_values = []  # List to store birth rate values over time
mort_values = []  # List to store mortality rate values over time

# Simulation loop
for year in range(1, years + 1):
    # Refugee population growth calculation
    if year <= years_to_grow:  # From 2021 to 2024
        new_refugees = refugee_population[-1] * (1 + growth_rate)
    else:  # After 2024, with faster growth
        new_refugees = refugee_population[-1] * (1 + faster) 
    
    refugee_population.append(new_refugees)

    # Update TFR for the year
    tfr = tfr + tfr_dec
    tfr_values.append(tfr)  # Store the TFR value for this year
    
    if year > 7:
        faster = 0  # Stop the fast growth after 2027
    if year > 20:
        refugee_population[-1] = 0  # Assuming no new refugees after 2041
    if tfr < 2:
        tfr_dec = 0  # TFR stabilizes after some point
        tfr=2
    
    # Population Pyramid Adjustments
    gap = (life_span - year) / life_span
    if(year > life_span):
    	gap=0
    pyramid_factor = pyramid_factor * gap
    mort = initial_mort * (1 - pyramid_factor)
    tfr_gap = tfr_pyramid * gap
    bir = tfr / life_span / 2 * (1 - tfr_gap) / (refugee_population[-1] / africa_population[-1] + 1)

    # Track the birth and mortality rates for the graph
    bir_values.append(bir)
    mort_values.append(mort)

    # Africa population growth calculation with decreasing growth rate over time
    africa_growth_rate = bir - mort  # Slight decrease in growth rate per year (reflecting slowing growth)
    new_africa_population = africa_population[-1] * (1 + africa_growth_rate)
    africa_population.append(new_africa_population)

    # Refugee deaths impact (adjusted correctly)
    refugee_deaths = new_refugees * 0.05  # 5% death rate per year
    refugee_population[-1] -= refugee_deaths  # Adjust the refugee population after deaths

    # Adjust Africa population due to refugee deaths
    africa_population_adjusted = africa_population[-1] - refugee_deaths
    africa_population[-1] = africa_population_adjusted  # Update Africa population

# Convert to arrays for easier manipulation
refugee_population = np.array(refugee_population)
africa_population = np.array(africa_population)
tfr_values = np.array(tfr_values)
bir_values = np.array(bir_values)
mort_values = np.array(mort_values)

# Plotting the results
fig, ax = plt.subplots(3, 1, figsize=(12, 18))

# First graph: Refugee and Africa Population
ax[0].plot(range(2021, 2021 + len(refugee_population)), refugee_population, label='Displaced Population', color='orange', linestyle='--')
ax[0].plot(range(2021, 2021 + len(africa_population)), africa_population, label='Africa Population (Projected)', color='blue')
ax[0].set_title("Displaced Population Growth and its Impact on Africa's Population (2021-2051)")
ax[0].set_xlabel("Year")
ax[0].set_ylabel("Population (Billions)")
ax[0].legend()
ax[0].grid(True)

# Second graph: Total Fertility Rate (TFR) over time
ax[1].plot(range(2021, 2021 + len(tfr_values)), tfr_values, label='Total Fertility Rate (TFR)', color='green')
ax[1].set_title("Total Fertility Rate (TFR) Over Time (2021-2051)")
ax[1].set_xlabel("Year")
ax[1].set_ylabel("TFR")
ax[1].legend()
ax[1].grid(True)

# Third graph: Birth Rate (bir) and Mortality Rate (mort) over time
ax[2].plot(range(2021, 2021 + len(bir_values)), bir_values, label='Birth Rate', color='red', linestyle='--')
ax[2].plot(range(2021, 2021 + len(mort_values)), mort_values, label='Mortality Rate', color='purple', linestyle='-')
ax[2].set_title("Birth Rate and Mortality Rate Over Time (2021-2051)")
ax[2].set_xlabel("Year")
ax[2].set_ylabel("Rate")
ax[2].legend()
ax[2].grid(True)

# Show the plots
plt.tight_layout()
plt.show()

# Output the calculated growth rate for reference
growth_rate
