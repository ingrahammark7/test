import math
import nuct

class Material:
    def __init__(self, name, molar_mass_g_mol, density_kg_m3, atomic_radius_m, atomic_number,
                cohesive_energy_ev, base_hvl_cm, material_energy_density_j_per_hvl, weak_factor=1):
        self.name = name
        self.molar_mass = molar_mass_g_mol
        self.density = density_kg_m3
        self.atomic_radius = atomic_radius_m
        self.atomic_number = atomic_number
        self.cohesive_energy_ev = cohesive_energy_ev
        self.base_hvl_cm = base_hvl_cm
        self.material_energy_density_j_per_hvl = material_energy_density_j_per_hvl
        self.weak_factor = weak_factor
        
        # Constants
        self.avogadro = 6.02214076e23
        self.ev_to_joule = 1.602e-19
        self.k = 9e9  # Coulomb constant
        self.elementary_charge = 1.60217663e-19
        self.phi = 1.61803398875
        self.ch=(self.elementary_charge ** 2) * self.k / (self.atomic_radius ** 2)
        self.ch1=self.ch*self.atomic_radius
        self.bol=1.380649e-23
        self.db=24.94
        self.zc=273.15
        self.pmas=nuct.prma/2
        self.emr=nuct.alpha**nuct.phi
        self.emr=self.emr/nuct.phi
        
        # Precompute values
        self.j_high_estimate = self.compute_high_estimate() ** 0.5
        self.cohesive_bond_energy = self.compute_cohesive_bond_energy()
        self.elmol=self.elementary_charge*self.avogadro
        self.elmol=self.elmol**(1/4)
        self.elmol*=self.phi
        self.te=1-(1/(8))
        self.elmol*=self.te
        self.db=self.elmol
    
    def compute_high_estimate(self):
        ch = self.ch
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
        
    def thermal_max_pen(self,d,round_energy):
        f=self.melt_one_hvl()
        r=(round_energy)/(f*self.base_hvl_cm)
        if(d>r):
            print("A ", d, "cm penetration was thermally bound to ", r,"cm.")
            return r
        print("A ", d,"cm penetration did not reach thermal bound ", r,"cm.")
        return d

    def penetration_depth(self, round_energy, round_diameter_cm, angle1, angle2, honeycomb_layers,round_mas):
        """
        Compute penetration depth (cm) using your MHD dynamic HVL model,
        with two slope angles (angle1, angle2) in degrees.
        """
        effective_angle = self.combine_angles(angle1, angle2)
        pm = nuct.NuclearPenetrationModel(self)
        d=nuct.nuclear_penetration(round_energy,round_diameter_cm,honeycomb_layers,round_mas,pm.material)
        d = self.pen_angle(d, effective_angle, round_energy, round_diameter_cm)
        d=self.honeycomb_pen(d,round_energy,round_diameter_cm,honeycomb_layers)
        d=self.thermal_max_pen(d,round_energy)
        return d

    def pen_angle(self, d, angle, round_energy, round_diameter_cm):
        if(angle==0):
            return 0
        r = 90 / angle
        r = r ** (4 ** self.phi)
        d = d / r
        d= self.base_pen(d, round_energy, round_diameter_cm)
        return d
        
    def getvel(self,round_diameter):
        mp=getmp(self)
        ht=getmht(self)
        n=getn()
        round_diameter=round_diameter/100
        ra=round_diameter**2
        airperhit=n.density*ra
        aireng=airperhit*getsh(n)*mp
        airvol=self.velfromen(airperhit,aireng)
        airenpers=aireng*airvol
        ht=airenpers/(ht*mp)
        ba=ht/airvol
        roundside=ra*4
        ba=ba/roundside
        return ba,airvol

    def gets(self):
        round_diameter=self.getdam()
        f,d=self.getvel(round_diameter)
        return d
        
    def getmass(self,round_diameter):
        ld,s=self.getvel(round_diameter)
        round_diameter/=100
        round_diameter*=round_diameter/100
        d=self.density
        ff=round_diameter*ld*d
        return ff
    
    def getdam(self):
        barrel=getsteel()
        maxd=barrel.base_hvl_cm
        doh=barrel.material_energy_density_j_per_hvl
        return self.damiter(maxd,doh)

    def damiter(self,maxd,doh):
        basevel=self.getmass(maxd)
        ff,bases=self.getvel(maxd)
        en=self.enfromvel(basevel,bases)
        r=doh/en
        r=r**.5
        return r*maxd
        
    
    def enfromvel(self,mass,vel):
        return .5*mass*vel*vel
    
    def velfromen(self,mass,en):
        return math.sqrt(2 * (en / mass))
    
    
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

    def base_pen(self, d, round_energy_j, round_diameter_cm):
        e = self.sectional_energy_density(round_energy_j, round_diameter_cm)
        m = self.material_energy_density_j_per_hvl
        m= (e/m)*self.base_hvl_cm
        if(m>d):
            return m
        return d

    def sectional_energy_density(self, round_energy_j, round_diameter_cm):
        if round_diameter_cm < self.base_hvl_cm:
            return round_energy_j / (self.base_hvl_cm ** 2)
        return round_energy_j / ((round_diameter_cm/self.base_hvl_cm) ** 2)

