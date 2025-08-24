# === MK-84 Global Inventory Model (Palestine-focused; Yemen declining) ===
# - One global pool (today): 150,000
# - Deliveries subtract from the global pool; capped by what's left (never negative)
# - Countries then "use" bombs from their own on-hand stock
# - Casualties estimated at 2–3.5 bombs per casualty
# - Prints month-by-month table + totals
# - Forecasts months to global ZERO using recent average monthly draw

from collections import defaultdict, OrderedDict

# ---------------------------
# Model constants
# ---------------------------
GLOBAL_START_STOCK = 150_000
MIN_BOMBS_PER_CASUALTY = 2.0
MAX_BOMBS_PER_CASUALTY = 3.5

# ---------------------------
# Scenario (you can edit)
# ---------------------------
# Deliveries: amounts pulled from the global pool and allocated to country stocks.
# Usage: bombs dropped (consumed) from each country's on-hand stock.

monthly_deliveries = OrderedDict({
    # Palestine/Gaza is the primary sink via Israel deliveries
    "Oct 2024": {"Israel/Palestine": 9_000, "Yemen/Saudi-led": 600},
    "Nov 2024": {"Israel/Palestine": 11_000, "Yemen/Saudi-led": 500},
    "Dec 2024": {"Israel/Palestine": 10_000, "Yemen/Saudi-led": 400},
    "Jan 2025": {"Israel/Palestine": 12_000, "Yemen/Saudi-led": 300},
    "Feb 2025": {"Israel/Palestine": 14_000, "Yemen/Saudi-led": 250},
    "Mar 2025": {"Israel/Palestine": 10_000, "Yemen/Saudi-led": 200},
    "Apr 2025": {"Israel/Palestine": 9_000,  "Yemen/Saudi-led": 150},
    "May 2025": {"Israel/Palestine": 9_000,  "Yemen/Saudi-led": 120},
    "Jun 2025": {"Israel/Palestine": 8_500,  "Yemen/Saudi-led": 100},
    "Jul 2025": {"Israel/Palestine": 8_500,  "Yemen/Saudi-led": 80},
    "Aug 2025": {"Israel/Palestine": 8_000,  "Yemen/Saudi-led": 60},
})

monthly_usage = OrderedDict({
    # Usage mirrors intensity: Palestine heavy; Yemen steadily declining
    "Oct 2024": {"Israel/Palestine": 9_000, "Yemen/Saudi-led": 700},
    "Nov 2024": {"Israel/Palestine": 11_500, "Yemen/Saudi-led": 600},
    "Dec 2024": {"Israel/Palestine": 10_000, "Yemen/Saudi-led": 450},
    "Jan 2025": {"Israel/Palestine": 12_000, "Yemen/Saudi-led": 350},
    "Feb 2025": {"Israel/Palestine": 13_500, "Yemen/Saudi-led": 300},
    "Mar 2025": {"Israel/Palestine": 10_000, "Yemen/Saudi-led": 220},
    "Apr 2025": {"Israel/Palestine": 9_000,  "Yemen/Saudi-led": 180},
    "May 2025": {"Israel/Palestine": 9_000,  "Yemen/Saudi-led": 130},
    "Jun 2025": {"Israel/Palestine": 8_500,  "Yemen/Saudi-led": 100},
    "Jul 2025": {"Israel/Palestine": 8_500,  "Yemen/Saudi-led": 80},
    "Aug 2025": {"Israel/Palestine": 8_000,  "Yemen/Saudi-led": 60},
})

# ---------------------------
# Helpers
# ---------------------------

def est_casualties(bombs_used: float) -> tuple[float, float]:
    """Return (min, max) casualties from bombs_used using 2–3.5 bombs per casualty."""
    min_est = bombs_used / MAX_BOMBS_PER_CASUALTY if MAX_BOMBS_PER_CASUALTY > 0 else 0.0
    max_est = bombs_used / MIN_BOMBS_PER_CASUALTY if MIN_BOMBS_PER_CASUALTY > 0 else 0.0
    return min_est, max_est

def cap_delivery(global_left: int, request: int) -> int:
    """Never deliver more than what's left in the global pool; never negative."""
    if request <= 0 or global_left <= 0:
        return 0
    return min(request, global_left)

def avg_monthly_draw(deliveries_plan: OrderedDict) -> int:
    """Average monthly draw on the global pool from the given deliveries plan."""
    if not deliveries_plan:
        return 0
    months = len(deliveries_plan)
    total = sum(sum(month.values()) for month in deliveries_plan.values())
    return total // months if months else 0

def months_to_zero(global_left: int, monthly_draw: int) -> int:
    """How many months to consume 'global_left' at 'monthly_draw' (integer months)."""
    if monthly_draw <= 0:
        return 0
    return (global_left + monthly_draw - 1) // monthly_draw

# ---------------------------
# Simulation
# ---------------------------

def run_sim(deliveries_plan: OrderedDict, usage_plan: OrderedDict, global_start: int):
    global_stock = global_start
    country_stock = defaultdict(int)

    print("Month      | Global Start | Delivered | Used | Global End | Est. Casualties (min–max)")
    print("-" * 96)

    total_min_cas, total_max_cas = 0.0, 0.0

    # Use the union of months (keep the delivery order first, then any extra usage months)
    months = list(OrderedDict.fromkeys(list(deliveries_plan.keys()) + list(usage_plan.keys())))

    for m in months:
        g_start = global_stock

        # 1) Deliveries (pull from the global pool)
        delivered_total = 0
        for country, req in deliveries_plan.get(m, {}).items():
            grant = cap_delivery(global_stock, int(req))
            if grant:
                country_stock[country] += grant
                global_stock -= grant
                delivered_total += grant

        # 2) Usage (consume from country on-hand)
        used_total = 0
        for country, want_to_use in usage_plan.get(m, {}).items():
            take = min(country_stock[country], int(want_to_use))
            country_stock[country] -= take
            used_total += take

        # 3) Casualties estimate (from total used)
        min_c, max_c = est_casualties(used_total)
        total_min_cas += min_c
        total_max_cas += max_c

        print(f"{m:10} | {g_start:>12,} | {delivered_total:>9,} | {used_total:>4,} | "
              f"{global_stock:>10,} | {int(min_c):>7,}–{int(max_c):>7,}")

        if global_stock == 0:
            print("(Global pool exhausted — further deliveries impossible; countries can only draw down remaining on-hand.)")

    print("-" * 96)
    delivered_sum = sum(sum(month.values()) for month in deliveries_plan.values())
    used_sum = sum(sum(month.values()) for month in usage_plan.values())
    print(f"Totals:                          Delivered={delivered_sum:,} | Used={used_sum:,} | Global Remaining={global_stock:,}")
    print(f"Total estimated casualties: {int(total_min_cas):,} – {int(total_max_cas):,}")

    return global_stock, dict(country_stock)

# ---------------------------
# Run the scenario & forecast
# ---------------------------
if __name__ == "__main__":
    final_global, final_country = run_sim(monthly_deliveries, monthly_usage, GLOBAL_START_STOCK)

    # Forecast months to ZERO using recent average monthly draw (deliveries)
    draw = avg_monthly_draw(monthly_deliveries)
    if final_global > 0 and draw > 0:
        m_to_zero = months_to_zero(final_global, draw)
        print(f"\nForecast to ZERO of global pool at ~{draw:,}/month: ~{m_to_zero} months.")
    elif final_global == 0:
        print("\nGlobal pool already at ZERO after the simulated months.")
    else:
        print("\nNo forecast: average monthly draw is zero (no further depletion of the global pool).")