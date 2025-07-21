import numpy as np
import matplotlib.pyplot as plt

# === PARAMETERS ===
years = np.arange(2025, 2036)  # inclusive

# Initial population (millions)
total_pop_0 = 43.0
adult_ratio_0 = 0.6
adult_pop_0 = total_pop_0 * adult_ratio_0

# Initial industrial capacity (% of pre-war)
industrial_capacity_0 = 50.0

# Initial drone production (million drones/year)
drone_prod_0 = 2.0

# Decline durations
drone_prod_decline_years = 10  # linear decline to zero by 2035

# Birth and death parameters
birth_rate_0 = 9.0      # per 1000 population per year
birth_rate_decline_rate = 0.02  # 2% annual decline

life_expectancy_0 = 72.0
life_expectancy_final = 60.0

# Annual declines / rates
adult_pop_decline_rate = 0.02       # 2% per year from war casualties, emigration
industrial_capacity_decline_rate = 0.05  # 5% per year degradation

# Migration (million per year, negative = emigration)
migration_start = -0.1   # start small negative
migration_accel = -0.02  # yearly increase in emigration magnitude

# Military aid parameters
military_aid_start = 2025
military_aid_drop_start = 2030
military_aid_decline_rate = 0.20   # 20% drop per year after 2030
military_aid_0 = 1.0               # normalized 1.0 in 2025

# === ARRAYS TO STORE RESULTS ===
N = len(years)
total_pop = np.zeros(N)
adult_pop = np.zeros(N)
industrial_capacity = np.zeros(N)
drone_prod = np.zeros(N)
birth_rate = np.zeros(N)
life_expectancy = np.zeros(N)
migration = np.zeros(N)
military_aid = np.zeros(N)

# === INITIAL VALUES ===
total_pop[0] = total_pop_0
adult_pop[0] = adult_pop_0
industrial_capacity[0] = industrial_capacity_0
drone_prod[0] = drone_prod_0
birth_rate[0] = birth_rate_0
life_expectancy[0] = life_expectancy_0
migration[0] = migration_start
military_aid[0] = military_aid_0

for i in range(1, N):
    year = years[i]

    # --- Military aid ---
    if year < military_aid_drop_start:
        military_aid[i] = military_aid_0
    else:
        years_since_drop = year - military_aid_drop_start + 1
        military_aid[i] = military_aid_0 * ((1 - military_aid_decline_rate) ** years_since_drop)

    # --- Drone production ---
    years_since_start = year - years[0]
    if years_since_start <= drone_prod_decline_years:
        drone_prod[i] = drone_prod_0 * (1 - years_since_start / drone_prod_decline_years)
    else:
        drone_prod[i] = 0.0

    # --- Industrial capacity ---
    industrial_capacity[i] = industrial_capacity[i-1] * (1 - industrial_capacity_decline_rate)
    industrial_capacity[i] = max(industrial_capacity[i], 10)  # assume a minimum baseline remains

    # --- Migration ---
    # Emigration grows in magnitude
    migration[i] = migration[i-1] + migration_accel
    # Clamp max emigration to -0.5 million/year
    migration[i] = max(migration[i], -0.5)

    # --- Birth rate ---
    birth_rate[i] = birth_rate[i-1] * (1 - birth_rate_decline_rate)
    birth_rate[i] = max(birth_rate[i], 5)  # minimum birth rate of 5 per 1000

    # --- Life expectancy ---
    life_expectancy[i] = life_expectancy_0 - ((life_expectancy_0 - life_expectancy_final) / (N-1)) * i

    # --- Adult population ---
    # Adult pop declines by war/emigration + natural aging/replacement
    adult_loss = adult_pop[i-1] * adult_pop_decline_rate
    adult_pop[i] = adult_pop[i-1] - adult_loss

    # Adjust adult pop by net migration (assume mostly adults migrate)
    adult_pop[i] += migration[i]
    adult_pop[i] = max(adult_pop[i], 10)  # floor to avoid negative population

    # --- Total population ---
    # Births
    births = total_pop[i-1] * (birth_rate[i] / 1000)
    # Deaths ~ total_pop / life_expectancy
    deaths = total_pop[i-1] / life_expectancy[i]
    # Migration applies to total pop, approx equal to adult migration
    total_pop[i] = total_pop[i-1] + births - deaths + migration[i]
    total_pop[i] = max(total_pop[i], adult_pop[i])  # total population cannot be less than adults

# === PLOTS ===
plt.figure(figsize=(14, 10))

plt.subplot(3,2,1)
plt.plot(years, total_pop, label='Total Population (M)', color='blue')
plt.plot(years, adult_pop, label='Adult Population (M)', color='navy')
plt.ylabel('Millions')
plt.title('Population')
plt.legend()
plt.grid()

plt.subplot(3,2,2)
plt.plot(years, industrial_capacity, 'orange', label='Industrial Capacity (%)')
plt.plot(years, drone_prod, 'red', label='Drone Production (Million/year)')
plt.ylabel('Percent / Million')
plt.title('Industry & Drones')
plt.legend()
plt.grid()

plt.subplot(3,2,3)
plt.plot(years, birth_rate, 'green', label='Birth Rate (per 1000)')
plt.ylabel('Births per 1000 per year')
plt.title('Birth Rate')
plt.legend()
plt.grid()

plt.subplot(3,2,4)
plt.plot(years, life_expectancy, 'purple', label='Life Expectancy (years)')
plt.ylabel('Years')
plt.title('Life Expectancy')
plt.legend()
plt.grid()

plt.subplot(3,2,5)
plt.plot(years, migration, 'brown', label='Net Migration (Million/year)')
plt.ylabel('Million per year')
plt.title('Migration (mostly emigration)')
plt.legend()
plt.grid()

plt.subplot(3,2,6)
plt.plot(years, military_aid, 'black', label='Military Aid (relative scale)')
plt.ylabel('Relative scale (1=2025)')
plt.title('Military Aid Flow')
plt.legend()
plt.grid()

plt.tight_layout()
plt.suptitle('Ukraine 2025-2035 Collapse Model', fontsize=16, y=1.02)
plt.show()