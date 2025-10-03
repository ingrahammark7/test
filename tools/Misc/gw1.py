#!/usr/bin/env python3
import argparse
import numpy as np
import csv

def run_simulation(rho_p, rho_f, g, C_d, theta_deg, v_w, H_min, H_max, N, output_file=None):
    theta = np.radians(theta_deg)
    tan_theta = np.tan(theta)

    # Self-consistent particle radius from wind-driven transport
    r = (3 * C_d * rho_f * v_w**2) / (8 * rho_p * g)  # meters
    r_microns = r * 1e6  # convert to microns

    hill_heights = np.random.uniform(H_min, H_max, N)
    particle_radii = np.full(N, r_microns)

    if output_file:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Hill_height_m', 'Particle_radius_um'])
            for H, radius in zip(hill_heights, particle_radii):
                writer.writerow([H, radius])
        print(f"Results saved to {output_file}")
    else:
        for H, radius in zip(hill_heights, particle_radii):
            print(f"Hill height: {H:.3f} m, Particle radius: {radius:.3f} μm")

    print(f"\nTypical particle radius (all samples): {r_microns:.3f} μm")
    return hill_heights, particle_radii

def main():
    parser = argparse.ArgumentParser(description="CLI Monte Carlo wind-driven hill simulation (no plot).")
    parser.add_argument("--rho_p", type=float, default=3000, help="Particle density (kg/m^3)")
    parser.add_argument("--rho_f", type=float, default=1.2, help="Air/fluid density (kg/m^3)")
    parser.add_argument("--g", type=float, default=9.8, help="Gravity (m/s^2)")
    parser.add_argument("--C_d", type=float, default=0.5, help="Drag coefficient")
    parser.add_argument("--theta", type=float, default=45.0, help="Slope angle in degrees")
    parser.add_argument("--v_w", type=float, default=5.0, help="Wind speed (m/s)")
    parser.add_argument("--H_min", type=float, default=0.0001, help="Minimum hill height (m)")
    parser.add_argument("--H_max", type=float, default=5000.0, help="Maximum hill height (m)")
    parser.add_argument("--N", type=int, default=10000, help="Number of Monte Carlo samples")
    parser.add_argument("--output", type=str, help="Optional CSV output file path")

    args = parser.parse_args()
    run_simulation(args.rho_p, args.rho_f, args.g, args.C_d, args.theta, args.v_w,
                   args.H_min, args.H_max, args.N, args.output)

if __name__ == "__main__":
    main()