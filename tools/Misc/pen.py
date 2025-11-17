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
        mo*=6
        ff=nuct.baseobj().am**(2)
        re/=ff
        re*=self.base_hvl
        return re/mo
    
    def compute_cohesive_bond_energy(self):
        moles = mass_g / self.molar_mass
        atoms = moles * self.avogadro
        bond_energy_per_atom_j = self.cohesive_energy_ev * self.ev_to_joule
        total_bond_energy_joules = atoms * bond_energy_per_atom_j
        return total_bond_energy_joules/mass_g

    def print_summary(self):
        pass

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
        
    def pen(self,mat,angle1,angle2):
    	effective_angle = mat.combine_angles(angle1, angle2)
    	rd,speed,mass,en=self.getroundparam(mat)
    	en=.5*mass*(speed**2)
    	armor=self
    	hvl=armor.base_hvl*zrule()
    	mult=1
    	if(rd>hvl):
    		mult=rd/hvl
    	mult=mult**2
    	armor.material_energy_density_j_per_hvl=mat.f4*estfix(armor)
    	th=self.thermalpen(en)
    	th=self.pen_angle(th,effective_angle,en,rd)
    	return th/mult
    	
    def barrellen(self,mat):
    	rd,speed,mass,en=self.getroundparam(mat)
    	lenn=getsteel().getbarrellen(mat,mat.getroundlenmass(mass,rd),speed,rd)
    	return lenn,rd
    	
    def getroundparam(self,mat):
    	rd=self.getdam(1)
    	ld,speed,mm=mat.getvel(rd)
    	rd*=mm
    	mass=mat.getmass(rd,ld)
    	en=.5*mass*(speed**2)
    	return rd,speed,mass,en

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
       ht=getht(self)
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
    	d1=(getsteel().density)/(1510)
    	d1*=getsteel().base_hvl
    	cut=d1*2
    	if(diam>cut):
    		foo=diam/cut
    		foo**=2/3
    		f=f*foo
    	return f
    	
    def getbarrelmass(self,rounde,roundl,diam,speed):
    	lenn=self.getbarrellen(rounde,roundl,speed,diam)
    	return self.getfinbar(lenn,diam)
    	
    def getbarmass(self,mat):
    	lenn,diam=self.barrellen(mat)
    	return self.getfinbar(lenn,diam)
    	
    def getfinbar(self,lenn,diam):
    	mm=self.getbarrelmat(1)
    	return mm.density*((mm.base_hvl*lenn)-(sp.pi*(mm.base_hvl**2)))*(diam/2)
    	
    def getparp(self,barmass,mat):
    	bm=self.getbarmass(mat)
    	rd,speed,mass,en=self.getroundparam(mat)
    	#lm=mat.getlm(mass,rd)
    	#bf=self.getbarrelmass(mat,lm,rd,speed)
    	m1=mass
    	if(bm<barmass):
    		return rd,speed,mass,en
    	r=bm/barmass
    	maxs=mat.gets(0)
    	rf=(r**(11/12))/r
    	if(speed==maxs):
    		pass
    	else: 
    	    speed*=rf
    	rm=r**(5/4)
    	mass/=rm
    	rd*=(mass/m1)**(3/8)
    	en=self.enfromvel(mass,speed)
    	return rd,speed,mass,en
    	
    def getldfm(self,mass,di):
    	le=self.getlm(mass,di)
    	return le/di
    	
    def getlm(self,mass,di):
    	d=self.density
    	d=mass/d
    	di**=2
    	di*=nuct.picor
    	d=d/di
    	return d
    
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
        	r=1
        return self.dobar(ba1,r)
        
    def dobar(self,ba1,r):
    	return ba1*(r**.5)

    def getbuc(self, ba, ba1):
    	L_eff = self.barhvl(ba1, 0)
    	r = (sp.pi**2 / 64) * (ba**2 / L_eff**2)
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
    corr=(1/self.atomic_radius)/ref
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
    
def baseproj():
    return getsteel().getparp(getsteel().getbarmass(getsteel()),getsteel())
    
def barpm():
    rd,speed,mass,en=baseproj()
    barml=getsteel().getbarrellen(getsteel(),getsteel().getroundlenmass(mass,rd),speed,rd)
    return barml/rd
    
