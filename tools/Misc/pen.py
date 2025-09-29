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
        
     
        self.avogadro = 6.02214076e23
        self.k = 9e9  
        self.elementary_charge = 1.60217663047908e-19
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
        self.crad=7e-11*1.001001777
        self.req=6378137
       
        self.bafac=1
        self.f2=1
        self.f3=1
        self.f4=1
        self.fill=1
                  
        
        self.j_high_estimate = (self.compute_high_estimate() ** 0.5)*self.f4
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
    	
    def getearth(self):
    	f=self.geth()
    	#emass=5.9722e24
    	f=f*self.av/6/(1+1/(16+1/2.2))
    	return f
    	
    def geth(self):
    	f=(self.av*3)*(nuct.alpha**nuct.phi)*8
    	f=f/self.avogadro/1000
    	return f
    	 
    def getsec(self):
    	c=nuct.c
    	pm=self.getpl()
    	pm=c/pm
    	pm*=3    	
    	return pm
    	
        	
    def getpl(self):
    	pm=nuct.pm*1000*self.avogadro*self.crad
    	return pm
    	
    def getbigg(self):
    	return self.getg()*self.req*self.req/self.getearth()
    	
    def getg(self):
    	req=self.req
    	pl=self.getpl()
    	amf=self.am
    	corr=(1/amf/(2/3)/nuct.alpha/(1+1/(24+(1/(2+(((1-(1/(8.1))))/2))))))
    	gg=pl*corr
    	gg*=self.getsec()
    	ff=pl/req
    	ff**=2
    	ff*=(1/gg)
    	ff/=1+6/amf
    	return ff
    
    def compute_high_estimate(self):
        ch = self.ch
        ch *= self.atomic_number
        ac = self.avogadro * ch
        moles = 1000 / self.molar_mass
        re = moles * ac
        re=re/self.weak_factor
        return re
    
    def compute_cohesive_bond_energy(self):
        mass_g = 1000  
        moles = mass_g / self.molar_mass
        atoms = moles * self.avogadro
        bond_energy_per_atom_j = self.cohesive_energy_ev * self.ev_to_joule
        total_bond_energy_joules = atoms * bond_energy_per_atom_j
        return total_bond_energy_joules

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
        r=self.thermalpen(round_energy)
        if(d==-1):
        	return r
        if(d>r):
            print("A ",d,"cm penetration was thermally bound to ", r,"cm.")
            return r
        print("A ", d,"cm penetration did not reach thermal bound ", r,"cm.")
        return d
        
    def thermalpen(self,round_energy):
    	f=self.melt_one_hvl()
    	hv=self.base_hvl_cm
    	r=(round_energy)/(f*hv)
    	return r

    def penetration_depth(self, round_energy, round_diameter_cm, angle1, angle2, honeycomb_layers,round_mas,roundmaterial):
        effective_angle = self.combine_angles(angle1, angle2)
        #pm = nuct.NuclearPenetrationModel(self)
        #d=nuct.nuclear_penetration(round_energy,round_diameter_cm,honeycomb_layers,round_mas,pm.material,roundmaterial)
        d=-1
        d=self.thermal_max_pen(d,round_energy)
        d = self.pen_angle(d, effective_angle, round_energy, round_diameter_cm)
        d=self.honeycomb_pen(d,round_energy,round_diameter_cm,honeycomb_layers)
        return d

    def pen_angle(self, d, angle, round_energy, round_diameter_cm):
        if(angle==0):
            return 0
        r = 90 / angle
        r = r ** (4 ** self.phi)
        d = d / r
        d= self.base_pen(d, round_energy, round_diameter_cm)
        return d
        
    def getvel(self,round_diameter1):
        mp=getmp(self)
        ht=getmht(self)
        n=getn()
        round_diameter1=round_diameter1/100
        ra=round_diameter1**2
        airperhit=n.density*ra
        aireng=airperhit*getsh(n)*mp
        airvol=self.velfromen(airperhit,aireng)
        airenpers=aireng*airvol
        ht=airenpers/(ht*mp)
        ba=ht/airvol
        roundside=ra*4
        ba=ba/roundside
        if(self.bafac==1):
        	return ba,airvol
        return self.bafac,airvol

    def gets(self):
        round_diameter1=self.getdam()
        f,d=self.getvel(round_diameter1)
        return d
        
    def getmass(self,round_diameter1):
        ld,s=self.getvel(round_diameter1)
        round_diameter1=round_diameter1/100
        round_diameter1=round_diameter1*round_diameter1*round_diameter1
        d=self.density
        ff=round_diameter1*ld*d*self.fill
        return ff
        
    def getbarrelmat(self):
    	return getsteel()
    	
    def getbarrellen(self,rounde,roundl,speed):
    	fine=nuct.alpha
    	if(speed==1):
    		fine=fine
    	else:
    			maxs=self.gets()
    			speed=speed/maxs
    			fine=1-speed
    			if(fine==0):
    				fine=nuct.alpha
    	mpb=getmp(self)
    	mpr=getmp(rounde)
    	rat=mpb/mpr
    	logl=math.log2(fine)*-1
    	return rat*logl*roundl
    	
    def getbarrelmass(self,rounde,roundl,diam,speed):
    	thick=self.base_hvl_cm
    	massper=self.density/1_000_000
    	lenn=self.getbarrellen(rounde,roundl,speed)
    	side=massper*thick*lenn*diam
    	return side*4/1000
    
    def getdam(self):
        barrel=self.getbarrelmat()
        maxd=barrel.base_hvl_cm
        doh=barrel.material_energy_density_j_per_hvl
        if(self.f2==1):
        	return self.damiter(maxd,doh)
        return self.f2

    def damiter(self,maxd,doh):
        basevel=self.getmass(maxd)
        ff,bases=self.getvel(maxd)
        en=self.enfromvel(basevel,bases)
        r=doh/en
        r=r**.5
        return r*maxd
        
    def getroundlenmass(self,mass,diam):
        dens=self.density/1_000_000
        firstd=diam*diam*dens
        lens=mass/firstd
        return lens/self.fill
    
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
        angle = angle % 180
        if angle > 90:
        	angle = 180 - angle
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
        
