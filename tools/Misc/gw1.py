import math
import nuct
import sympy as sp
import cons

mass_g=cons.mass_g
cm_m=cons.cm_m
req=cons.req
crad=cons.crad
avo=cons.avo
ec=cons.ec

class Material:
    def __init__(self, name, molar_mass_kg_mol, density_kg_m3, atomic_radius_m, atomic_number,
                cohesive_energy_ev, base_hvl, material_energy_density_j_per_hvl, weak_factor=1):
        self.name = name
        self.molar_mass = molar_mass_kg_mol
        self.density = density_kg_m3
        self.atomic_radius = atomic_radius_m
        self.atomic_number = atomic_number
        self.cohesive_energy_ev = cohesive_energy_ev
        self.base_hvl = base_hvl
        self.material_energy_density_j_per_hvl = material_energy_density_j_per_hvl
        self.weak_factor = weak_factor
            
        self.avogadro = avo
        self.k = 8987551752.21422
        self.elementary_charge = ec
        self.ev_to_joule = self.elementary_charge
        self.phi = nuct.phi
        self.ch=(self.elementary_charge ** 2) * self.k / (self.atomic_radius ** 2)
        self.ch1=self.ch*self.atomic_radius
        self.bol=1.380649e-23
        self.db=24.94
        self.zc=273.15
        self.pmas=nuct.prma/2
        self.emr=nuct.alpha**nuct.phi
        self.emr=self.emr/nuct.phi
        self.crad=crad
        self.req=req
       
        self.bafac=1
        self.f2=1
        self.f3=1
        self.f4=1
        self.fill=1
        self.exp=0
                  
        
        self.j_high_estimate = (self.compute_high_estimate())*self.f4
        self.cohesive_bond_energy = self.compute_cohesive_bond_energy()
        self.elmol=self.elementary_charge*self.avogadro
        self.elmol=self.elmol**(1/4)
        self.elmol*=self.phi
        self.te=1-(1/(8))
        self.elmol*=self.te
        self.db=self.elmol
        self.av=(((nuct.alpha**nuct.phi)**7)/3)
        self.am=nuct.alpha**nuct.phi
        
    
    def getrange(self,round_mas,diam):
    	airdens=getn().density
    	de=self.density*self.fill
    	lenn=self.getroundlenmass(round_mas,diam)
    	de=self.density/airdens
    	return lenn*de

    
    def compute_high_estimate(self):
        ch = self.ch
        ac = self.avogadro * ch
        moles = mass_g/ self.molar_mass
        re = moles * ac
        re=re/self.weak_factor
        mo=(4*sp.pi)-6
        mo**=nuct.phi
        re**=.5
        re/=mo
        return re
    
    def compute_cohesive_bond_energy(self):
        moles = mass_g / self.molar_mass
        atoms = moles * self.avogadro
        bond_energy_per_atom_j = self.cohesive_energy_ev * self.ev_to_joule
        total_bond_energy_joules = atoms * bond_energy_per_atom_j
        return total_bond_energy_joules/mass_g

    def print_summary(self):
        print(f"Cohesive bond energy total (J): {self.cohesive_bond_energy:.4e}")
        print(f"Cohesive bond energy total (MJ): {self.cohesive_bond_energy / 1e6:.4f}")

    def combine_angles(self, angle1_deg, angle2_deg):
        a1=self.clean_angle(angle1_deg) 
        a2=self.clean_angle(angle2_deg) 
        f2=90-a2 
        r=f2/90 
        r=1-r
        r=(a1)*r
        return min(r, 90)
    
    def hvl_mass_kg(self):
        h=self.base_hvl
        dens=self.density
        v=h**3
        m=v*dens
        return m
    
    def melt_one_hvl(self):
        h=self.hvl_mass_kg()
        bo=self.cohesive_bond_energy
        bo=h*bo
        return bo
        
    def thermal_max_pen(self,d,round_energy):
        r=self.thermalpen(round_energy)
        if(d==-1):
        	return r
        if(d>r):
            print("A ",d,"cm penetration was thermally bound to ", r,"cm.")
            return r
        print("A ", d,"cm penetration did not reach thermal bound ", r,"cm.")
        return d
        
    def thermalpen(self,round_energy):
    	return self.thermalpenexp(round_energy,0)
    
    def thermalpenexp(self,round_energy,exp):
    	f=self.melt_one_hvl()
    	hv=self.base_hvl
    	r=(round_energy/f)*hv/nuct.phi
    	r/=nuct.picor
    	return self.doexp(r,exp)
    	
    def doexp(self,r,exp):
    	if(exp==0):
    		return r
    	exp=self.exen(exp)
    	f1=self
    	f1.exp=0
    	d=f1.thermalpen(exp)
    	return r+d
    	
    def exen(self,exp):
    	rdxdens=5330e3
    	exp*=rdxdens
    	return exp    	
    	
    def penetration_depth(self, round_energy, round_diameter, angle1, angle2, honeycomb_layers):
        effective_angle = self.combine_angles(angle1, angle2)
        d=-1
        d=self.thermal_max_pen(d,round_energy)
        d = self.pen_angle(d, effective_angle, round_energy, round_diameter)
        d=self.honeycomb_pen(d,round_energy,round_diameter,honeycomb_layers)
        return d

    def pen_angle(self, d, angle, round_energy, round_diameter):
        if(angle==0):
            return 0
        r = 90 / angle
        r = r ** (4 ** self.phi)
        d = d / r
        d= self.base_pen(d, round_energy, round_diameter)
        return d
        
    def getvel(self,round_diameter1):
        ba,airvol=self.getvol(round_diameter1)
        if(self.bafac==1):
        	v1=airvol
        	ba,airvol=self.domaxld(ba,airvol)
        	v1/=airvol
        	ba/=v1
        	return ba,airvol,v1
        return self.bafac,airvol,1
    
    def getvol(self,round_diameter1):
       airvol,ht,ra=self.getv(round_diameter1)
       ba=self.getba(ht,ra)
       return ba,airvol
       
    def getv(self,round_diameter1):
       mp=getmp(self)
       ht=getmht(self)
       airvol,ht,ra=self.getairvol(ht,mp,round_diameter1)
       return airvol,ht,ra
       
    def getba(self,ht,ra):
       ba=ht
       roundside=ra*nuct.sp.pi
       ba=ba/roundside
       return ba
       
    def getairvol(self,ht,mp,ra):
        airvol=self.getav(ra,mp)
        ht=self.getairen(mp,ra)/(ht*mp)
        return airvol,ht,ra**2
    
    def getav(self,ra,mp):
        aireng= self.getairen(mp,ra)
        airvol=self.velfromen(self.getaph(ra),aireng)
        return airvol
        
    def getairen(self,mp,ra):
        n=getn()
        airperhit=self.getaph(ra)
        return airperhit*getsh_per_kg(n)*mp
        
    def getaph(self,ra):
        n=getn()
        return n.density*(ra**2)*nuct.picor
        
    def domaxld(self,ba,airvol):
    	ba1=ba
    	ba=self.barmm(0,ba)
    	diff=ba1/ba
    	diff**=1/3
    	airvol/=diff
    	return ba,airvol

    def gets(self,isbarrel):
        round_diameter1=self.getdam(isbarrel)
        d=self.getav(round_diameter1,getmp(self))
        return d
        
    def getmass(self,round_diameter1,ld):
        round_diameter1=round_diameter1*round_diameter1*round_diameter1
        d=self.density
        ff=round_diameter1*ld*d*self.fill
        return ff*nuct.picor
        
    def getbarrelmat(self,isbarrel):
    	if(isbarrel==1):
    		return getsteel()
    	return self
    	
    def getbarrellen(self,rounde,roundl,speed,diam):
    	fine=nuct.alpha
    	if(speed==1):
    		pass
    	else:
    			maxs=self.gets(1)
    			speed=speed/maxs
    			fine=1-speed
    			if(fine<=0):
    				fine=nuct.alpha
    	mpb=getmp(self)
    	mpr=getmp(rounde)
    	rat=mpb/mpr
    	logl=math.log2(fine)
    	logl=abs(logl)  
    	f= rat*roundl*logl
    	d1=7.85/(1.51)
    	d1*=1.27/cm_m	
    	cut=d1*2
    	if(diam>cut):
    		foo=diam/cut
    		foo**=2/3
    		f=f*foo
    	return f
    	
    def getbarrelmass(self,rounde,roundl,diam,speed):
    	thick=self.base_hvl
    	massper=self.density
    	lenn=self.getbarrellen(rounde,roundl,speed,diam)
    	side=massper*thick*lenn*diam*nuct.picor
    	return side*nuct.sp.pi
    
    def getdam(self,isbarrel):
        if(self.f2==1):
        	return self.damiter(isbarrel)
        return self.f2   
        
    def barm(self,isbarrel):
    	return self.barmm(isbarrel,1)
    	
    def barmm(self,isbarrel,ba):	
        baro=self.getbaro()
        ba1=ba
        if(isbarrel==1):
        	return baro
        ba=self.barhvl(baro**.5,isbarrel)
        r=self.getbuc(ba,ba1)
        if(r>1):
        	print("ld not limited ",sp.N(r))
        	r=1
        res=ba1*(r**.5)
        return res

    def getbuc(self,ba,ba1):
    	ba1=self.barhvl(ba1,0)
    	r=ba/2
    	r**=4
    	r*=sp.pi/4
    	r*=(sp.pi**2)
    	ba*=2
    	ba**=2
    	ba*=nuct.picor
    	r/=(ba1**2)*ba
    	return r
    	
    	
    def getbaro(self):
    	b=self.getbarrelmat(1)
    	ben=b.getben()
    	return ben
    	
    def getben(self):
    	maxd=self.base_hvl
    	mm=self.hvl_mass_kg()
    	mp=getmp(self)
    	av=self.getav(maxd,mp)
    	ben=self.enfromvel(mm,av)
    	doh=self.material_energy_density_j_per_hvl
    	return doh/ben
 
   
    def damiter(self,isbarrel):
        r=self.barm(isbarrel)
        r=r**(.5)
        return self.barhvl(r,isbarrel)
        
    def barhvl(self,r,isbarrel):
        return r*self.getbarrelmat(isbarrel).base_hvl
        
    def getroundlenmass(self,mass,diam):
        dens=self.density
        firstd=diam*diam*dens*nuct.picor
        lens=mass/firstd
        return lens/self.fill
    
    def enfromvel(self,mass,vel):
        return .5*mass*vel*vel
    
    def velfromen(self,mass,en):
        return math.sqrt(2 * (en / mass))
    
    
    def honeycomb_pen(self,d,round_energy_mj,round_diameter,layers):
        if(layers==0):
            return d
        l=(layers*2)**2
        r=90/l
        d=self.pen_angle(d,r,round_energy_mj,round_diameter)
        d=self.base_pen(d,round_energy_mj,round_diameter)
        return d
            
    def clean_angle(self, angle):
        angle = angle % 180
        if angle > 90:
        	angle = 180 - angle
        return angle

    def base_pen(self, d, round_energy_j, round_diameter):
        e = self.sectional_energy_density(round_energy_j, round_diameter)
        m = self.material_energy_density_j_per_hvl
        m= (e/m)*self.base_hvl
        if(m>d):
            return m
        return d

    def sectional_energy_density(self, round_energy_j, round_diameter):
        if round_diameter< self.base_hvl:
            return round_energy_j / (self.base_hvl** 2)
        return round_energy_j / ((round_diameter/self.base_hvl) ** 2)

