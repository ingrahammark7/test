import math

class RadCalc:
    def __init__(self, total_power_watts, mass_kg_per_s, photon_energy_ev=1.0):
        self.power = total_power_watts  # in watts
        self.mass = mass_kg_per_s       # in kg/s
        self.photon_energy_ev = photon_energy_ev
        self.electronvolt_joules = 1.60218e-19
        self.molar_mass_nitrogen = 0.028  # kg/mol for N2
        self.avogadro = 6.022e23

        # Total nitrogen atoms per second
        self.total_atoms = (self.mass / self.molar_mass_nitrogen) * self.avogadro

        # Energy per atom in eV (average)
        self.energy_per_atom_ev = (self.power / self.total_atoms) / self.electronvolt_joules

        # Photons per atom per second at base photon energy (default 1 eV)
        self.photons_per_atom = self.energy_per_atom_ev / self.photon_energy_ev

        # Total photons per second
        self.total_photons = self.photons_per_atom * self.total_atoms

    def max_photon_energy(self):
        # Maximum photon energy based on: k * sqrt(N)
        # Here k = photons_per_atom (mean photons per atom)
        return self.photons_per_atom * math.sqrt(self.total_atoms)

    def photons_above_threshold_log_model(self, threshold_ev):
        E_max = self.max_photon_energy()
        if threshold_ev >= E_max:
            return 0
        rat=E_max/threshold_ev
        rat=rat*rat
        return rat

    def report(self):
        print("=== Photon Emission Report ===")
        print(f"Total nitrogen atoms per second:      {self.total_atoms:.3e}")
        print(f"Energy per atom (average):            {self.energy_per_atom_ev:.3f} eV")
        print(f"Photons per atom per second (@1 eV): {self.photons_per_atom:.3f}")
        print(f"Total photons per second:              {self.total_photons:.3e}")
        print(f"Maximum photon energy:                 {self.max_photon_energy():.3e} eV")

        print("\n=== Estimated Photon Counts Above Energy Thresholds (Log Dropoff) ===")
        thresholds = [("1 MeV", 1e6), ("1 GeV", 1e9), ("1 TeV", 1e12), ("1 PeV", 1e15)]
        for label, ev in thresholds:
            n = self.photons_above_threshold_log_model(ev)
            print(f"Photons > {label}: {n:.3e} photons/sec")

if __name__ == "__main__":
    rc = RadCalc(total_power_watts=1e12, mass_kg_per_s=12000)
    rc.report()