import math

class Material:
    def __init__(self, name, molar_mass_g_mol, density_kg_m3, atomic_radius_m, atomic_number,
                 cohesive_energy_ev, base_hvl_cm, material_energy_density_mj_per_cm):
        self.name = name
        self.molar_mass = molar_mass_g_mol
        self.density = density_kg_m3
        self.atomic_radius = atomic_radius_m
        self.atomic_number = atomic_number
        self.cohesive_energy_ev = cohesive_energy_ev
        self.base_hvl_cm = base_hvl_cm
        self.material_energy_density_mj_per_cm = material_energy_density_mj_per_cm
        
        
        # Constants
        self.avogadro = 6.022e23
        self.ev_to_joule = 1.602e-19
        self.k = 9e9  # Coulomb constant
        self.elementary_charge = 1.6e-19
        self.phi=1.61803398875
        
        # Precompute values
        self.j_high_estimate = self.compute_high_estimate()
        self.j_high_estimate=self.j_high_estimate**.5
    
        self.cohesive_bond_energy = self.compute_cohesive_bond_energy()
    
    def compute_high_estimate(self):
        ch = (self.elementary_charge ** 2) * self.k / (self.atomic_radius ** 2)
        ch *= self.atomic_number
        ac = self.avogadro * ch
        moles = 1000 / self.molar_mass
        re = moles * ac
        return re
    
    def compute_cohesive_bond_energy(self):
        mass_g = 1000  # for 1 kg iron
        moles = mass_g / self.molar_mass
        atoms = moles * self.avogadro
        bond_energy_per_atom_j = self.cohesive_energy_ev * self.ev_to_joule
        total_bond_energy_joules = atoms * bond_energy_per_atom_j
        return total_bond_energy_joules


    def print_summary(self):
        
      print(f"2 GJ/kg consistent estimate (sqrt): {self.j_high_estimate:.4e}")
      print(f"Cohesive bond energy total (J): {self.cohesive_bond_energy:.4e}")
      print(f"Cohesive bond energy total (MJ): {self.cohesive_bond_energy / 1e6:.4f}")
    
    def penetration_depth(self, round_energy_mj, round_diameter_cm, angle, alpha=0.5):
        angle=self.clean_angle(angle)
        """
        Compute penetration depth (cm) using your MHD dynamic HVL model.
        """
        d0 = round_energy_mj / self.material_energy_density_mj_per_cm
        n = round_diameter_cm / self.base_hvl_cm
        hvl = self.base_hvl_cm * max(0.01, (1 - alpha * n))  # prevent zero or negative HVL
        n_eff = round_diameter_cm / hvl
        d = d0 * n_eff ** 2
        d=self.pen_angle(d,angle,round_energy_mj,round_diameter_cm)
        return d, hvl
        
    def pen_angle(self,d,angle,round_energy_mj,round_diameter_cm):
     	b=self.base_pen(d,round_energy_mj,round_diameter_cm)   	
     	r=90/angle
     	r=r**4**self.phi
     	d=d/r
     	if(d<b):
     		return b
     	return d
    
    def clean_angle(self,angle):
        if(angle>180):
            angle=angle-180
        if(angle>90):
            angle=angle-90
        return angle
    
    def base_pen(self,d,round_energy_mj,round_diameter_cm):
    	e=self.sectional_energy_density(round_energy_mj,round_diameter_cm)
    	h=self.base_hvl_cm
    	m=self.material_energy_density_mj_per_cm
    	m=m*h
    	return e/m
    
    def sectional_energy_density(self,round_energy_mj,round_diameter_cm):
    	if(round_diameter_cm<self.base_hvl_cm):
    		return round_energy_mj/self.base_hvl_cm/self.base_hvl_cm
    	return round_energy_mj/round_diameter_cm/round_diameter_cm


# Usage example:
steel = Material(
    name="Iron (Steel)",
    molar_mass_g_mol=55.85,
    density_kg_m3=7850,
    atomic_radius_m=126e-12,
    atomic_number=26,
    cohesive_energy_ev=4.28,
    base_hvl_cm=1.3,
    material_energy_density_mj_per_cm=1
)

steel.print_summary()

# Penetration example
round_energy = 10  # MJ
round_diameter = 2.2# cm

steel.material_energy_density_mj_per_cm=(steel.j_high_estimate*steel.density)/1000000/1000000
depth, effective_hvl = steel.penetration_depth(round_energy, round_diameter,70)
print(f"Penetration depth: {depth:.2f} cm")
print(f"Effective HVL after MHD effect: {effective_hvl:.2f} cm")