# ===== Exact Hebrew Calendar (Correct Deḥiyyot Order) =====

PARTS_PER_HOUR = 1080
PARTS_PER_DAY = 24 * PARTS_PER_HOUR

# Molad Tohu: Monday 5h 204p
MOLAD_TOHU_DAY = 1  # 0=Sunday
MOLAD_TOHU_PARTS = 5 * PARTS_PER_HOUR + 204

MONTH_PARTS = (
    29 * PARTS_PER_DAY +
    12 * PARTS_PER_HOUR +
    793
)

# Leap year in 19-year cycle
def is_leap(year):
    return year % 19 in (0, 3, 6, 8, 11, 14, 17)

def months_elapsed(year):
    y = year - 1
    return (
        235 * (y // 19) +
        12 * (y % 19) +
        ((7 * (y % 19) + 1) // 19)
    )

def molad_tishrei(year):
    m = months_elapsed(year)
    total_parts = MOLAD_TOHU_PARTS + m * MONTH_PARTS
    day = MOLAD_TOHU_DAY + total_parts // PARTS_PER_DAY
    parts = total_parts % PARTS_PER_DAY
    return day, parts

def rosh_hashanah_day(year):
    day, parts = molad_tishrei(year)

    # 1. Molad Zaken
    if parts >= 18 * PARTS_PER_HOUR:
        day += 1

    weekday = day % 7

    # 2. GaTRaD
    if (
        not is_leap(year) and
        weekday == 2 and  # Tuesday
        parts >= (9 * PARTS_PER_HOUR + 204)
    ):
        day += 1
        weekday = day % 7

    # 3. BeTuTaKPaT
    if (
        is_leap(year - 1) and
        weekday == 1 and  # Monday
        parts >= (15 * PARTS_PER_HOUR + 589)
    ):
        day += 1
        weekday = day % 7

    # 4. Lo ADU Rosh (LAST)
    if weekday in (0, 3, 5):  # Sunday, Wednesday, Friday
        day += 1

    return day

def year_length(year):
    return rosh_hashanah_day(year + 1) - rosh_hashanah_day(year)

def year_type(year):
    length = year_length(year)
    if length in (353, 383):
        return 0  # deficient
    if length in (354, 384):
        return 1  # regular
    if length in (355, 385):
        return 2  # complete
    raise ValueError(f"Invalid year length {length} for year {year}")

def month_lengths(year):
    t = year_type(year)
    leap = is_leap(year)

    if t == 0:
        cheshvan, kislev = 29, 29
    elif t == 1:
        cheshvan, kislev = 29, 30
    else:
        cheshvan, kislev = 30, 30

    months = [
        30,            # Tishrei
        cheshvan,
        kislev,
        29,            # Tevet
        30,            # Shevat
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
    rh_next = rosh_hashanah_day(year + 1)
    elul_len = month_lengths(year)[-1]
    elul_18 = rh_next - (elul_len - 18)
    return elul_18, rh_next

# Utility
def digit_sum(n):
    return sum(map(int, str(n)))

WINDOW = 3

candidate_years = [y for y in range(5000, 6001) if digit_sum(y) == 26]

results = []
for y in candidate_years:
    e18, rh = eighteen_elul_offset(y)
    d = rh - e18
    if 0 <= d <= WINDOW:
        results.append((y, e18, rh, d))

for y, e, r, d in results:
    print(f"Year {y}: 18 Elul = {e}, RH = {r}, diff = {d}")
