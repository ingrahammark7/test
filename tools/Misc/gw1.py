#!/usr/bin/env python3
import math

def neuron_atoms(radius_m=10e-6, include_dendrites=True):
    """Estimate total number of atoms in a neuron (kg/m3 ~ 1000, avg atom mass 12 amu)."""
    V_soma = 4/3 * math.pi * radius_m**3
    if include_dendrites:
        V_neuron = 2 * V_soma
    else:
        V_neuron = V_soma
    m_neuron = 1000 * V_neuron  # kg
    m_atom = 12 * 1.66e-27  # kg
    N_atoms = m_neuron / m_atom
    N_electrons = 6 * N_atoms
    return N_atoms, N_electrons

def protein_particle_limit(N_atoms_total, N_atoms_repair=1e7):
    """Compute max particle size (atoms) and number of particles."""
    particles = N_atoms_total / N_atoms_repair
    particle_size = N_atoms_repair
    return int(particles), int(particle_size)

def spike_energy(bits=1, energy_per_bit=1e-11, freq_hz=10):
    """Compute neuron power usage for given spike rate."""
    energy_per_sec = energy_per_bit * bits * freq_hz
    return energy_per_sec

def areal_bit_rate(active_neurons=1.8e7, osc_hz=10):
    """Compute effective bit rate (bits/sec) for given oscillation."""
    return active_neurons * osc_hz

def ponderomotive_force(q=1.6e-19, m=3.8e-26, E=2e7, freq_hz=10, R_m=1e-5):
    """Estimate ponderomotive force on ion inside neuron."""
    omega = 2 * math.pi * freq_hz
    grad_E2 = E**2 / R_m
    F = (q**2 / (4 * m * omega**2)) * grad_E2
    return F

def brain_temperature(R_m=0.08, k=0.6, total_power_W=10, brain_volume_m3=1.3e-3):
    """Estimate central temperature rise (°C) in brain sphere."""
    q = total_power_W / brain_volume_m3
    delta_T = q * R_m**2 / (6 * k)
    return delta_T

def main():
    print("=== Neuron / Brain CLI Analysis ===\n")
    # Neuron atoms
    N_atoms, N_electrons = neuron_atoms()
    print(f"Neuron atoms: {N_atoms:.2e}, electrons: {N_electrons:.2e}")
    
    # Protein particle limit
    particles, particle_size = protein_particle_limit(N_atoms)
    print(f"Max particles per neuron: {particles}, particle size (atoms): {particle_size}")
    
    # Spike energy
    energy = spike_energy(freq_hz=10)
    print(f"Neuron energy usage @10Hz: {energy:.2e} W")
    
    # Areal bit rate
    bit_rate = areal_bit_rate()
    print(f"Effective areal bit rate: {bit_rate:.2e} bits/sec (~20 Mbps realistic)")
    
    # Ponderomotive force
    F_pond = ponderomotive_force()
    print(f"Ponderomotive force on ion: {F_pond:.2e} N")
    
    # Brain temperature rise
    delta_T = brain_temperature()
    print(f"Central brain temperature rise (R=8cm): {delta_T:.2f} °C (without perfusion)\n")
    
    print("=== End of Analysis ===")

if __name__ == "__main__":
    main()