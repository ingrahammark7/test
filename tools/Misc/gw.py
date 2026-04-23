import numpy as np

# -----------------------------
# 1. Atmospheric energy model
# -----------------------------

def atmospheric_energy_budget(solar_flux=240, efficiency=0.015):
    """
    Solar flux (W/m^2) → kinetic energy in atmosphere
    """
    kinetic_energy_flux = solar_flux * efficiency  # W/m^2
    return kinetic_energy_flux


# -----------------------------
# 2. Jet stream scaling model
# -----------------------------

def jet_stream_speed(temp_gradient=30, coriolis=1e-4):
    """
    Simplified thermal wind scaling.

    u ~ (g/fT) * dT/dy (collapsed constant form)
    We compress constants into a scaling coefficient.
    """

    # empirical scaling constant (tuned to ~30–70 m/s reality)
    k = 1.2

    speed = k * temp_gradient  # m/s

    # physical saturation cap (observed regime limit)
    return min(speed, 75.0)


# -----------------------------
# 3. Aircraft performance model
# -----------------------------

def flight_cycle(climb_rate_fpm=2000,
                  cruise_speed_mph=480,
                  glide_ratio=15,
                  altitude_top=35000,
                  altitude_bottom=5000,
                  distance_miles=500,
                  jet_stream=0):

    # altitude difference
    delta_alt = altitude_top - altitude_bottom

    # climb time
    climb_time = delta_alt / climb_rate_fpm  # minutes

    # descent via glide ratio (air-relative)
    cruise_speed_fpm = cruise_speed_mph * 88
    descent_rate_fpm = cruise_speed_fpm / glide_ratio
    descent_time = delta_alt / descent_rate_fpm

    # cruise time (ground speed affected by jet stream)
    ground_speed = cruise_speed_mph + jet_stream * 2.237  # m/s → mph
    cruise_time = distance_miles / ground_speed * 60

    total_time = climb_time + cruise_time + descent_time

    return {
        "climb_time_min": climb_time,
        "cruise_time_min": cruise_time,
        "descent_time_min": descent_time,
        "total_time_min": total_time,
        "jet_stream_mps": jet_stream,
        "ground_speed_mph": ground_speed
    }


# -----------------------------
# 4. Coupled simulation
# -----------------------------

def simulate(temp_gradient=30):
    """
    Full chain:
    solar → kinetic energy → jet stream → flight cycle
    """

    energy = atmospheric_energy_budget()

    jet = jet_stream_speed(temp_gradient=temp_gradient)

    flight = flight_cycle(jet_stream=jet)

    return {
        "atmospheric_kinetic_flux_Wm2": energy,
        "jet_stream_speed_mps": jet,
        **flight
    }


# -----------------------------
# 5. Run scenarios
# -----------------------------

scenarios = [15, 30, 45, 60, 90]

for tg in scenarios:
    result = simulate(temp_gradient=tg)
    print("\nTEMP GRADIENT:", tg)
    for k, v in result.items():
        print(f"{k}: {v:.2f}")