def baseshot():
    return sp.pi*(nuct.phi**2)
    
def maxshot():
	res=(barpm()*baseshot())
	return res

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

steel=getsteel()
du=getdu()
cf=getrp1tenpct()
steel.print_summary()
   
def getstr(mat):
    mat = basevals(mat)
    return mat.j_high_estimate

def bhn250():
    mat = basevals(getsteel())
    return (863*10**6) / mat.j_high_estimate

def do10gel():
    mat = basevals(getsteel())
    gel = getrp1tenpct()
    return gel.j_high_estimate / mat.j_high_estimate

strength = bhn250()
gels = do10gel()

def lethalcalc(mat, en, exp):
    sk = getskin()
    sken = sk.material_energy_density_j_per_hvl / (2**nuct.phi**6)
    en += sk.exen(exp)
    if en < sken:
        print("round not lethal")
        return 0
    mel = mat.melt_one_hvl()
    en = en / mel
    sken = sken / mel
    hvls = en / sken
    ar = mat.base_hvl
    hvls **= (1 / 12)
    hvls = hvls * ar
    return hvls

def dopen(mat):
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

if __name__ == "__main__":   
    
    
    def do2mm():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=3.5
    	cf.f2=.27/cm_m
    	cf.f3=speed/200
    	cf.f4=strength
    	dopen(cf)
    	print("barrel 7cm")
    	
    	
    def do25acp():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=2.5
    	cf.f2=.635/cm_m
    	cf.f3=speed/230
    	cf.f4=strength
    	dopen(cf)
    	print("barrel 9.8cm")
    
    def do22long():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=2.6
    	cf.f2=.57/cm_m
    	cf.f3=speed/370
    	cf.f4=strength
    	dopen(cf)
    	print("barrel 38cm")
    
    def do9mm():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=2
    	cf.f2=.9/cm_m
    	cf.f3=speed/376
    	cf.f4=strength
    	dopen(cf)
    	print("19mm drop in .5mpa clay is .01mm steel. 2000x clay steel ratio is .15mm for 30cm clay.")
    	print("barrel 11.4cm")
    	
    def do44():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=3
    	cf.f2=1.09/cm_m
    	cf.f3=speed/470
    	cf.f4=strength
    	dopen(cf)
    	print("actual .5")
    	print("barrel 12.5cm")
    
    def do556():
    	cf=steel
    	speed=getspeed(cf)	
    	cf.bafac=8.1
    	cf.f2=.556/cm_m
    	cf.f3=speed/994
    	cf.f4=strength
    	dopen(cf)
    	print("actual 1.5 (scaled from magnun).")
    	print("barrel 50.8cm")
    	
    def do762():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=6.7
    	cf.f2=.762/cm_m
    	cf.f3=speed/856
    	cf.f4=strength
    	dopen(cf)
    	print("actual 1.5 (scaled from magnum) ")
    	print("barrel 41.5cm")
    	
    def do3006():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=8.25
    	cf.f2=.762/cm_m
    	cf.f3=speed/890
    	cf.f4=strength
    	dopen(cf)
    	print("actual 1.5 (scaled from mangum")
    	print("barrel 60cm")
    	
    	
    def do50cal():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=7.8
    	cf.f2=1.27/cm_m
    	cf.f3=speed/(860)
    	cf.f4=strength
    	cf.fill=.5
    	cf.exp=.005
    	dopen(cf)
    	cf.exp=0
    	print("actual 2.3")
    	print("barrel 51cm")
    	
    def dom919():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=14
    	cf.f2=2.5/3/cm_m
    	cf.f3=speed/1385
    	cf.f4=strength
    	cf.fill=.85
    	dopen(cf)
    	print("actual 10.1")
    	print("barrel 106.7 cm")
    	
    def do37mmm4():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=3.08
    	cf.f2=3.7/cm_m
    	cf.f3=speed/(610)
    	cf.f4=strength
    	cf.fill=.91
    	cf.exp=0.05
    	dopen(cf)
    	cf.exp=0
    	print("actual 3.5cm")
    	print("barrel 198cm")
    
    def do40mmbofor():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=3.775
    	cf.f2=4/cm_m
    	cf.f3=speed/(860)
    	cf.f4=strength
    	cf.fill=.6
    	cf.exp=.1
    	dopen(cf)
    	cf.exp=0
    	print("actual 6.9cm")
    	print("barrel 225cm")
    	
    def dom1937():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=3.82
    	cf.f2=4.5/cm_m
    	cf.f3=speed/(760)
    	cf.f4=strength
    	cf.fill=.66
    	cf.exp=.254/2
    	dopen(cf)
    	print("actual 9.4cm")
    	print("barrel 207cm")
    	cf.exp=0
    	
    def dos60():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=3.6
    	cf.f2=5.7/cm_m
    	cf.f3=speed/(1000)
    	cf.f4=strength
    	cf.fill=.69
    	dopen(cf)
    	print("actual 10.6cm")
    	print("barrel 440cm")
    	
    def dom72():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=3.12
    	cf.f2=7.5/cm_m
    	cf.f3=speed/(618)
    	cf.f4=strength
    	cf.fill=.78
    	dopen(cf)
    	print("actual 10.9cm")
    	print("barrel 292cm")
    	
    def dom93():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=3.53
    	cf.f2=7.62/cm_m
    	cf.f3=speed/(1036)
    	cf.f4=strength
    	cf.fill=.44
    	dopen(cf)
    	print("actual 23.9cm")
    	print("barrel 340cm")
    	
    def dod48():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=3.02
    	cf.f2=8.5/cm_m
    	cf.f3=speed/(1040)
    	cf.f4=strength
    	cf.fill=.43
    	dopen(cf)
    	print("actual 19.5cm")
    	print("barrel 629cm")
    	
    def dobs3():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=4.1
    	cf.f2=10/cm_m
    	cf.f3=speed/(887)
    	cf.f4=strength
    	cf.fill=.62
    	dopen(cf)
    	print("actual 20cm")
    	print("barrel 534cm")
    	
    def dosherman():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=7.07
    	cf.f2=7.6/cm_m
    	cf.f3=speed/(792)
    	cf.f4=strength
    	cf.fill=.5
    	dopen(cf)
    	print("actual 23.9")
    	print("barrel 304.8cm")
    
    def do88():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=3.8
    	cf.f2=8.8/cm_m
    	cf.f3=speed/773
    	cf.f4=strength
    	cf.fill=.59#type 18
    	dopen(cf)  	
    	print("actual 17")
    	print("barrel 493.8 cm")
    	
    def do122():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=3.28
    	cf.f2=12.2/cm_m
    	cf.f3=speed/780
    	cf.f4=strength
    	cf.fill=.5
    	dopen(cf)
    	print("actual 17")
    	print("barrel 276.94 cm")
    	
    def dom833():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=17.7
    	cf.f2=2.46/cm_m
    	cf.f3=speed/1494
    	cf.f4=strength
    	cf.fill=1
    	dopen(cf)
    	print("actual 37cm")
    	print("barrel 546cm")
    
    def dom900():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=71.1/2.31
    	cf.f2=2.31/cm_m
    	cf.f3=speed/1505
    	cf.f4=strength
    	cf.fill=1
    	dopen(cf)
    	print("actual 50cm")
    	print("barrel 546cm")
    	
    def dobr412():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=3.26
    	cf.f2=10/cm_m
    	cf.f3=speed/(895*.93)
    	cf.f4=strength
    	cf.fill=.78
    	dopen(cf)
    	print("actual 15cm")
    	print("barrel 535cm")
    	
    def do3bm8():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=4.05
    	cf.f2=5.5/cm_m
    	cf.f3=speed/(1415*.85)
    	cf.f4=strength
    	cf.fill=1
    	dopen(cf)
    	print("actual 29cm")
    	print("barrel 535cm")
    	
    def do3vmb3():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=10
    	cf.f2=4.1/cm_m
    	cf.f3=speed/(1800*.85)
    	cf.f4=strength
    	cf.fill=1
    	dopen(cf)	
    	print("actual 25cm")
    	print("barrel 600cm")
    	
    def do3bm7():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=12
    	cf.f2=3.6/cm_m
    	cf.f3=speed/(1785)
    	cf.f4=strength
    	cf.fill=1
    	dopen(cf)
    	print("actual 40cm")
    	print("barrel 600cm")
    	
    def do3vbm17():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=17
    	cf.f2=3.1/cm_m
    	cf.f3=speed/(1700*.85)
    	cf.f4=strength
    	cf.fill=.63
    	dopen(cf)
    	print("actual 52cm")
    	print("barrel 600cm")
    	
    def dosvinets():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=21.84
    	cf.f2=2.5/cm_m
    	cf.f3=speed/(1700*.85)
    	cf.f4=strength
    	cf.fill=.88
    	dopen(cf)
    	print("actual 66cm")
    	print("barrel 600cm")
    	
    def do3bm59_60():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=28.18
    	cf.f2=2.2/cm_m
    	cf.f3=speed/(1660*.85)
    	cf.f4=strength
    	cf.fill=1
    	dopen(cf)
    	print("actual 66cm")
    	print("barrel 600cm")
    	
    def dotapna():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=29
    	cf.f2=2.5/cm_m
    	cf.f3=speed/1690
    	cf.f4=strength
    	cf.fill=2/3
    	dopen(cf)
    	print("actual 63cm")
    	print("barrel 600cm")
    	
    def dom829():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=35.68
    	cf.f2=2.5/cm_m
    	cf.f3=speed/1555
    	cf.f4=strength
    	cf.fill=1
    	dopen(cf)
    	print("actual 71cm")
    	print("barrel 530cm")
    	
    def do140mm():
    	cf=du
    	speed=getspeed(cf)
    	cf.bafac=32
    	cf.f2=2.95/cm_m
    	cf.f3=speed/1700
    	cf.f4=strength
    	cf.fill=.55
    	dopen(cf)
    	print("actual 80cm")
    	print("barrel 658cm")
    	
    def do5():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=5.35
    	cf.f2=12.7/cm_m
    	cf.f3=speed/790
    	cf.f4=strength
    	cf.fill=.33
    	dopen(cf)
    	print("actual 13cm")
    	print("barrel 475cm")
    	
    def do6():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=4.5
    	cf.f2=15/cm_m
    	cf.f3=speed/640
    	cf.f4=strength
    	cf.fill=.5
    	cf.exp=2.6/2
    	dopen(cf)
    	cf.exp=0
    	print("actual 30cm")
    	print("barrel 750cm")
    	
    def do8():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=4.06
    	cf.f2=20/cm_m
    	cf.f3=speed/(823)
    	cf.f4=strength
    	cf.fill=.5
    	dopen(cf)
    	print("actual 40cm")
    	print("barrel 800cm")
    	
    def do16():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=4.5
    	cf.f2=41/cm_m
    	cf.f3=speed/762
    	cf.f4=strength
    	cf.fill=.5
    	dopen(cf)
    	print("actual 75cm")
    	print("barrel 2020 cm")
    
    def dogust():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=3
    	cf.f2=80/cm_m
    	cf.f3=speed/720
    	cf.f4=strength
    	cf.fill=.75
    	dopen(cf)
    	print("barrel 3250cm")
    	
    def doharp():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=.437
    	cf.f2=.41
    	cf.f3=speed/2164
    	cf.f4=strength
    	cf.fill=1
    	dopen(cf)
    	print("barrel 5400cm")
    	
    def dobab():
    	cf=steel
    	speed=getspeed(cf)
    	cf.bafac=(544/7850)
    	cf.f2=1.01
    	cf.f3=speed/3600
    	cf.f4=strength
    	cf.fill=1
    	dopen(cf)
    	print("barrel 15600cm")
    	
    	
    def dosteel():
    	cf=du
    	cf.bafac=1
    	cf.f2=1
    	cf.f3=1
    	cf.f4=1
    	cf.fill=1
    	dopen(cf)
    	
    
    	    
    dopen(cf)
    do2mm()
    do25acp()
    do22long()
    do9mm()
    do44()
    do556()
    do762()
    do3006()
    do50cal()
    dom919()
    do37mmm4()
    do40mmbofor()
    dom1937()
    dos60()
    dom72()
    dom93()
    dod48()
    dobs3()
    dosherman()
    do88()
    do122()
    dom833()
    dom900()
    do3bm8()
    dobr412()
    do3vmb3()
    do3bm7()
    do3vbm17()
    dosvinets()
    do3bm59_60()
    dotapna()
    dom829()
    do140mm()
    do5()
    do6()
    do8()
    do16()
    dogust()
    doharp()
    dobab()
    dosteel()
    
