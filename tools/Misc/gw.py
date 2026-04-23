def flight_cycle_time_glide(climb_rate_fpm=2000,
                            glide_ratio=15,
                            cruise_speed_mph=480,
                            altitude_top_ft=35000,
                            altitude_bottom_ft=5000,
                            horizontal_distance_miles=100):

    delta_alt = altitude_top_ft - altitude_bottom_ft

    # climb time
    climb_time_min = delta_alt / climb_rate_fpm

    # cruise time
    cruise_time_min = (horizontal_distance_miles / cruise_speed_mph) * 60

    # convert cruise speed to ft/min
    cruise_speed_fpm = cruise_speed_mph * 88

    # glide-based descent rate
    descent_rate_fpm = cruise_speed_fpm / glide_ratio

    descent_time_min = delta_alt / descent_rate_fpm

    total_time = climb_time_min + cruise_time_min + descent_time_min

    return {
        "climb_time_min": climb_time_min,
        "cruise_time_min": cruise_time_min,
        "descent_time_min": descent_time_min,
        "total_time_min": total_time,
        "climb_fraction": climb_time_min / total_time,
        "cruise_fraction": cruise_time_min / total_time,
        "descent_fraction": descent_time_min / total_time,
        "descent_rate_fpm": descent_rate_fpm
    }


result = flight_cycle_time_glide()

for k, v in result.items():
    print(f"{k}: {v:.3f}")