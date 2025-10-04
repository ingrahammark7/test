#!/usr/bin/env python3
"""
wheat_model.py

Simple CLI model for U.S. 2025/26 wheat supply/use that:
 - uses USDA/ERS 2025/26 numbers (defaults)
 - treats losses as % of production (harvest)
 - distributes harvest and loss over harvest months (Aug–Nov)
 - computes monthly depletion from use + losses and prints a simple table

Default data source: USDA ERS Wheat Outlook, Sept 16, 2025 (see comments / citation).
"""

import argparse
from typing import List

# ---------------------------
# Default 2025/26 U.S. wheat supply/use (million bushels)
# Source: USDA ERS Wheat Outlook: September 16, 2025, Table 1.
# Beginning stocks: 851
# Production:        1,927
# Imports:            120
# Supply total:      2,898
# Food:                972
# Seed:                 62
# Feed & residual:     120
# Domestic total:    1,154
# Exports:             900
# Use total:         2,054
# Ending stocks:       844
# (million bushels)
# ---------------------------

DEFAULTS = {
    "beginning_stocks": 851.0,
    "production": 1927.0,
    "imports": 120.0,
    "domestic_use": 1154.0,
    "exports": 900.0,
    "use_total": 2054.0,
    "ending_stocks": 844.0,
}

MONTHS = [
    "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
    "Dec", "Jan", "Feb", "Mar", "Apr", "May"
]

# ---------------------------
# Utility functions
# ---------------------------

def evenly_distribute_total(total: float, months: int = 12) -> List[float]:
    """Evenly distribute a total value across all months."""
    return [total / months] * months

def parse_monthly_override(s: str) -> List[float]:
    """Parse comma-separated 12 numbers into list."""
    parts = [p.strip() for p in s.split(",")]
    if len(parts) != 12:
        raise argparse.ArgumentTypeError("Must have 12 comma-separated monthly values (Jun→May).")
    try:
        return [float(p) for p in parts]
    except ValueError:
        raise argparse.ArgumentTypeError("All monthly override values must be numeric.")

# ---------------------------
# Core model
# ---------------------------