def cohfrommp(mp):
		he=(getsteel().db*mp)/getsteel().avogadro
		he=he/getsteel().ev_to_joule
		return he*2*zrule()
		
def zrule():
	return 6

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
rpmo=16
rp1z=8
rpsolidfrac=0.1
rp1tendensity=1400
waterfrac=.9
invw=1-waterfrac

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
    
def getrp1tenpct():
    rp1tenpct=Material(
    name="RP1tenpct",
    molar_mass_g_mol=rpmo,
    density_kg_m3=rp1tendensity,
    atomic_radius_m=6e-11,
    atomic_number=rp1z,
    cohesive_energy_ev=cohfrommp(60/((1/rpsolidfrac)**2)),
    base_hvl_cm=10,
    material_energy_density_j_per_hvl=1,
    weak_factor=(((getsteel().density)/rp1tendensity)**6)*nuct.alpha.evalf()*(1/rpsolidfrac)
    )
    rp1tenpct.material_energy_density_j_per_hvl=estfix(rp1tenpct)   
    return rp1tenpct
            
def getskin():
    skin=Material(
    name="Organic",
    molar_mass_g_mol=1,
    density_kg_m3=1000,
    atomic_radius_m=5.3e-11,
    atomic_number=1,
    cohesive_energy_ev=-8,
    base_hvl_cm=4,
    material_energy_density_j_per_hvl=1,
    weak_factor=((1/invw)**2)**2
    )
    skin.material_energy_density_j_per_hvl=estfix(skin)
    return skin
    
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
    ce=ce/zrule()
    sh=getsh(self)
    return ce/sh/2/(self.f3**2)
    #at 1.55kms 25mm ld 29
    #28cm pen du vs steel
    #863mpa wikipedia rha
    #68cm pen

