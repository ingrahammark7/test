# Define constants for the critical temperature and slope values
critical_crown_temp_c = -12  # Critical crown temperature for winter wheat in Celsius
slope_at_0cm = 1  # Slope at 0cm snow depth (initial)
slope_at_20cm = 0  # Slope at 20cm snow depth (final)
critical_air_temp_c = -32.9  # Air temperature corresponding to critical crown temperature (calculated earlier)
wind_speed_kmh = 30  # Wind speed in km/h for wind chill calculation

# Function to calculate wind chill temperature using the formula
def calculate_wind_chill(temp_celsius, wind_speed):
    return 13.12 + 0.6215 * temp_celsius - 11.37 * (wind_speed ** 0.16) + 0.3965 * temp_celsius * (wind_speed ** 0.16)

# Function to calculate the slope based on snow depth
def calculate_slope(snow_depth_cm):
    return slope_at_0cm - (snow_depth_cm / 20) * (slope_at_0cm - slope_at_20cm)

# Function to calculate the crown temperature considering wind chill
def calculate_crown_temp_with_wind_chill(snow_depth_cm, air_temp_celsius, wind_speed):
    # Calculate the slope for the given snow depth
    slope = calculate_slope(snow_depth_cm)
    
    # Calculate wind chill temperature
    wind_chill_temp_c = calculate_wind_chill(air_temp_celsius, wind_speed)
    
    # Calculate crown temperature considering wind chill
    crown_temp_with_wind_chill_c = wind_chill_temp_c * slope
    return wind_chill_temp_c, crown_temp_with_wind_chill_c

# Update snow depth for the southern Midwest (5 inches)
new_snow_depth_in = 5  # inches
new_snow_depth_cm = new_snow_depth_in * 2.54  # convert to cm

# Calculate the wind chill and crown temperature for the current air temperature and snow depth
wind_chill_temp_c, crown_temp_with_wind_chill_c = calculate_crown_temp_with_wind_chill(new_snow_depth_cm, critical_air_temp_c, wind_speed_kmh)

# Output the results
print(f"Calculated Wind Chill Temperature: {wind_chill_temp_c:.2f} °C")
print(f"Crown Temperature with Wind Chill (Adjusted): {crown_temp_with_wind_chill_c:.2f} °C")

# Check if the crown temperature is below the critical threshold for winter wheat
if crown_temp_with_wind_chill_c < critical_crown_temp_c:
    print("Warning: The crown temperature is below the critical threshold, which could threaten the winter wheat crop.")
else:
    print("The crown temperature is above the critical threshold, the crop is not at immediate risk.")
