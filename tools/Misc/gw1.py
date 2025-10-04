#!/usr/bin/env python3
"""
wheat_model.py

Simple CLI model for U.S. 2025/26 wheat supply/use that:
 - uses USDA/ERS 2025/26 numbers (defaults)
 - allows a loss-rate projection (percent per month)
 - allows specifying monthly starting stocks (or auto-spreads)
 - computes monthly depletion from use + losses and prints a simple table

Default data source: USDA ERS Wheat Outlook, Sept 16, 2025 (see comments / citation).
"""

import argparse
import math
from typing import List

# ---------------------------
# Default real 2025/26 numbers (US, million bushels) from USDA ERS Wheat Outlook Sep 2025.
# Source: USDA ERS Wheat Outlook: September 16, 2025, Table 1 (U.S. wheat supply and use).
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
# (Numbers are in million bushels). Citation: USDA ERS (WHS-25i) Sep 16, 2025. 1
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

def evenly_distribute_total(total: float, months: int = 12) -> List[float]:
    """Even spread total across months (simple)."""
    base = total / months
    return [base] * months

def pretty_millions(x):
    """Format million-bushels number with one decimal and 'M bu' suffix."""
    return f"{x:10,.1f} M bu"

def run_model(begin_stocks_mbu: float,
              production_mbu: float,
              imports_mbu: float,
              domestic_use_mbu: float,
              exports_mbu: float,
              loss_rate_pct_per_month: float,
              monthly_stock_override: List[float] = None,
              show_monthly: bool = True):
    """
    Core modeling function.

    - loss_rate_pct_per_month: percent (e.g. 0.5 -> 0.5% per month lost to storage/other losses)
    - monthly_stock_override: optional list of 12 monthly starting stock values (million bu).
      If None, the program will place beginning stocks in June and add production
      in months typical for marketing-year receipts (default: distribute production into Sep-Oct).
    """
    # Prepare monthly starting stocks (millions bu)
    months = 12
    loss_rate = loss_rate_pct_per_month / 100.0

    # Build monthly supply inflows:
    # Place beginning stocks in month 0 (June).
    # Distribute production receipts: for simplicity, assume harvest receipts mostly in Sep-Oct (split).
    monthly_inflows = [0.0] * months
    monthly_inflows[0] += begin_stocks_mbu  # beginning stocks in June
    # simple receipt pattern: 10% Aug, 50% Sep, 30% Oct, 10% Nov
    prod_pattern = [0, 0.10, 0.50, 0.30, 0.10]  # relative to production across months Aug-Nov (indexing logic below)
    # map pattern to months: Aug(index=2), Sep(3), Oct(4), Nov(5) — but for simplicity use indexes 2..5
    prod_month_indices = [2, 3, 4, 5]  # Aug, Sep, Oct, Nov
    for share, idx in zip(prod_pattern[1:], prod_month_indices):
        monthly_inflows[idx] += production_mbu * share
    # any leftover (if pattern doesn't sum to 1) put remainder into Sep
    leftover = production_mbu * (1.0 - sum(prod_pattern[1:]))
    if leftover != 0:
        monthly_inflows[3] += leftover  # add to Sep

    # Imports: evenly spread
    monthly_imports = evenly_distribute_total(imports_mbu, months)
    for i in range(months):
        monthly_inflows[i] += monthly_imports[i]

    # Monthly 'use' split between domestic and exports:
    monthly_domestic = evenly_distribute_total(domestic_use_mbu, months)
    monthly_exports = evenly_distribute_total(exports_mbu, months)

    # Optionally override monthly starting stock
    if monthly_stock_override:
        if len(monthly_stock_override) != months:
            raise ValueError("monthly_stock_override must contain 12 values (one per month).")
        # If overridden, use these as starting stocks for each month instead of our inflow-based assumption.
        # We'll still treat production/imports as inflows which add to the overridden starting stock.
        starting_stocks = [monthly_stock_override[i] for i in range(months)]
        # We'll still include inflows as additions at start-of-month:
        for i in range(months):
            starting_stocks[i] += monthly_imports[i]  # imports considered part of that month's on-hand
    else:
        # derive starting stocks as cumulative inflows placed into months before uses
        # We'll simulate month-by-month.
        starting_stocks = [0.0] * months
        running_on_hand = 0.0
        for i in range(months):
            running_on_hand += monthly_inflows[i]
            starting_stocks[i] = running_on_hand

            # subtract use & losses at end of month to prepare for next month's starting_on_hand
            month_use = monthly_domestic[i] + monthly_exports[i]
            month_losses = running_on_hand * loss_rate  # losses applied to on-hand during month
            running_on_hand = max(running_on_hand - month_use - month_losses, 0.0)

    # If no override we already simulated running_on_hand to represent end-of-month carry
    # For explicit monthly table, we should re-simulate to show per-month beginning, inflows, loss, use, ending.
    table = []
    on_hand = 0.0
    if monthly_stock_override:
        # start with overridden beginning stocks in month 0 (June)
        on_hand = monthly_stock_override[0] + monthly_imports[0] + monthly_inflows[0] - monthly_imports[0]
        # but simpler: set on_hand = starting_stocks[0]
        on_hand = starting_stocks[0]
    else:
        on_hand = begin_stocks_mbu  # begin stocks as given in June

    # For months, we'll add production receipts and imports as we had in monthly_inflows
    for i in range(months):
        month_name = MONTHS[i]
        inflow = monthly_inflows[i] if not monthly_stock_override else (monthly_inflows[i])  # always include inflows
        beginning = on_hand
        on_hand += inflow if i != 0 else (inflow if monthly_stock_override else 0.0)  # for month 0 we already added beginning stocks
        month_dom = monthly_domestic[i]
        month_exp = monthly_exports[i]
        month_use = month_dom + month_exp
        month_loss = on_hand * loss_rate
        ending = max(on_hand - month_use - month_loss, 0.0)
        table.append({
            "month": month_name,
            "beginning": beginning,
            "inflow": inflow,
            "use_domestic": month_dom,
            "use_exports": month_exp,
            "loss": month_loss,
            "ending": ending
        })
        # next month starting on_hand:
        on_hand = ending

    # Summaries
    final_ending = table[-1]["ending"]
    total_use_modeled = sum(r["use_domestic"] + r["use_exports"] for r in table)
    total_losses_modeled = sum(r["loss"] for r in table)
    total_inflows_modeled = sum(r["inflow"] for r in table) + (begin_stocks_mbu if not monthly_stock_override else 0.0)

    # Print nicely
    if show_monthly:
        print("\nMonthly projection (million bushels):")
        header = f"{'Month':>5} | {'Begin':>10} | {'Inflow':>10} | {'DomUse':>9} | {'Exports':>8} | {'Loss':>9} | {'End':>10}"
        print(header)
        print("-" * len(header))
        for r in table:
            print(f"{r['month']:>5} | {r['beginning']:10,.1f} | {r['inflow']:10,.1f} | {r['use_domestic']:9,.1f} | "
                  f"{r['use_exports']:8,.1f} | {r['loss']:9,.1f} | {r['ending']:10,.1f}")

    print("\nSummary (million bushels):")
    print(f"  Total inflows considered (incl. production receipts & imports + beginning): {total_inflows_modeled:,.1f}")
    print(f"  Total modeled use (domestic + exports):                                      {total_use_modeled:,.1f}")
    print(f"  Total modeled losses (applied monthly @ {loss_rate_pct_per_month}%/month):    {total_losses_modeled:,.1f}")
    print(f"  Modeled ending stocks (May, end of marketing year):                          {final_ending:,.1f}")
    print(f"\nNote: USDA reported ending stocks for 2025/26 (million bushels): {DEFAULTS['ending_stocks']:.1f} (Sept 2025 ERS).")
    print("Model is deterministic and uses a simple receipt/use split. Adjust loss rate or provide monthly override for custom scenarios.")