def estfix(self):
        return (self.j_high_estimate*self.hvl_mass_kg())
        
def cohfrommp(mp):
		he=(getsteel().db*mp)/getsteel().avogadro
		he=he/getsteel().ev_to_joule
		return he*2*zrule()
		
def zrule():
	return 6

def getsteel():
    steel = Material(
        name="Iron (Steel)",
        molar_mass_kg_mol=55.85/mass_g,
        density_kg_m3=7850,
        atomic_radius_m=126e-12,
        atomic_number=26,
        cohesive_energy_ev=4.28,
        base_hvl=1.27/cm_m,
        material_energy_density_j_per_hvl=1,
        weak_factor=1
    )
    steel.material_energy_density_j_per_hvl=estfix(steel)
    return steel
    
def getdu():
    du=Material(
    name="Uranium",
    molar_mass_kg_mol=238/mass_g,
    density_kg_m3=19500,
    atomic_radius_m=175e-12,
    atomic_number=92,
    cohesive_energy_ev=5.06,
    base_hvl=0.03/cm_m,
    material_energy_density_j_per_hvl=1,
    weak_factor=3
    )
    du.material_energy_density_j_per_hvl=estfix(du)
    return du
    
def getcf():
    cf=Material(
    name="CF",
    molar_mass_kg_mol=12/mass_g,
    density_kg_m3=1930,
    atomic_radius_m=77e-12,
    atomic_number=6,
    cohesive_energy_ev=7.37,
    base_hvl=7.33/cm_m,
    material_energy_density_j_per_hvl=1,
    weak_factor=1
    )
    cf.material_energy_density_j_per_hvl=estfix(cf)
    return cf