def run_model(begin_stocks_mbu: float,
              production_mbu: float,
              imports_mbu: float,
              domestic_use_mbu: float,
              exports_mbu: float,
              loss_rate_pct_of_harvest: float,
              monthly_stock_override: List[float] = None,
              show_monthly: bool = True):
    """
    Core model using losses = % of production (harvest), applied to harvest months.

    - loss_rate_pct_of_harvest: percent (e.g. 1.0 means 1% of total harvest lost)
    - monthly_stock_override: optional list of 12 monthly starting stock values (million bu)
    """

    months = 12
    loss_fraction = loss_rate_pct_of_harvest / 100.0

    # ---------------------------
    # Inflows setup
    # ---------------------------
    monthly_inflows = [0.0] * months
    monthly_inflows[0] += begin_stocks_mbu  # beginning stocks in June

    # Harvest receipts pattern: Aug–Nov = 10%, 50%, 30%, 10%
    prod_pattern = [0, 0.10, 0.50, 0.30, 0.10]
    prod_month_indices = [2, 3, 4, 5]  # Aug, Sep, Oct, Nov

    for share, idx in zip(prod_pattern[1:], prod_month_indices):
        monthly_inflows[idx] += production_mbu * share

    # Imports evenly spread across the year
    monthly_imports = evenly_distribute_total(imports_mbu, months)
    for i in range(months):
        monthly_inflows[i] += monthly_imports[i]

    # ---------------------------
    # Losses (percent of harvest)
    # ---------------------------
    total_loss = production_mbu * loss_fraction
    monthly_losses = [0.0] * months
    total_prod_inflow = sum(monthly_inflows[i] for i in prod_month_indices)
    if total_prod_inflow > 0:
        for i in prod_month_indices:
            share = monthly_inflows[i] / total_prod_inflow
            monthly_losses[i] = total_loss * share

    # ---------------------------
    # Uses
    # ---------------------------
    monthly_domestic = evenly_distribute_total(domestic_use_mbu, months)
    monthly_exports = evenly_distribute_total(exports_mbu, months)

    # ---------------------------
    # Simulation
    # ---------------------------
    table = []
    on_hand = begin_stocks_mbu

    for i, month_name in enumerate(MONTHS):
        inflow = monthly_inflows[i] if i != 0 else 0.0  # June already includes beginning
        beginning = on_hand
        on_hand += inflow

        month_dom = monthly_domestic[i]
        month_exp = monthly_exports[i]
        month_loss = monthly_losses[i]

        ending = max(on_hand - month_dom - month_exp - month_loss, 0.0)
        table.append({
            "month": month_name,
            "beginning": beginning,
            "inflow": inflow,
            "use_domestic": month_dom,
            "use_exports": month_exp,
            "loss": month_loss,
            "ending": ending
        })
        on_hand = ending

    # ---------------------------
    # Summaries
    # ---------------------------
    final_ending = table[-1]["ending"]
    total_losses_modeled = sum(r["loss"] for r in table)
    total_use_modeled = sum(r["use_domestic"] + r["use_exports"] for r in table)
    total_inflows_modeled = sum(r["inflow"] for r in table) + begin_stocks_mbu

    # ---------------------------
    # Output
    # ---------------------------
    if show_monthly:
        print("\nMonthly projection (million bushels):")
        header = f"{'Month':>5} | {'Begin':>10} | {'Inflow':>10} | {'DomUse':>9} | {'Exports':>8} | {'Loss':>9} | {'End':>10}"
        print(header)
        print("-" * len(header))
        for r in table:
            print(f"{r['month']:>5} | {r['beginning']:10,.1f} | {r['inflow']:10,.1f} | "
                  f"{r['use_domestic']:9,.1f} | {r['use_exports']:8,.1f} | "
                  f"{r['loss']:9,.1f} | {r['ending']:10,.1f}")

    print("\nSummary (million bushels):")
    print(f"  Total inflows (beginning + production + imports): {total_inflows_modeled:,.1f}")
    print(f"  Total modeled use (domestic + exports):           {total_use_modeled:,.1f}")
    print(f"  Total harvest losses (@ {loss_rate_pct_of_harvest}% of production): {total_losses_modeled:,.1f}")
    print(f"  Modeled ending stocks (May):                     {final_ending:,.1f}")
    print(f"\nNote: USDA reported ending stocks for 2025/26: {DEFAULTS['ending_stocks']:.1f} M bu (ERS Sep 2025).")
    print("Model assumes deterministic inflow/use/loss patterns for simplicity.")

# ---------------------------
# CLI interface
# ---------------------------

def main():
    parser = argparse.ArgumentParser(description="Simple U.S. wheat stocks/use monthly model (2025/26 defaults).")
    parser.add_argument("--begin", type=float, default=DEFAULTS["beginning_stocks"],
                        help=f"Beginning stocks (M bu). Default {DEFAULTS['beginning_stocks']}")
    parser.add_argument("--prod", type=float, default=DEFAULTS["production"],
                        help=f"Production (M bu). Default {DEFAULTS['production']}")
    parser.add_argument("--imp", type=float, default=DEFAULTS["imports"],
                        help=f"Imports (M bu). Default {DEFAULTS['imports']}")
    parser.add_argument("--dom", type=float, default=DEFAULTS["domestic_use"],
                        help=f"Domestic use (M bu). Default {DEFAULTS['domestic_use']}")
    parser.add_argument("--exp", type=float, default=DEFAULTS["exports"],
                        help=f"Exports (M bu). Default {DEFAULTS['exports']}")
    parser.add_argument("--loss", type=float, default=70.0,
                        help="Loss rate as percent of harvest (e.g., 1.0 = 1% of production lost). Default 1.0")
    parser.add_argument("--monthly-override", type=parse_monthly_override, default=None,
                        help="Optional comma-separated 12 monthly starting stock values (M bu, Jun→May).")
    args = parser.parse_args()

    run_model(begin_stocks_mbu=args.begin,
              production_mbu=args.prod,
              imports_mbu=args.imp,
              domestic_use_mbu=args.dom,
              exports_mbu=args.exp,
              loss_rate_pct_of_harvest=args.loss,
              monthly_stock_override=args.monthly_override,
              show_monthly=True)

# ---------------------------

if __name__ == "__main__":
    main()