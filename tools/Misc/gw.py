#!/usr/bin/env python3
"""
Educational-only Arrhenius demo adapted with RDX-like numeric parameters (purely theoretical).

SAFETY NOTICE: This is a purely in-silico, non-operational demonstration for educational/modeling only.
It does NOT provide instructions for synthesis, handling, storage, or initiation of energetic materials.
Do NOT use this code to guide any real-world work with explosives. Consult qualified authorities for real testing.

The numeric choices (A, Ea) are representative literature-like magnitudes for RDX thermal decomposition kinetics
used ONLY to make the simulated curves show realistic temperature sensitivity. They are not exact experimental values.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import os

# Representative (theoretical) Arrhenius parameters for RDX-like thermal decomposition (1/s and J/mol)
A_true = 1e17       # representative pre-exponential (1/s) — for demo only
Ea_true = 160e3     # representative activation energy (J/mol) — for demo only
R = 8.31446261815324  # J/mol/K

# Experiment temperatures (°C) chosen to show negligible decay at room-T and measurable decay at elevated T
temps_C = np.array([25.0, 100.0, 150.0])
temps_K = temps_C + 273.15

# Time vector: focus on short-to-intermediate times where decomposition could be observable at elevated T
t_max = 100000* 3600.0   # simulate 48 hours in seconds
n_points = 250
t = np.linspace(0, t_max, n_points)

C0 = 1.0  # normalized initial amount

def arrhenius_k(A, Ea, T):
    return A * np.exp(-Ea / (R * T))

def simulate_decay_first_order(k, t, C0=1.0, noise_std=0.005):
    C = C0 * np.exp(-k * t)
    noise = np.random.normal(scale=noise_std, size=C.shape) * C0
    return np.clip(C + noise, a_min=0, a_max=None)

def run_simulation(seed=2025, noise_std=0.003):
    datasets = []
    np.random.seed(seed)
    for T, Tc in zip(temps_K, temps_C):
        k_true = arrhenius_k(A_true, Ea_true, T)
        C = simulate_decay_first_order(k_true, t, C0=C0, noise_std=noise_std)
        datasets.append({"T_C": Tc, "T_K": T, "k_true": k_true, "t": t, "C": C})
    return datasets

def fit_first_order(datasets):
    fitted_results = []
    for data in datasets:
        mask = data["C"] > 0
        tt = data["t"][mask]
        lnC = np.log(data["C"][mask])
        slope, intercept, r_value, p_value, std_err = stats.linregress(tt, lnC)
        k_est = -slope
        C0_est = np.exp(intercept)
        fitted_results.append({
            "T_C": data["T_C"],
            "T_K": data["T_K"],
            "k_true": data["k_true"],
            "k_est": k_est,
            "C0_est": C0_est,
            "r2": r_value**2
        })
    return pd.DataFrame(fitted_results)

def fit_arrhenius(df_results):
    invT = 1.0 / df_results["T_K"].values
    lnk = np.log(df_results["k_est"].replace(0, np.nan)).values  # avoid log(0)
    # If any k_est are non-finite, replace with a very small number for fitting
    lnk = np.where(np.isfinite(lnk), lnk, np.log(1e-50))
    slope, intercept, r_value, p_value, std_err = stats.linregress(invT, lnk)
    Ea_fit = -slope * R
    A_fit = np.exp(intercept)
    return {"slope": slope, "intercept": intercept, "r2": r_value**2, "Ea_fit_J_per_mol": Ea_fit, "A_fit_per_s": A_fit, "invT": invT, "lnk": lnk}

def plot_results(datasets, df_results, arrh_fit, out_dir=None):
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # Plot 1: Decay curves (hours on x-axis)
    plt.figure(figsize=(8,5))
    for data, row in zip(datasets, df_results.to_dict(orient="records")):
        plt.plot(data["t"] / 3600.0, data["C"], label=f"{data['T_K']-273.15:.0f} °C data")
        C_fit = row["C0_est"] * np.exp(-row["k_est"] * data["t"])
        plt.plot(data["t"] / 3600.0, C_fit, linestyle="--", label=f"{data['T_K']-273.15:.0f} °C fit")
    plt.xlabel("Time (hours)")
    plt.ylabel("Relative quantity (arb. units)")
    plt.title("Simulated first-order decay (RDX-like parameters)")
    plt.legend()
    plt.tight_layout()
    if out_dir:
        plt.savefig(os.path.join(out_dir, "decay_curves.png"), bbox_inches="tight")
    plt.show()

    # Plot 2: Arrhenius plot (ln(k) vs 1/T)
    plt.figure(figsize=(6,5))
    plt.plot(arrh_fit["invT"], arrh_fit["lnk"], marker="o", linestyle="none", label="Estimated ln(k)")
    x_line = np.linspace(arrh_fit["invT"].min()*0.95, arrh_fit["invT"].max()*1.05, 100)
    y_line = arrh_fit["intercept"] + arrh_fit["slope"] * x_line
    plt.plot(x_line, y_line, linestyle="-", label="Arrhenius fit")
    plt.xlabel("1 / Temperature (1/K)")
    plt.ylabel("ln(k)")
    plt.title("Arrhenius fit (RDX-like demo)")
    plt.legend()
    plt.tight_layout()
    if out_dir:
        plt.savefig(os.path.join(out_dir, "arrhenius_plot.png"), bbox_inches="tight")
    plt.show()

def main():
    datasets = run_simulation()
    df_results = fit_first_order(datasets)
    arrh_fit = fit_arrhenius(df_results)

    # Display numeric results to console and save CSV
    print("\nFitted decay rates (RDX-like demo):")
    print(df_results.to_string(index=False, float_format="{:.3e}".format))
    df_results.to_csv("fitted_decay_rates.csv", index=False)
    print("\nSaved fitted_decay_rates.csv")

    print("\nEducational-only fitted Arrhenius parameters (representative magnitudes):")
    print(f"Estimated A = {arrh_fit['A_fit_per_s']:.3e} 1/s (theoretical demo, not experimental)")
    print(f"Estimated Ea = {arrh_fit['Ea_fit_J_per_mol']/1000:.2f} kJ/mol")
    print(f"R^2 of Arrhenius linear fit = {arrh_fit['r2']:.4f}")

    # Remind user of safety boundaries
    print("\nSAFETY: These numbers are for simulation visualization only. This output does not imply safe handling practices.")

    # Generate plots and optionally save them
    plot_results(datasets, df_results, arrh_fit, out_dir="figures")

if __name__ == "__main__":
    main()