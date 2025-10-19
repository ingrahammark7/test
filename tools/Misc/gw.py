from convertdate import hebrew
from datetime import date

# Known Shmita year reference
known_shmita_jewish_year = 5782

def shmita_rosh_hashanah_list(start_year, end_year):
    shmita_dates = []
    year = start_year
    while year >= end_year:
        # Rosh Hashanah is 1 Tishrei -> month 7 in convertdate
        g_year, g_month, g_day = hebrew.to_gregorian(year, 7, 1)
        shmita_dates.append((year, date(g_year, g_month, g_day)))
        year -= 7
    return list(reversed(shmita_dates))

# Generate Shmita years back to 1800 CE
# The Jewish year corresponding roughly to 1800 CE is 5560
shmita_years = shmita_rosh_hashanah_list(5782, 5560)

# Print results
for jy, rh_date in shmita_years:
    print(f"Jewish year {jy} → Rosh Hashanah: {rh_date}")