def estfix(self):
        return (self.j_high_estimate*self.hvl_mass_kg())	


def getsteel():
    steel = Material(
        name="Iron (Steel)",
        molar_mass_g_mol=55.85,
        density_kg_m3=7850,
        atomic_radius_m=126e-12,
        atomic_number=26,
        cohesive_energy_ev=4.28,
        base_hvl_cm=1.3,
        material_energy_density_j_per_hvl=1,
        weak_factor=1
    )
    steel.material_energy_density_j_per_hvl=estfix(steel)
    return steel
    
def getdu():
    du=Material(
    name="Uranium",
    molar_mass_g_mol=238,
    density_kg_m3=19500,
    atomic_radius_m=175e-12,
    atomic_number=92,
    cohesive_energy_ev=5.06,
    base_hvl_cm=0.03,
    material_energy_density_j_per_hvl=1,
    weak_factor=3
    )
    du.material_energy_density_j_per_hvl=estfix(du)
    return du
    
def getcf():
    cf=Material(
    name="CF",
    molar_mass_g_mol=12,
    density_kg_m3=1930,
    atomic_radius_m=77e-12,
    atomic_number=6,
    cohesive_energy_ev=7.37,
    base_hvl_cm=7.33,
    material_energy_density_j_per_hvl=1,
    weak_factor=1
    )
    cf.material_energy_density_j_per_hvl=estfix(cf)
    return cf

dn=1.25

def getn():
    n=Material(
    name="N",
    molar_mass_g_mol=14,
    density_kg_m3=dn,
    atomic_radius_m=7e-11,
    atomic_number=7,
    cohesive_energy_ev=1,
    base_hvl_cm=((getsteel().density/dn))*getsteel().base_hvl_cm,
    material_energy_density_j_per_hvl=1,
    weak_factor=1
    )
    return n
    
def getmht(self):
    ht=getht(self)
    n=getn()
    return ht*(n.density/getsteel().density)
    
def getht(self):
    molv=self.density*self.molar_mass/1_000_000
    molv=molv*self.avogadro
    molv=molv**(2/3)
    ar=self.atomic_radius
    mp=getmp(self)
    v=getvel(self,mp)
    v=v**(1/3)
    t=v/ar
    am=amass(self)*molv
    ke=.5*(v*v)*am
    w=t*ke
    w=math.sqrt(self.emr)*w
    return w
    
def amass(self):
    return (self.molar_mass/1000)/self.avogadro

def getvel(self,t):
    s=3*self.bol*t
    m=(self.molar_mass/1000)/self.avogadro
    return math.sqrt(s/m)

def getmp(self):
    ce=self.cohesive_bond_energy
    ce=ce/6
    sh=getsh(self)
    return ce/sh

def getsh(self):
    sh=self.db
    ker=1000/self.molar_mass
    sh=ker*sh
    return sh
    
    

# Example usage:
if __name__ == "__main__":    
    steel=getsteel()
    du=getdu()
    cf=getdu()
    steel.print_summary()
    rspeed=cf.gets()
    round_diameter = cf.getdam() # cm
    round_mas=cf.getmass(round_diameter)
    print("mass",round_mas)
    round_energy = (.5*round_mas*(rspeed**2))
    print("energy j ",round_energy)
    angle_vert = 90
    angle_horz = 90

    depth= getsteel().penetration_depth(round_energy, round_diameter, angle_vert, angle_horz,0,round_mas)
    print(f"Penetration depth: {depth:.2f} cm")
  
    

    
    
    

