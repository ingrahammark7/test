import math
import json

class RadCalc:
    def __init__(self, total_power_watts, mass_kg_per_s, mat_json_path, material_name, photon_energy_ev=1.0):
        self.power = total_power_watts  # in watts
        self.mass = mass_kg_per_s       # in kg/s
        self.photon_energy_ev = photon_energy_ev
        self.electronvolt_joules = 1.60218e-19

        # Load material data and extract HVL at 0.5 MeV
        self.hvl = self._get_hvl_from_json(mat_json_path, material_name, base_hvl_energy_mev=0.5)

        # Constants for nitrogen (or other material) calculations
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

    def _get_hvl_from_json(self, json_path, material_name, base_hvl_energy_mev=0.5):
        with open(json_path, 'r') as f:
            materials = json.load(f)

        mat = None
        for item in materials:
            if item.get("name", "").lower() == material_name.lower():
                mat = item
                break
        if mat is None:
            raise ValueError(f"Material '{material_name}' not found in JSON")

        hvl_data = mat.get("hvl", {})
        hvl_key = f"{base_hvl_energy_mev}MeV"
        hvl_value = None
        for key, val in hvl_data.items():
            if key.lower() == hvl_key.lower():
                hvl_value = val
                break
        if hvl_value is None:
            raise ValueError(f"HVL for {base_hvl_energy_mev} MeV not found in material data for '{material_name}'")

        return hvl_value

    def scaled_hvl(self, target_energy_mev, base_energy_mev=0.5, exponent=0.7):
        """
        Scale the HVL from base_energy_mev to target_energy_mev using power law scaling.
        exponent default 0.7 can be adjusted empirically.
        Returns HVL in same units as base HVL (cm).
        """
        if target_energy_mev <= 0:
            raise ValueError("Energy must be positive")
        scale_factor = (target_energy_mev/ base_energy_mev) ** exponent
        return self.hvl * scale_factor

    def max_photon_energy(self):
        # Maximum photon energy based on: k * sqrt(N)
        # Here k = photons_per_atom (mean photons per atom)
        return self.photons_per_atom * math.sqrt(self.total_atoms)

    def photons_above_threshold_log_model(self, threshold_ev):
        E_max = self.max_photon_energy()
        if threshold_ev >= E_max:
            return 0
        ratio = E_max / threshold_ev
        ratio = ratio * ratio  # square of ratio
        return ratio

    def report(self):
        print("=== Photon Emission Report ===")
        print(f"Total nitrogen atoms per second:      {self.total_atoms:.3e}")
        print(f"Energy per atom (average):            {self.energy_per_atom_ev:.3f} eV")
        print(f"Photons per atom per second (@1 eV): {self.photons_per_atom:.3f}")
        print(f"Total photons per second:              {self.total_photons:.3e}")
        print(f"Maximum photon energy:                 {self.max_photon_energy():.3e} eV")
        print(f"Half-Value Layer (HVL) of {material_name} at 0.5 MeV: {self.hvl} cm")

        print("\n=== Scaled HVL Examples ===")
        for energy in [0.25, 0.5, 1, 2, 5]:  # MeV values to show scaling
            scaled = self.scaled_hvl(energy)
            print(f"HVL at {energy} MeV: {scaled:.3f} cm")

        print("\n=== Estimated Photon Counts Above Energy Thresholds (Log Dropoff) ===")
        thresholds = [("1 MeV", 1e6), ("1 GeV", 1e9), ("1 TeV", 1e12), ("1 PeV", 1e15)]
        for label, ev in thresholds:
            n = self.photons_above_threshold_log_model(ev)
            print(f"Photons > {label}: {n:.3e} photons/sec")


if __name__ == "__main__":
    # Customize these parameters
    total_power_watts = 1e12
    mass_kg_per_s = 12000
    mat_json_path = "mat.json"   # Path to your JSON file
    material_name = "Steel"
    photon_energy_ev = 1.0  # Base photon energy in eV for calculation

    rc = RadCalc(total_power_watts, mass_kg_per_s, mat_json_path, material_name, photon_energy_ev)
    rc.report()