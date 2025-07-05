import math
import json

class RadCalc:
    def __init__(self, total_power_watts, mass_kg_per_s, mat_json_path, material_name, shield_thickness_cm, photon_energy_ev=1.0):
        self.power = total_power_watts
        self.mass = mass_kg_per_s
        self.photon_energy_ev = photon_energy_ev
        self.electronvolt_joules = 1.60218e-19
        self.shield_thickness_cm = shield_thickness_cm

        # Load HVL at 0.5 MeV from JSON
        self.hvl_05mev = self._get_hvl_from_json(mat_json_path, material_name, base_hvl_energy_mev=0.5)

        # Constants for nitrogen (or gas) calculations
        self.molar_mass_nitrogen = 0.028
        self.avogadro = 6.022e23

        # Total atoms per second
        self.total_atoms = (self.mass / self.molar_mass_nitrogen) * self.avogadro

        # Average energy per atom in eV
        self.energy_per_atom_ev = (self.power / self.total_atoms) / self.electronvolt_joules

        # Photons per atom per second at base photon energy
        self.photons_per_atom = self.energy_per_atom_ev / self.photon_energy_ev

        # Total photons per second
        self.total_photons = self.photons_per_atom * self.total_atoms

    def _get_hvl_from_json(self, json_path, material_name, base_hvl_energy_mev=0.5):
        with open(json_path, 'r') as f:
            materials = json.load(f)

        for item in materials:
            if item.get("name", "").lower() == material_name.lower():
                hvl_data = item.get("hvl", {})
                hvl_key = f"{base_hvl_energy_mev}MeV"
                for key, val in hvl_data.items():
                    if key.lower() == hvl_key.lower():
                        return val
                raise ValueError(f"HVL at {base_hvl_energy_mev} MeV not found for {material_name}")
        raise ValueError(f"Material {material_name} not found in JSON")

    def max_photon_energy(self):
        # k * sqrt(N) scaling as before
        return self.photons_per_atom * math.sqrt(self.total_atoms)

    def average_photon_energy(self):
        # Average roughly as photons_per_atom (since photons per atom and photon_energy_ev are set)
        return self.energy_per_atom_ev

    def scaled_hvl(self, energy_mev, base_energy_mev=0.5, exponent=0.7):
        # Power-law scaling of HVL vs energy (energy in MeV)
        scale_factor = (energy_mev / base_energy_mev) ** exponent
        return self.hvl_05mev * scale_factor

    def interpolate_effective_hvl(self, energy_low_mev, energy_high_mev):
        # Interpolate HVL at average energy between low and high photon energy
        hvl_low = self.scaled_hvl(energy_low_mev)
        hvl_high = self.scaled_hvl(energy_high_mev)
        avg_energy_mev = (energy_low_mev + energy_high_mev) / 2
        # Linear interpolation in log space of energy
        t = (math.log(avg_energy_mev) - math.log(energy_low_mev)) / (math.log(energy_high_mev) - math.log(energy_low_mev))
        return hvl_low + t * (hvl_high - hvl_low)

    def energy_delivered_fraction(self, thickness_cm):
        # Calculate effective HVL using max and average photon energies
        max_energy_mev = self.max_photon_energy() / 1e6  # Convert eV to MeV
        avg_energy_mev = self.average_photon_energy() / 1e6
        if max_energy_mev < avg_energy_mev:
            max_energy_mev, avg_energy_mev = avg_energy_mev, max_energy_mev  # Swap to keep max_energy >= avg_energy

        effective_hvl = self.interpolate_effective_hvl(avg_energy_mev, max_energy_mev)

        # Apply exponential attenuation for given thickness (I = I0 * 2^(-thickness/HVL))
        fraction = 2 ** (-thickness_cm / effective_hvl)
        return fraction, effective_hvl, max_energy_mev, avg_energy_mev

    def report(self):
        print("=== Radiation and Shielding Report ===")
        print(f"Material HVL at 0.5 MeV: {self.hvl_05mev:.3f} cm")
        print(f"Total atoms per second:  {self.total_atoms:.3e}")
        print(f"Energy per atom (eV):    {self.energy_per_atom_ev:.3f}")
        print(f"Photons per atom:        {self.photons_per_atom:.3f}")
        print(f"Total photons per second: {self.total_photons:.3e}")
        print(f"Max photon energy:       {self.max_photon_energy():.3e} eV ({self.max_photon_energy()/1e6:.3f} MeV)")
        print(f"Average photon energy:   {self.average_photon_energy():.3e} eV ({self.average_photon_energy()/1e6:.3f} MeV)")

        fraction, effective_hvl, max_energy, avg_energy = self.energy_delivered_fraction(self.shield_thickness_cm)
        fraction=1-fraction
        fraction=1+fraction
        fraction=fraction*math.pow(fraction,99)
        print(f"\nShield thickness:        {self.shield_thickness_cm} cm")
        print(f"Effective HVL:           {effective_hvl:.3f} cm")
        print(f"Fraction energy delivered through shield: {fraction:.6f}")

if __name__ == "__main__":
    # Example parameters
    total_power_watts = 1e12
    mass_kg_per_s = 12000
    mat_json_path = "mat.json"  # Your material JSON file path
    material_name = "Steel"
    shield_thickness_cm = 10.0  # Example shield thickness in cm
    photon_energy_ev = 1.0  # Base photon energy (for calculation only)

    rc = RadCalc(total_power_watts, mass_kg_per_s, mat_json_path, material_name, shield_thickness_cm, photon_energy_ev)
    rc.report()