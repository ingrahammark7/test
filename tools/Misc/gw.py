# === MK-84 Global Inventory Model ===
# - Global stock (today): 150,000 (this is the ONLY pool)
# - Deliveries to any country subtract from the global pool and are capped at what's left (no negatives)
# - Countries then "use" bombs from their own on-hand inventory (country stock)
# - Casualties are estimated from bombs used, using 2–3.5 bombs per casualty
# - Includes a forecast to ZERO (global pool stockout)

from collections import defaultdict, OrderedDict

# ---------------------------
# Config / assumptions
# ---------------------------
GLOBAL_START_STOCK = 150_000
MIN_BOMBS_PER_CASUALTY = 2.0
MAX_BOMBS_PER_CASUALTY = 3.5

# Example monthly plans (edit freely)
# Deliveries: { "Month YYYY": {"Country": amount, ...}, ... }
monthly_deliveries = OrderedDict({
    "October 2024": {"Israel": 5_000},
    "November 2024": {"Israel": 7_000},
    "December 2024": {"Israel": 6_000},
    "January 2025": {"Israel": 10_000},
    "February 2025": {"Israel": 12_000},
    "March 2025": {"Israel": 8_000},
    "April 2025": {"Israel": 7_000},
})

# Usage: bombs dropped by country each month
monthly_usage = OrderedDict({
    "October 2024": {"Israel": 5_000},
    "November 2024": {"Israel": 8_000},
    "December 2024": {"Israel": 7_000},
    "January 2025": {"Israel": 10_000},
    "February 2025": {"Israel": 12_000},
    "March 2025": {"Israel": 8_000},
    "April 2025": {"Israel": 7_000},
})

# ---------------------------
# Core helpers
# ---------------------------

def est_casualties(bombs_used: float) -> tuple[float, float]:
    """Return (min, max) casualties from bombs_used with 2–3.5 bombs per casualty."""
    if MAX_BOMBS_PER_CASUALTY <= 0 or MIN_BOMBS_PER_CASUALTY <= 0:
        return (0.0, 0.0)
    # min casualties uses the less lethal ratio (more bombs per casualty)
    min_est = bombs_used / MAX_BOMBS_PER_CASUALTY
    # max casualties uses the more lethal ratio (fewer bombs per casualty)
    max_est = bombs_used / MIN_BOMBS_PER_CASUALTY
    return min_est, max_est

def safe_deliver(global_left: int, request: int) -> int:
    """Cap delivery at remaining global stock; never negative."""
    if request <= 0 or global_left <= 0:
        return 0
    return min(request, global_left)

def forecast_to_zero(global_left: int, future_monthly_delivery_rate: int) -> int:
    """
    Forecast how many months until the global pool hits ZERO,
    assuming a constant future monthly delivery rate (consumption of the pool).
    Returns the number of months (integer). If rate <= 0, returns 0.
    """
    if future_monthly_delivery_rate <= 0:
        return 0
    months = (global_left + future_monthly_delivery_rate - 1) // future_monthly_delivery_rate
    return months

# ---------------------------
# Simulation
# ---------------------------

def run_simulation(
    deliveries_plan: "OrderedDict[str, dict[str, int]]",
    usage_plan: "OrderedDict[str, dict[str, int]]",
    global_start: int
):
    # State
    global_stock = global_start
    country_stock = defaultdict(int)

    print("Month | Global Start | Delivered | Used | Global End | Est. Casualties (min–max)")
    print("-" * 92)

    total_min_cas = 0.0
    total_max_cas = 0.0

    # Iterate months present in either plan (union, ordered by deliveries_plan first, then remaining usage months)
    months = list(OrderedDict.fromkeys(list(deliveries_plan.keys()) + list(usage_plan.keys())))

    for month in months:
        g_start = global_stock

        # Deliveries for this month
        delivered_total = 0
        for c, req in deliveries_plan.get(month, {}).items():
            grant = safe_deliver(global_stock, int(req))
            if grant > 0:
                global_stock -= grant
                country_stock[c] += grant
                delivered_total += grant

        # Usage (bombs dropped) for this month
        used_total = 0
        for c, used in usage_plan.get(month, {}).items():
            # Country can only use what it has
            take = min(country_stock[c], int(used))
            country_stock[c] -= take
            used_total += take

        # Casualty estimates for this month (from total bombs used)
        min_c, max_c = est_casualties(used_total)
        total_min_cas += min_c
        total_max_cas += max_c

        print(f"{month:12} | {g_start:>12,} | {delivered_total:>9,} | {used_total:>4,} | {global_stock:>10,} | {min_c:>8.0f}–{max_c:>8.0f}")

        if global_stock == 0:
            print("(Global pool exhausted — no further deliveries possible.)")
            # After global stock hits zero, subsequent months can only use remaining country stocks.
            # We continue the loop to reflect that usage could still happen from on-hand.

    print("-" * 92)
    print(f"Totals:                         Delivered={sum(sum(m.values()) for m in deliveries_plan.values()):,} | "
          f"Used={sum(sum(m.values()) for m in usage_plan.values()):,} | Global Remaining={global_stock:,}")
    print(f"Total estimated casualties: {int(total_min_cas):,} – {int(total_max_cas):,}")

    return global_stock, dict(country_stock)

# ---------------------------
# Run with the example plans
# ---------------------------

if __name__ == "__main__":
    final_global, final_country_stocks = run_simulation(
        monthly_deliveries, monthly_usage, GLOBAL_START_STOCK
    )

    # Forecast to ZERO of the global pool assuming a future constant delivery rate
    # (i.e., how many more months of deliveries at this rate until stockout?)
    # We use the average monthly delivery rate from the plan as a sensible default.
    months_count = len(monthly_deliveries) if monthly_deliveries else 0
    avg_future_rate = (
        sum(sum(m.values()) for m in monthly_deliveries.values()) // months_count
        if months_count > 0 else 0
    )

    if final_global > 0 and avg_future_rate > 0:
        months_to_zero = forecast_to_zero(final_global, avg_future_rate)
        print(f"\nForecast to ZERO of global pool at ~{avg_future_rate:,}/month: ~{months_to_zero} months.")
    elif final_global == 0:
        print("\nGlobal pool already at ZERO after the simulated months.")
    else:
        print("\nNo forecast: average future delivery rate is zero (no further draw on the global pool).")