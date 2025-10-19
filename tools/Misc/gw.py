from convertdate import hebrew
from datetime import date

def shmita_calendar_correct(start_year, end_year):
    shmita_list = []
    year = start_year
    while year >= end_year:
        # Start of Shmita: 1 Tishrei (month 7, day 1)
        start_greg = hebrew.to_gregorian(year, 7, 1)
        start_date = date(*start_greg)

        # End of Shmita: 29 Elul (month 6, day 29) of the same Hebrew year
        end_greg = hebrew.to_gregorian(year, 6, 29)
        end_date = date(*end_greg)

        shmita_list.append({
            'Jewish Year': year,
            'Start': start_date,
            'End': end_date
        })
        year -= 7
    return list(reversed(shmita_list))

# Generate Shmita years from 5782 back to ~5560 (~1800 CE)
shmita_years = shmita_calendar_correct(5782, 5560)

# Print results
for s in shmita_years:
    print(f"Jewish year {s['Jewish Year']} → {s['Start']} to {s['End']}")