def parse_monthly_override(s: str) -> List[float]:
    """
    Parse comma-separated 12 numbers into list.
    e.g. "80,80,80,..."
    """
    parts = [p.strip() for p in s.split(",")]
    if len(parts) != 12:
        raise argparse.ArgumentTypeError("monthly override must contain 12 comma-separated numbers (one per month Jun->May).")
    vals = []
    for p in parts:
        try:
            vals.append(float(p))
        except:
            raise argparse.ArgumentTypeError("monthly override values must be numeric.")
    return vals

def main():
    parser = argparse.ArgumentParser(description="Simple winter-wheat/wheat stocks/use monthly model (US 2025/26 defaults).")
    parser.add_argument("--begin", type=float, default=DEFAULTS["beginning_stocks"],
                        help=f"Beginning stocks (million bushels). Default {DEFAULTS['beginning_stocks']}")
    parser.add_argument("--prod", type=float, default=DEFAULTS["production"],
                        help=f"Production (million bushels). Default {DEFAULTS['production']}")
    parser.add_argument("--imp", type=float, default=DEFAULTS["imports"],
                        help=f"Imports (million bushels). Default {DEFAULTS['imports']}")
    parser.add_argument("--dom", type=float, default=DEFAULTS["domestic_use"],
                        help=f"Domestic use (million bushels). Default {DEFAULTS['domestic_use']}")
    parser.add_argument("--exp", type=float, default=DEFAULTS["exports"],
                        help=f"Exports (million bushels). Default {DEFAULTS['exports']}")
    parser.add_argument("--loss", type=float, default=0.2,
                        help="Loss rate percent per month (e.g., 0.2 means 0.2% per month). Default 0.2")
    parser.add_argument("--monthly-override", type=parse_monthly_override, default=None,
                        help="Optional comma-separated 12 monthly starting stock values (million bu) Jun->May.")
    args = parser.parse_args()

    run_model(begin_stocks_mbu=args.begin,
              production_mbu=args.prod,
              imports_mbu=args.imp,
              domestic_use_mbu=args.dom,
              exports_mbu=args.exp,
              loss_rate_pct_per_month=args.loss,
              monthly_stock_override=args.monthly_override,
              show_monthly=True)

if __name__ == "__main__":
    main()