dn=1.25
rpmo=16
rp1z=8
rpsolidfrac=0.1
rp1tendensity=1400
waterfrac=.9
invw=1-waterfrac

def getn():
    n=Material(
    name="N",
    molar_mass_kg_mol=14/mass_g,
    density_kg_m3=dn,
    atomic_radius_m=7e-11,
    atomic_number=7,
    cohesive_energy_ev=1,
    base_hvl=(getsteel().density/dn)*getsteel().base_hvl,
    material_energy_density_j_per_hvl=1,
    weak_factor=1
    )
    return n
    
def getrp1tenpct():
    rp1tenpct=Material(
    name="RP1tenpct",
    molar_mass_kg_mol=rpmo/mass_g,
    density_kg_m3=rp1tendensity,
    atomic_radius_m=6e-11,
    atomic_number=rp1z,
    cohesive_energy_ev=cohfrommp(60),
    base_hvl=10/cm_m,
    material_energy_density_j_per_hvl=1,
    weak_factor=(((getsteel().density)/rp1tendensity)**6)*nuct.alpha*(1/rpsolidfrac)
    )
    rp1tenpct.material_energy_density_j_per_hvl=estfix(rp1tenpct)   
    return rp1tenpct
            
def getskin():
    skin=Material(
    name="Organic",
    molar_mass_kg_mol=1,
    density_kg_m3=1000,
    atomic_radius_m=5.3e-11,
    atomic_number=1,
    cohesive_energy_ev=-8,
    base_hvl=4/cm_m,
    material_energy_density_j_per_hvl=1,
    weak_factor=((1/invw)**2)**2
    )
    skin.material_energy_density_j_per_hvl=estfix(skin)
    return skin
    
