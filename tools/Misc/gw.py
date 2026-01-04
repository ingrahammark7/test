import numpy as np

# ----------------------------
# Parameters
# ----------------------------
days = 365 * 500*1_0 # simulate 500 years
dt = 1  # time step in days

# Initial phosphate pools (arbitrary units)
P_sol = 10.0     # soluble phosphate
P_org = 5.0      # organic phosphate
P_ca_am = 0.0    # amorphous calcium phosphate
P_apa = 0.0      # crystalline apatite

# Rates (per day)
k_uptake = 0.01      # microbial uptake of soluble P → organic P
k_mineral = 0.005    # mineralization of organic P → soluble P
k_ca_precip = 0.0001 # amorphous Ca-P precipitation rate
k_apa_form = 1e-6    # crystallization of apatite from amorphous Ca-P

# Total initial phosphate for reference
P_total = P_sol + P_org + P_ca_am + P_apa

# Accumulators for fluxes
flux_org = 0.0
flux_inorg = 0.0
flux_apa = 0.0

# Track time to 50% apatite
half_apa_time = None

# ----------------------------
# Simulation loop
# ----------------------------
for t in range(0, days, dt):
    # Microbial cycling
    uptake = k_uptake * P_sol * dt
    mineralization = k_mineral * P_org * dt

    P_sol = P_sol - uptake + mineralization
    P_org = P_org + uptake - mineralization

    # Amorphous Ca-P formation (inorganic)
    ca_precip = k_ca_precip * P_sol * dt
    P_sol -= ca_precip
    P_ca_am += ca_precip

    # Crystalline apatite formation (from amorphous Ca-P)
    apa_form = k_apa_form * P_ca_am * dt
    P_ca_am -= apa_form
    P_apa += apa_form

    # Accumulate fluxes for averaging
    flux_org += uptake  # organic formation
    flux_inorg += ca_precip  # amorphous Ca-P formation
    flux_apa += apa_form     # crystalline apatite formation

    # Check if 50% apatite reached
    if half_apa_time is None and P_apa >= 0.5 * P_total:
        half_apa_time = t / 365  # convert days to years

# ----------------------------
# Console output
# ----------------------------
print("=== Phosphate Cycling Simulation Results ===")
if half_apa_time is not None:
    print(f"Effective delay (time until 50% of total phosphate is in apatite): {half_apa_time:.1f} years")
else:
    print("50% apatite not reached in simulation period.")

# Average daily and yearly fluxes
avg_flux_org_daily = flux_org / days
avg_flux_inorg_daily = flux_inorg / days
avg_flux_apa_daily = flux_apa / days
avg_flux_org_yearly = avg_flux_org_daily * 365
avg_flux_inorg_yearly = avg_flux_inorg_daily * 365
avg_flux_apa_yearly = avg_flux_apa_daily * 365

print(f"\nAverage daily organic formation flux (soluble → organic P): {avg_flux_org_daily:.6f}")
print(f"Average daily inorganic formation flux (soluble → amorphous Ca-P): {avg_flux_inorg_daily:.6f}")
print(f"Average daily apatite formation flux (amorphous → crystalline): {avg_flux_apa_daily:.6e}")
print(f"\nAverage yearly organic flux: {avg_flux_org_yearly:.6f}")
print(f"Average yearly inorganic flux: {avg_flux_inorg_yearly:.6f}")
print(f"Average yearly apatite formation flux: {avg_flux_apa_yearly:.6e}")

# Final phosphate pools
print("\nFinal phosphate pool breakdown (arbitrary units):")
print(f"Soluble P: {P_sol:.3f}")
print(f"Organic P: {P_org:.3f}")
print(f"Amorphous Ca-P: {P_ca_am:.3f}")
print(f"Crystalline Apatite: {P_apa:.3f}")
print(f"Total P: {P_sol + P_org + P_ca_am + P_apa:.3f} (should equal initial {P_total})")