def calculate_worker_power(
    total_tonnage_annual,     # total tons moved per year (tons)
    workers,                  # number of workers (persons)
    lifts_per_ton,            # number of lifts per ton moved
    lift_height_meters,       # height of each lift (meters)
    work_hours_per_day,       # active work hours per day
    work_days_per_year        # number of workdays per year
):
    # Constants
    g = 9.81  # m/s^2, gravity
    kg_per_ton = 1000

    # Total lifts per year
    total_lifts = total_tonnage_annual * lifts_per_ton

    # Lifts per worker per year
    lifts_per_worker_year = total_lifts / workers

    # Work per lift (Joules) = m * g * h
    work_per_lift = kg_per_ton * g * lift_height_meters

    # Total work per worker per year (Joules)
    total_work_per_worker_year = lifts_per_worker_year * work_per_lift

    # Total seconds worked per year per worker
    seconds_worked_per_year = work_hours_per_day * 3600 * work_days_per_year

    # Average power per worker during work hours (Watts)
    avg_power_work_hours = total_work_per_worker_year / seconds_worked_per_year

    # Average power per worker over entire year (Watts)
    seconds_per_year = 365 * 24 * 3600
    avg_power_year = total_work_per_worker_year / seconds_per_year

    return {
        "lifts_per_worker_year": lifts_per_worker_year,
        "total_work_per_worker_year_J": total_work_per_worker_year,
        "avg_power_work_hours_W": avg_power_work_hours,
        "avg_power_year_W": avg_power_year
    }

# Example parameters based on your data:
result = calculate_worker_power(
    total_tonnage_annual=20_000_000_000,  # 20 billion tons per year
    workers=1_000_000,                     # 1 million workers
    lifts_per_ton=10,                      # 10 lifts per ton
    lift_height_meters=1,                  # 1 meter lift height
    work_hours_per_day=8,                  # 8 hour work day
    work_days_per_year=250                 # 250 work days per year (approximate)
)

avg=result['avg_power_year_W']

print(f"Lifts per worker per year: {result['lifts_per_worker_year']:.0f}")
print(f"Total work per worker per year (MJ): {result['total_work_per_worker_year_J']/1e6:.2f}")
print(f"Average power per worker during work hours (W): {result['avg_power_work_hours_W']:.2f}")
print(f"Average power per worker over entire year (W): {result['avg_power_year_W']:.2f}")
print("Median worker ", avg*4*3)