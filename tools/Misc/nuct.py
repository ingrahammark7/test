# nuct.py

import sympy as sp

# Attempt import from your pen.py
from pen import Material # adjust names if different
materials_available = True
import pen

    # Fallback Material class (minimal)



class NuclearPenetrationModel:
    def __init__(self, material):
        self.material = material
        
        # Symbolic variables
        self.E = sp.symbols('E')        # Particle energy in MeV
        self.n_e = sp.symbols('n_e')    # Electron density proxy
        
        self.phi=sp.GoldenRatio
        # Physical constants
        self.alpha_fs = 1/((((4*sp.pi)-6)**self.phi)**self.phi)# Fine structure constant
        self.alpha=1/self.alpha_fs
        self.am=self.alpha**self.phi
        self.osc=6
        self.brem=self.am*(self.alpha**(1+((1/((self.osc-1)*(self.osc-2))))))
        self.disc=self.brem*16
        self.shellt=self.brem/3
        self.compt=self.brem*2
       

    def bremsstrahlung_loss(self):
        # Z squared factor
        Z = self.material.atomic_number
        frac=self.E/self.compt
        expr=frac*self.osc
        # Bremsstrahlung loss symbolic expression
        loss_expr = (Z**expr) * self.n_e * self.alpha_fs * sp.log(self.E + 1)
        return loss_expr

    def honeycomb_dissipation_factor(self, layers):
        return (1 + layers)**3

    def penetration(self, round_energy_mj, round_diameter_cm, honeycomb_layers=0):
        # Convert MJ to MeV (approx 1 MJ = 6.242e12 MeV)
        E_mev_val = round_energy_mj * 6.242e12

        # Electron density proxy proportional to material density (adjust as needed)
        n_e_val = self.material.density * 1e-3

        brems_loss_expr = self.bremsstrahlung_loss()
        brems_loss_val = brems_loss_expr.subs({
            self.E: E_mev_val,
            self.n_e: n_e_val
        }).evalf()
        print(self.material.material_energy_density_mj_per_hvl)
        import os
        os.sys.exit()

        base_penetration = (round_energy_mj / self.material.material_energy_density_mj_per_hvl) * self.material.base_hvl_cm
        dissipation = self.honeycomb_dissipation_factor(honeycomb_layers)

        adjusted_penetration = base_penetration / (1 + brems_loss_val * dissipation)

        # Ensure penetration not below 1 HVL physically
        if adjusted_penetration < self.material.base_hvl_cm:
            adjusted_penetration = 0

        return float(adjusted_penetration)


def nuclear_penetration(round_energy_mj, round_diameter_cm, honeycomb_layers=0, material_name="steel"):
    """
    Compute nuclear-effect-adjusted penetration depth (cm) for given round and armor.

    Parameters:
    - round_energy_mj: Kinetic energy of projectile (MJ)
    - round_diameter_cm: Diameter of projectile (cm)
    - honeycomb_layers: Armor layering parameter (float)
    - material_name: String "steel" or "du" (case insensitive), or pass Material instance

    Returns:
    - Estimated penetration depth in cm (float)
    """

    if isinstance(material_name, Material):
        material = material_name
    else:
        mat_name = material_name.lower()
        if mat_name == "steel":
            
            material = pen.getsteel()
            print(material.j_high_estimate)
        elif mat_name == "du":
            material = pen.getdu()
        else:
            # Unknown material, default to steel
            material = pen.getsteel()

    model = NuclearPenetrationModel(material)
    return model.penetration(round_energy_mj, round_diameter_cm, honeycomb_layers)


if __name__ == "__main__":
    # Test/demo
    print("Testing nuclear penetration model...")

    round_energy = 10  # MJ
    round_diameter = 2.2  # cm
    honeycomb = 0

    pen_steel = nuclear_penetration(round_energy, round_diameter, honeycomb, "steel")
    pen_du = nuclear_penetration(round_energy, round_diameter, honeycomb, "du")

    print(f"Estimated penetration in Steel: {pen_steel:.3f} cm")
    print(f"Estimated penetration in Depleted Uranium: {pen_du:.3f} cm")