def getmht(self):
    ht=getht(self)
    return ht
    
def getht(self):
    nm=(self.molar_mass/self.density)/getn().density
    side=nm**(1/3)
    ac=self.avogadro**(2/3)
    mp=getmp(self)
    vel=getvel(self,mp)
    ar=self.atomic_radius*2
    vf=vel/ar
    vf**=2/3
    va=vf*ar
    en=.5*va*va*amass(self)
    en*=ac
    t=vf*en
    t*=(1/side)/2
    r=self.avogadro/self.av
    r**=2/3
    t/=r
    ref=nuct.baseobj().am**3
    ref/=3
    corr=(1/getsteel().atomic_radius)/ref
    t/=corr
    return t
    
def amass(self):
    return (self.molar_mass*mass_g)/self.avogadro

def getvel(self,t):
    s=3*self.bol*t*self.avogadro
    m=self.molar_mass
    return math.sqrt(s/m)

def getmp(self):
    ce=self.cohesive_bond_energy
    ce=ce/zrule()
    sh=getsh_per_kg(self)
    sh=ce/sh/2/(self.f3**2)
    return sh

def getsh_per_kg(self):
    sh=self.db
    ker=self.molar_mass
    return sh/ker

if __name__ == "__main__":   
    steel=getsteel()
    du=getdu()
    cf=getrp1tenpct()
    steel.print_summary()
   
    
    
    def basevals(mat):
    	mat.bafac=1
    	mat.f2=1
    	mat.f3=1
    	mat.f4=1
    	mat.fill=1
    	mat.exp=0
    	return mat
    
    def getspeed(mat):
    	mat=basevals(mat)
    	return mat.gets(1)
    	
    def getstr(mat):
    	mat=basevals(mat)
    	return mat.j_high_estimate
    	
    def lethalcalc(mat,en,exp):
    	sk=getskin()
    	sken=sk.material_energy_density_j_per_hvl/(2**nuct.phi**6)
    	en+=sk.exen(exp)
    	if(en<sken):
    		print("round not lethal")
    		return 0
    	mel=mat.melt_one_hvl()
    	en=en/mel
    	sken=sken/mel
    	hvls=en/sken
    	ar=mat.base_hvl
    	hvls**=(1/12)
    	hvls=hvls*ar
    	print("round lethal at armor cm",hvls.evalf()*cm_m)
    	return hvls
    	
    	
    
    def dopen(mat):
    	print("")
    	round_diameter = mat.getdam(1)
    	ld,rspeed,mm=mat.getvel(round_diameter)
    	round_diameter*=mm
    	round_mas=mat.getmass(round_diameter,ld)    	
    	print("round",sp.N(round_diameter*cm_m))
    	print("mass",round_mas.evalf())
    	round_energy = (.5*round_mas*(rspeed**2))
    	print("energy j ",round_energy.evalf())
    	print("speed",sp.N(rspeed))
    	armor=steel
    	if(round_diameter==.009):
    		armor=getrp1tenpct()
    		armor.base_hvl=round_diameter*2	
    	hvl=armor.base_hvl*zrule()
    	mult=1
    	if(round_diameter>hvl):
    		mult=round_diameter/hvl
    	mult=mult**2
    	armor.material_energy_density_j_per_hvl=mat.f4*estfix(steel)
    	depth= 1
    	exer=mat.exp
    	if(exer!=0):
    		print("fill",mat.fill)
    		pcte=mat.exp/round_mas
    		rdxdens=mat.density/1600
    		print("exp pct",pcte.evalf()*rdxdens)
    	th=armor.thermalpenexp(round_energy,mat.exp)
    	depth=th
    	depth=depth/mult
    	print("ld ",sp.N(ld))
    	print(f"Penetration depth: {depth*100:.2f} cm")
    	lethalcalc(armor,round_energy,exer)
    	lenn=getsteel().getbarrellen(mat,mat.getroundlenmass(round_mas,round_diameter),rspeed,round_diameter)
    	print("barrel length cm ",lenn.evalf()*cm_m)
    	
    
dopen(steel)