def getsh(self):
    sh=self.db
    ker=1000/self.molar_mass
    sh=ker*sh
    return sh
    

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
    	return mat
    
    def getspeed(mat):
    	mat=basevals(mat)
    	return mat.gets()
    	
    def getstr(mat):
    	mat=basevals(mat)
    	return mat.j_high_estimate
    	
    def bhn250():
    	mat=basevals(getsteel())
    	return (863*10**6)/mat.j_high_estimate
    	
    def do10gel():
    	mat=basevals(getsteel())
    	gel=getrp1tenpct()
    	return gel.j_high_estimate/mat.j_high_estimate
    	
    strength=bhn250()
    gels=do10gel()
    
    def do2mm():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=3.5
    	cf.f2=.27
    	cf.f3=speed/200
    	cf.f4=strength
    	dopen(cf)
    	
    def dopaintball():
    	cfa=steel
    	cfa.density=1900
    	speed=getspeed(cfa)
    	cfa.bafac=1.1
    	cfa.f2=1.8
    	cfa.f3=speed/60
    	cfa.f4=strength
    	dopen(cfa)
    	
    def dorubber():
    	cfa=steel
    	cfa.density=1900
    	speed=getspeed(cfa)
    	cfa.bafac=4
    	cfa.f2=3.7
    	cfa.f3=speed/60
    	cfa.f4=strength
    	dopen(cfa)
    
    def do25acp():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=2.5
    	cf.f2=.635
    	cf.f3=speed/230
    	cf.f4=strength
    	dopen(cf)
    
    def do22long():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=2.6
    	cf.f2=.57
    	cf.f3=speed/370
    	cf.f4=strength
    	dopen(cf)
    
    def do9mm():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=2
    	cf.f2=.9
    	cf.f3=speed/376
    	cf.f4=strength
    	dopen(cf)
    	print("19mm drop in .5mpa clay is .01mm steel. 2000x clay steel ratio is .15mm for 30cm clay.")
    	
    def do44():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=3
    	cf.f2=1.09
    	cf.f3=speed/470
    	cf.f4=strength
    	dopen(cf)
    	print("actual 5mm plate. cavity exceeds hvl and enters new regime")
    
    def do556():
    	cf=du
    	speed=getspeed(cf)	
    	cf.bafac=8.1
    	cf.f2=.556
    	cf.f3=speed/994
    	cf.f4=strength
    	dopen(cf)
    	print("actual 1.5 (scaled from magnun).")
    	
    def do762():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=6.7
    	cf.f2=.762
    	cf.f3=speed/856
    	cf.f4=strength
    	dopen(cf)
    	print("actual 1.5 (scaled from magnum) ")
    	
    def do3006():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=8.25
    	cf.f2=.762
    	cf.f3=speed/890
    	cf.f4=strength
    	dopen(cf)
    	print("actual 1.5 (scaled from mangum")
    	
    	
    def do50cal():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=7.8
    	cf.f2=1.27
    	cf.f3=speed/(860)#explosive
    	cf.f4=strength
    	dopen(cf)
    	print("actual 2.3")
    	
    def dobradley():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=5.5
    	cf.f2=2.5
    	cf.f3=speed/1385
    	cf.f4=strength
    	cf.fill=(100/1670)
    	dopen(cf)
    	cf.fill=1
    	print("actual 10.1")
    	
    def dosherman():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=7.07
    	cf.f2=7.6
    	cf.f3=speed/(792)#explosive
    	cf.f4=strength
    	dopen(cf)
    	print("actual 23.9")
    
    def do88():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=10
    	cf.f2=8.8
    	cf.f3=speed/773
    	cf.f4=strength
    	cf.fill=.25
    	dopen(cf)    	
    	print("actual 17")
    	
    def do122():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=3.28
    	cf.f2=12.2
    	cf.f3=speed/780
    	cf.f4=strength
    	cf.fill=.5
    	dopen(cf)
    	print("actual 17")
    	
    def do3vmb3():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=10
    	cf.f2=4.1
    	cf.f3=speed/(1800*.85)
    	cf.f4=strength
    	cf.fill=1
    	dopen(cf)	
    	print("actual 25cm")
    	
    def do3bm7():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=12
    	cf.f2=3.6
    	cf.f3=speed/(1785)
    	cf.f4=strength
    	cf.fill=1
    	dopen(cf)
    	print("actual 40cm")
    	
    def do3vbm17():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=17
    	cf.f2=3.1
    	cf.f3=speed/(1700*.85)
    	cf.f4=strength
    	cf.fill=.3
    	dopen(cf)
    	print("actual 52cm")
    	
    def dosvinets():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=21.84
    	cf.f2=2.5
    	cf.f3=speed/(1700*.85)
    	cf.f4=strength
    	cf.fill=.3
    	dopen(cf)
    	print("actual 66cm")
    	
    def dotapna():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=29
    	cf.f2=2.5
    	cf.f3=speed/1690
    	cf.f4=strength
    	cf.fill=.3
    	dopen(cf)
    	print("actual 63cm")
    	
    def do5():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=5.35
    	cf.f2=12.7
    	cf.f3=speed/790
    	cf.f4=strength
    	cf.fill=.25
    	dopen(cf)
    	print("actual 13cm")
    	
    def do6():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=4.5
    	cf.f2=15
    	cf.f3=speed/640
    	cf.f4=strength
    	cf.fill=.5
    	dopen(cf)
    	print("actual 30cm")
    	
    def do8():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=4.06
    	cf.f2=20
    	cf.f3=speed/(823)
    	cf.f4=strength
    	cf.fill=.5
    	dopen(cf)
    	print("actual 40cm")
    	
    def do16():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=4.5
    	cf.f2=41
    	cf.f3=speed/762
    	cf.f4=strength
    	cf.fill=.5
    	dopen(cf)
    	print("actual 75cm")
    	
    

    def lethalcalc(mat,en):
    	sk=getskin()
    	sken=sk.material_energy_density_j_per_hvl/(2**nuct.phi.evalf()**6)
    	if(en<sken):
    		print("round not lethal")
    		return 0
    	mel=mat.melt_one_hvl()
    	en=en/mel
    	sken=sken/mel
    	hvls=en/sken
    	ar=mat.base_hvl_cm
    	hvls**=(1/12)
    	hvls=hvls*ar
    	print("round lethal at armor cm",hvls)
    	return hvls
    	
    	
    
    def dopen(mat):
    	print("")
    	rspeed=mat.gets()
    	round_diameter = mat.getdam()
    	round_mas=mat.getmass(round_diameter)
    	round_len=mat.getroundlenmass(round_mas,round_diameter)
    	print("mass",round_mas)
    	round_energy = (.5*round_mas*(rspeed**2))
    	print("energy j ",round_energy)
    	angle_vert = 90
    	angle_horz = 90
    	armor=steel
    	if(round_diameter==.9):
    		armor=getrp1tenpct()
    		armor.base_hvl_cm=round_diameter*2	
    	hvl=armor.base_hvl_cm*zrule()
    	mult=1
    	if(round_diameter>hvl):
    		mult=round_diameter/hvl
    	mult=mult**2
    	armor.material_energy_density_j_per_hvl=mat.f4*estfix(steel)
    	depth= 1#armor.penetration_depth(round_energy, round_diameter, angle_vert, angle_horz,0,round_mas,mat)
    	th=armor.thermalpen(round_energy)
    	depth=th
    	depth=depth/mult
    	ld=mat.getroundlenmass(round_mas,round_diameter)
    	print("ld ",ld/round_diameter)
    	print(f"Penetration depth: {depth:.2f} cm")
    	lethalcalc(armor,round_energy)
    	lenn=getsteel().getbarrellen(mat,mat.getroundlenmass(round_mas,round_diameter),rspeed)
    	print("barrel length cm ",lenn*(1))
    	
    
    dopen(cf)
    do2mm()
    dopaintball()
    dorubber()
    do25acp()
    do22long()
    do9mm()
    do44()
    do556()
    do762()
    do3006()
    do50cal()
    dobradley()
    dosherman()
    do88()
    do122()
    do3vmb3()
    do3bm7()
    do3vbm17()
    dosvinets()
    dotapna()
    do5()
    do6()
    do8()
    do16()
    n=nuct.baseobj()
    n.getpow()
    
  
    

    
    
    

