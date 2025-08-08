# nuct.py

import sympy as sp
import math

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
        self.evperj=pen.getsteel().ev_to_joule
        self.pm=self.alpha**self.phi**4.55
        self.ac=self.pm       
        self.prma=1/(self.alpha**self.phi**5)
        self.prma=self.prma/1000
        self.pm=self.pm*self.prma
        print(self.pm.evalf())
        self.ec=material.elementary_charge
       

    def bremsstrahlung_loss(self, E_mev, n_e):
    	Z = self.material.atomic_number
    	E_mev=math.sqrt(E_mev)
    	frac = E_mev / (self.compt)
    	exponent = frac * self.osc
    	loss = (Z ** exponent) * n_e * self.alpha_fs * 		math.log(E_mev + 1)
    	return loss
    
    def mhd_bolus(self,E_mev,round_energy_mj,round_diameter_cm,round_mas):
    	numpm=round_mas/self.pm
    	perpm=round_energy_mj/numpm
    	numpm=math.sqrt(numpm)
    	peaken=numpm*perpm
    	charger=(peaken/numpm)/pen.getsteel().ch1
    	if(charger>1):
    		print("ionization achieved")
    	print(charger.evalf())
    	return 1#placeholder

    def honeycomb_dissipation_factor(self, layers):
        return (1 + layers)**3
        
    def mjtomev(self,num):
    	return num*6.242e12

    def penetration(self, round_energy_mj, round_diameter_cm, honeycomb_layers, round_mas):
        # Convert MJ to MeV (approx 1 MJ = 6.242e12 MeV)
        round_front_vol=round_diameter_cm*round_diameter_cm/1000000
        round_front_mass=round_front_vol*self.material.density        
        round_ld=round_mas/round_front_mass
        print("round ld ",round_ld)
        E_mev_val = self.mjtomev(round_energy_mj)

        # Electron density proxy proportional to material density (adjust as needed)
        n_e_val = self.material.density * (1/self.am)

        brems_loss_expr = self.bremsstrahlung_loss(E_mev_val,n_e_val)
        brems_loss_val = brems_loss_expr.subs({
            self.E: E_mev_val,
            self.n_e: n_e_val
        }).evalf()
        
        base_penetration = (round_energy_mj / self.material.material_energy_density_mj_per_hvl) * self.material.base_hvl_cm
        
        dissipation = self.honeycomb_dissipation_factor(honeycomb_layers)

        if(brems_loss_val>E_mev_val):
        	brems_loss_val=0 #entire energy dissipated
        mhd_var=self.mhd_bolus(E_mev_val,round_energy_mj,round_diameter_cm,round_mas)
        adjusted_penetration = mhd_var+base_penetration / (1 + brems_loss_val * dissipation)
        # Ensure penetration not below 1 HVL physically
        if adjusted_penetration < self.material.base_hvl_cm:
            adjusted_penetration = 0

        return float(adjusted_penetration)


def nuclear_penetration(round_energy_mj, round_diameter_cm, honeycomb_layers, round_mas, material_name="steel"):
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
        elif mat_name == "du":
            material = pen.getdu()
        else:
            # Unknown material, default to steel
            material = pen.getsteel()

    model = NuclearPenetrationModel(material)
    return model.penetration(round_energy_mj, round_diameter_cm, honeycomb_layers,round_mas)


if __name__ == "__main__":
    # Test/demo
    print("Testing nuclear penetration model...")

    round_energy = 10e-5 # MJ
    round_diameter = 2.2  # cm
    round_mass=2
    honeycomb = 0

    pen_steel = nuclear_penetration(round_energy, round_diameter, honeycomb, round_mass, "steel")
    pen_du = nuclear_penetration(round_energy, round_diameter, honeycomb, round_mass, "du")

    print(f"Estimated penetration in Steel: {pen_steel:.3f} cm")
    print(f"Estimated penetration in Depleted Uranium: {pen_du:.3f} cm")