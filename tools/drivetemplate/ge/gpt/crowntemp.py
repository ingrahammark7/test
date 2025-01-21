import numpy as np

# Constants based on the provided scenario
normal_snow_depth = 16  # normal snow depth in inches
current_snow_depth_in = 7  # current snow depth in inches
current_snow_depth_cm = current_snow_depth_in * 2.54  # convert to cm
temperature_increase_f = 3.1  # temperature increase in Fahrenheit
slope_at_0cm = 1  # slope at 0cm snow depth
slope_at_20cm = 0  # slope at 20cm snow depth

# Calculate the slope at current snow depth (linear interpolation)
slope = slope_at_0cm - (current_snow_depth_cm / 20) * (slope_at_0cm - slope_at_20cm)

# Example of air temperature increase calculation (assuming base temperature is 32°F or 0°C)
base_air_temp_c = 0  # base temperature in Celsius
current_air_temp_c = base_air_temp_c + (temperature_increase_f - 32) * 5 / 9  # converting F to C

# Estimate the crown temperature using the current slope and air temperature
crown_temp_c = current_air_temp_c * slope  # linear relationship

current_air_temp_c, slope, crown_temp_c