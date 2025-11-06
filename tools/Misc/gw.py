#!/usr/bin/env python3
"""
Generic physical-erosion demo (deterministic erosion + stochastic spallation)
Safe, abstract modeling example — not operational guidance.

This script simulates a rectangular block (mass normalized) experiencing:
 - continuous surface erosion rate E(t) = E0 * (1 + alpha*T_factor)
 - stochastic spallation events occurring as a Poisson process with rate lambda(t),
   each event removing a random chunk mass drawn from a chosen distribution.

Outputs:
 - time series of normalized mass
 - histogram of spall event sizes
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------- model parameters (abstract, generic) ----------
t_total = 48.0  # total simulation time in hours
dt = 0.01       # time step in hours
times = np.arange(0.0, t_total + dt, dt)

# initial conditions
mass0 = 1.0     # normalized initial mass
thickness0 = 1.0  # normalized thickness (arbitrary units)

# Continuous erosion: E0 in mass units per hour
E0 = 1e-3       # baseline continuous erosion rate
alpha_T = 0.0   # optional temperature factor (keeps model general)

# Stochastic spallation (Poisson events)
lambda_base = 0.05  # base event rate per hour (expected events/hour)
# event rate could depend on 'damage' or other variables; keep simple here

# chunk size distribution for spall events (use a gamma to get skew)
spall_shape = 2.0
spall_scale = 0.01  # mean chunk size = shape*scale

# random seed for reproducibility
rng = np.random.default_rng(2025)

# ---------- simulation arrays ----------
mass = np.empty_like(times)
thickness = np.empty_like(times)
mass[0] = mass0
thickness[0] = thickness0

spall_times = []
spall_sizes = []

# ---------- simulation loop ----------
for i in range(1, len(times)):
    t = times[i]
    # continuous erosion this timestep
    E_t = E0 * (1.0 + alpha_T * 0.0)  # placeholder for temperature effect
    dmass_cont = E_t * dt

    # Poisson chance of one or more spall events in dt
    # expected number = lambda_base * dt; draw number from Poisson
    expected_events = lambda_base * dt
    n_events = rng.poisson(expected_events)

    # if events occur, draw sizes and subtract
    dmass_spall = 0.0
    if n_events > 0:
        sizes = rng.gamma(spall_shape, spall_scale, size=n_events)
        dmass_spall = sizes.sum()
        # record individual events
        for j, s in enumerate(sizes):
            spall_times.append(t)
            spall_sizes.append(s)

    # update mass (prevent negative)
    new_mass = max(0.0, mass[i-1] - dmass_cont - dmass_spall)
    mass[i] = new_mass

    # thickness proportional to mass (simple linear relation for demo)
    thickness[i] = (mass[i] / mass0) * thickness0

# ---------- results ----------
print(f"Simulated {len(spall_sizes)} spall events over {t_total} hours.")
print(f"Final normalized mass: {mass[-1]:.5f}")
print(f"Total mass lost: {mass0 - mass[-1]:.5f}")

# Plotting: mass vs time and event raster
plt.figure(figsize=(10,4))
plt.plot(times, mass, label="Normalized mass")
plt.xlabel("Time (hours)")
plt.ylabel("Normalized mass")
plt.title("Physical erosion + stochastic spallation (generic model)")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Add a small raster of spall event times on top
if spall_times:
    plt.vlines(spall_times, ymin=0.0, ymax=0.03, alpha=0.4, linewidth=1, label="spall events")
    plt.legend()

plt.show()

# Histogram of spall sizes
if spall_sizes:
    plt.figure(figsize=(6,3))
    plt.hist(spall_sizes, bins=30)
    plt.xlabel("Spall chunk size (normalized mass units)")
    plt.ylabel("Count")
    plt.title("Histogram of spall chunk sizes")
    plt.tight_layout()
    plt.show()