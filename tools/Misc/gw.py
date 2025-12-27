# =================== Exact Hebrew Calendar with Numerology Notes ===================

PARTS_PER_HOUR = 1080
PARTS_PER_DAY = 24 * PARTS_PER_HOUR

# Molad Tohu: Monday 5h 204p
MOLAD_TOHU_DAY = 1  # 0=Sunday
MOLAD_TOHU_PARTS = 5 * PARTS_PER_HOUR + 204

# Length of a lunar month in parts
MONTH_PARTS = 29 * PARTS_PER_DAY + 12 * PARTS_PER_HOUR + 793

# ------------------- Core Functions -------------------

def is_leap(year):
    """Return True if the Hebrew year is a leap year in the 19-year cycle"""
    return year % 19 in (0, 3, 6, 8, 11, 14, 17)

def months_elapsed(year):
    """Return total months elapsed since Molad Tohu up to start of given year"""
    y = year - 1
    return 235 * (y // 19) + 12 * (y % 19) + ((7 * (y % 19) + 1) // 19)

def molad_tishrei(year):
    """Return (absolute_day, parts) of molad Tishrei"""
    m = months_elapsed(year)
    total_parts = MOLAD_TOHU_PARTS + m * MONTH_PARTS
    day = MOLAD_TOHU_DAY + total_parts // PARTS_PER_DAY
    parts = total_parts % PARTS_PER_DAY
    return day, parts

def rosh_hashanah_day(year):
    """
    Return absolute day of 1 Tishrei for given year
    Correct deḥiyyot order: Molad Zaken, GaTRaD, BeTuTaKPaT, Lo ADU Rosh
    """
    molad_day, molad_parts = molad_tishrei(year)
    molad_weekday = molad_day % 7  # weekday of molad (0=Sunday)

    day = molad_day

    # 1. Molad Zaken
    if molad_parts >= 18 * PARTS_PER_HOUR:
        day += 1

    # 2. GaTRaD (uses molad weekday)
    if not is_leap(year) and molad_weekday == 2 and molad_parts >= (9 * PARTS_PER_HOUR + 204):
        day += 1

    # 3. BeTuTaKPaT (uses molad weekday)
    if is_leap(year - 1) and molad_weekday == 1 and molad_parts >= (15 * PARTS_PER_HOUR + 589):
        day += 1

    # 4. Lo ADU Rosh (applied last)
    if day % 7 in (0, 3, 5):  # Sunday, Wednesday, Friday
        day += 1

    return day

def year_length(year):
    """Return length of Hebrew year in days"""
    return rosh_hashanah_day(year + 1) - rosh_hashanah_day(year)

def year_type(year):
    """
    Return year type:
        0 = deficient
        1 = regular
        2 = complete
    """
    length = year_length(year)
    if length in (353, 383):
        return 0
    if length in (354, 384):
        return 1
    if length in (355, 385):
        return 2
    raise ValueError(f"Invalid year length {length} for year {year}")

def month_lengths(year):
    """Return list of month lengths from Tishrei to Elul"""
    t = year_type(year)
    leap = is_leap(year)

    if t == 0:
        cheshvan, kislev = 29, 29
    elif t == 1:
        cheshvan, kislev = 29, 30
    else:
        cheshvan, kislev = 30, 30

    months = [
        30,        # Tishrei
        cheshvan,
        kislev,
        29,        # Tevet
        30,        # Shevat
    ]

    if leap:
        months += [30, 29]  # Adar I, Adar II
    else:
        months += [29]      # Adar

    months += [
        30,  # Nisan
        29,  # Iyar
        30,  # Sivan
        29,  # Tammuz
        30,  # Av
        29   # Elul
    ]
    return months

def eighteen_elul_offset(year):
    """Return absolute day of 18 Elul and next Rosh Hashanah"""
    rh_next = rosh_hashanah_day(year + 1)
    elul_len = month_lengths(year)[-1]
    elul_18 = rh_next - (elul_len - 18)
    return elul_18, rh_next

# ------------------- Numerology & Notes -------------------

def rosh_hashanah_diagnostics(year):
    """Return list of notes explaining why a year is numerologically or structurally sensitive"""
    molad_day, molad_parts = molad_tishrei(year)
    molad_weekday = molad_day % 7
    notes = []

    # Thresholds
    zaken = 18 * PARTS_PER_HOUR
    gatrad = 9 * PARTS_PER_HOUR + 204
    betutakpat = 15 * PARTS_PER_HOUR + 589

    def near(x):
        return abs(molad_parts - x) <= PARTS_PER_HOUR

    # Molad Zaken
    if molad_parts >= zaken:
        notes.append("Molad Zaken applied")
    elif near(zaken):
        notes.append("Near Molad Zaken threshold")

    # GaTRaD
    if not is_leap(year) and molad_weekday == 2:
        if molad_parts >= gatrad:
            notes.append("GaTRaD applied")
        elif near(gatrad):
            notes.append("Near GaTRaD threshold")

    # BeTuTaKPaT
    if is_leap(year - 1) and molad_weekday == 1:
        if molad_parts >= betutakpat:
            notes.append("BeTuTaKPaT applied")
        elif near(betutakpat):
            notes.append("Near BeTuTaKPaT threshold")

    # Lo ADU
    rh = rosh_hashanah_day(year)
    if rh % 7 in (0, 3, 5):
        notes.append("Lo ADU Rosh forced shift")

    # Edge-length
    length = year_length(year)
    if length in (353, 355, 383, 385):
        notes.append("Edge-length year")

    return notes

# ------------------- Candidate Years & Output -------------------

def digit_sum(n):
    return sum(int(d) for d in str(n))

WINDOW = 3

# Candidate years 5000–6000 with digit sum 26
candidate_years = [y for y in range(5000, 6001) if digit_sum(y) == 26]

results = []

for y in candidate_years:
    elul18, rh = eighteen_elul_offset(y)
    delta = rh - elul18
    notes = rosh_hashanah_diagnostics(y)

    # Include all notable years
    if 0 <= delta <= WINDOW or notes:
        results.append((y, elul18, rh, delta, notes))

# Print results with annotations
for y, e, r, d, notes in results:
    note_str = "; ".join(notes) if notes else "—"
    print(f"Year {y}: 18 Elul = {e}, RH = {r}, diff = {d} | Notes: {note_str}")
