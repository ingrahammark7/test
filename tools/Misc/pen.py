import math

class Material:
    def __init__(self, name, molar_mass_g_mol, density_kg_m3, atomic_radius_m, atomic_number,
                 cohesive_energy_ev, base_hvl_cm, material_energy_density_mj_per_hvl, weak_factor=1):
        self.name = name
        self.molar_mass = molar_mass_g_mol
        self.density = density_kg_m3
        self.atomic_radius = atomic_radius_m
        self.atomic_number = atomic_number
        self.cohesive_energy_ev = cohesive_energy_ev
        self.base_hvl_cm = base_hvl_cm
        self.material_energy_density_mj_per_hvl = material_energy_density_mj_per_hvl
        self.weak_factor = weak_factor
        
        # Constants
        self.avogadro = 6.022e23
        self.ev_to_joule = 1.602e-19
        self.k = 9e9  # Coulomb constant
        self.elementary_charge = 1.6e-19
        self.phi = 1.61803398875
        
        # Precompute values
        self.j_high_estimate = self.compute_high_estimate() ** 0.5
        self.cohesive_bond_energy = self.compute_cohesive_bond_energy()
    
    def compute_high_estimate(self):
        ch = (self.elementary_charge ** 2) * self.k / (self.atomic_radius ** 2)
        ch *= self.atomic_number
        ac = self.avogadro * ch
        moles = 1000 / self.molar_mass
        re = moles * ac
        re=re/self.weak_factor
        return re
    
    def compute_cohesive_bond_energy(self):
        mass_g = 1000  # for 1 kg
        moles = mass_g / self.molar_mass
        atoms = moles * self.avogadro
        bond_energy_per_atom_j = self.cohesive_energy_ev * self.ev_to_joule
        total_bond_energy_joules = atoms * bond_energy_per_atom_j
        return total_bond_energy_joules

    def print_summary(self):
        print(f"2 GJ/kg consistent estimate (sqrt): {self.j_high_estimate:.4e}")
        print(f"Cohesive bond energy total (J): {self.cohesive_bond_energy:.4e}")
        print(f"Cohesive bond energy total (MJ): {self.cohesive_bond_energy / 1e6:.4f}")

    def combine_angles(self, angle1_deg, angle2_deg):
        """
        Combine two orthogonal angles (degrees) into one effective angle (degrees).
        Caps at 90 degrees.
        """
        a1=self.clean_angle(angle1_deg) 
        a2=self.clean_angle(angle2_deg) 
        f2=90-a2 
        r=f2/90 
        r=1-r
        r=(a1)*r
        return min(r, 90)
    
    def hvl_mass_kg(self):
    	h=self.base_hvl_cm
    	dens=self.density
    	h=h/100
    	v=h**3
    	m=v*dens
    	return m
    
    def melt_one_hvl(self):
    	h=self.hvl_mass_kg()
    	bo=self.cohesive_bond_energy
    	bo=h*bo
    	return bo
    	
    def thermal_max_pen(self,d,round_energy_mj):
    	f=self.melt_one_hvl()
    	r=(round_energy_mj*(10**6))/(f*self.base_hvl_cm)
    	if(d>r):
    		print("A ", d, "cm penetration was thermally bound to ", r,"cm.")
    		return r
    	print("A ", d,"cm penetration did not reach thermal bound ", r,"cm.")
    	return d

    def penetration_depth(self, round_energy_mj, round_diameter_cm, angle1, angle2, honeycomb_layers, alpha=0.5):
        """
        Compute penetration depth (cm) using your MHD dynamic HVL model,
        with two slope angles (angle1, angle2) in degrees.
        """
        effective_angle = self.combine_angles(angle1, angle2)
        d0 = (round_energy_mj / self.material_energy_density_mj_per_hvl)*self.base_hvl_cm
        n = round_diameter_cm / self.base_hvl_cm
        hvl = self.base_hvl_cm * max(0.01, (1 - alpha * n))
        n_eff = round_diameter_cm / hvl
        d = d0 * n_eff ** 2
        d = self.pen_angle(d, effective_angle, round_energy_mj, round_diameter_cm)
        d=self.honeycomb_pen(d,round_energy_mj,round_diameter_cm,honeycomb_layers)
        d=self.thermal_max_pen(d,round_energy_mj)
        return d, hvl

    def pen_angle(self, d, angle, round_energy_mj, round_diameter_cm):
        if(angle==0):
        	return 0
        r = 90 / angle
        r = r ** (4 ** self.phi)
        d = d / r
        d= self.base_pen(d, round_energy_mj, round_diameter_cm)
        return d
        
    def honeycomb_pen(self,d,round_energy_mj,round_diameter_cm,layers):
    	if(layers==0):
    		return d
    	l=(layers*2)**2
    	r=90/l
    	d=self.pen_angle(d,r,round_energy_mj,round_diameter_cm)
    	d=self.base_pen(d,round_energy_mj,round_diameter_cm)
    	return d
    		
    def clean_angle(self, angle):
        if angle > 180:
            angle -= 180
        if angle > 90:
            angle -= 90
        return angle

    def base_pen(self, d, round_energy_mj, round_diameter_cm):
        e = self.sectional_energy_density(round_energy_mj, round_diameter_cm)
        m = self.material_energy_density_mj_per_hvl
        m= (e/m)*self.base_hvl_cm
        if(m>d):
        	return m
        return d

    def sectional_energy_density(self, round_energy_mj, round_diameter_cm):
        if round_diameter_cm < self.base_hvl_cm:
            return round_energy_mj / (self.base_hvl_cm ** 2)
        return round_energy_mj / ((round_diameter_cm/self.base_hvl_cm) ** 2)


# Example usage:
if __name__ == "__main__":
    steel = Material(
        name="Iron (Steel)",
        molar_mass_g_mol=55.85,
        density_kg_m3=7850,
        atomic_radius_m=126e-12,
        atomic_number=26,
        cohesive_energy_ev=4.28,
        base_hvl_cm=1.3,
        material_energy_density_mj_per_hvl=1,
        weak_factor=1
    )

    du=Material(
    name="Uranium",
    molar_mass_g_mol=238,
    density_kg_m3=1950,
    atomic_radius_m=175e-12,
    atomic_number=92,
    cohesive_energy_ev=5.06,
    base_hvl_cm=0.03,
    material_energy_density_mj_per_hvl=1,
    weak_factor=3
    )
    
    def estfix(self):
    	return (self.j_high_estimate*self.hvl_mass_kg()/(10**6))
    	
    steel.material_energy_density_mj_per_hvl=estfix(steel)
    du.material_energy_density_mj_per_hvl=estfix(du)
    steel.print_summary()
    round_energy = 10  # MJ
    round_diameter = 2.2  # cm
    angle_vert = 90
    angle_horz = 90

    depth, effective_hvl = steel.penetration_depth(round_energy, round_diameter, angle_vert, angle_horz,0)
    print(f"Penetration depth: {depth:.2f} cm")
    print(f"Effective HVL after MHD effect: {effective_hvl:.2f} cm")

