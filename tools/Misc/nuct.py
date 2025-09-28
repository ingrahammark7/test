# nuct.py
import sympy as sp
import math
from pen import Material 
import pen
import ast

phi = sp.GoldenRatio
alpha_fs = 1/((((4*sp.pi)-6)**phi)**phi)  
alpha = 1 / alpha_fs
pm = alpha ** phi ** (4+5/9)
ac = pm       
prma = 1 / (alpha ** phi ** 5)
prma = prma / 1000
pm = pm * prma
c1=299792456.2
c=c1
penn=pen.getsteel()
PRECISION=2**12
unage=sp.exp(32+2/3)
year=60*60*24*365

class NuclearPenetrationModel:
    def __init__(self, material):
        self.material = material
        

        self.E = sp.symbols('E')        
        self.n_e = sp.symbols('n_e')   
        self.ec = material.elementary_charge
        
        self.am = alpha ** phi
        self.osc = 6
        self.brem = self.am * (alpha ** (1 + ((1/((self.osc-1)*(self.osc-2))))))
        self.disc = self.brem * 16
        self.shellt = self.brem / 3
        self.compt = self.brem * 2
        self.evperj = pen.getsteel().ev_to_joule
        self.c3=c**(1/3)

    def getpow(self):
    	p=penn
    	h=p.geth()
    	g=p.getg()
    	r=p.crad
    	gg=p.getbigg()
    	c=self.getc()
    	crate=(c/p.crad**1/3)
    	
    	print(self.corprma().evalf())
    	
 
   
    def corprma(self):
    	#cop=1.67262192595e-27	
    	hb=self.gethb()
    	cc=self.getc()
    	hb=2*hb/(cc*cc)
    	amf=1/self.am
    	fl=53+(1/(12-(1/(3+(1/(5/(4/(3.3/(1+alpha_fs*(.5*(1-amf*51)))))))))))
    	aml=sp.exp((fl))
    	aml=hb*aml
    	print(aml.evalf())
    	return aml
    
    def getelm(self):
    	ff=self.corprma()
    	#1836.152673426
    	fd=self.am/phi
    	
    	amf=1/self.am
    	amf=1+amf*71.9727
    	fd*=amf
    	return fd/1836.152673426
    	
    def getc(self):
    	p=penn
    	sec=p.getsec()
    	ll=p.getpl()
    	cc=ll/4.8/sec
    	return cc
    
    def gethb(self):
    	tp=self.gettp()
    	tp*=tp
    	g=penn.getbigg()
    	cc=self.getc()**5
    	tp*=cc*2*sp.pi
    	tp/=g
    	return tp
    	
    def getrhb(self):
    	return self.gethb()/(2*sp.pi)
    	
    def gettp(self):
    	#tp=5.391247e-44
    	sec=pen.getsteel().getsec()
    	r=sec
    	r=r/(self.am**12)/(40+phi*(1/(.999)))
    	return r
    
    def getalp(self):
    	d=self.getalpd()
    	d=d**-1
    	d*=1+(2/(3+(.2-(alpha_fs/((8-(1/13.7))/9)))))
    	d+=137
    	return d
    	
    def getalpd(self):
    	inv=self.getinvtp()
    	d=alpha**1/3
    	ee=alpha**1/2
    	gh=unage/self.gettp()
    	d=d/(gh)
    	d=d*ee*inv
    	d=1/d
    	d=sp.log(d)
    	ff=alpha
    	ff=sp.log(ff)
    	d=d/ff
    	re=d
    	return re
    	
    def getinalp(self):
    	return 1/self.getalp()
    
    def getinvtp(self):
    	tp = self.gettp()           # assume tp is symbolic or numeric
    	tp_inv = 1/tp               # invert
    	tp_inv = sp.nsimplify(tp_inv)  # simplify if symbolic

    # Convert to string scientific notation
    	tp_str = "{:.{}e}".format(tp_inv.evalf(),PRECISION)  # convert to string like '1.600000e-43'
    	sig_str, exp_str = tp_str.split('e')
    	sig = sp.S(sig_str)
    	exp = sp.S(int(exp_str))  # make exponent exact integer

    	f = sig * 10**(exp*-1)

    	return f
    
    def getgem(self):
    	f=self.am**phi**5
    	f=1/f
    	am=self.am
    	#a=1/f/1.5/(1-1/32)
    	b=1/f*am*6/(1+1/24)
    	#cc=1/f*9/(1-1/alpha)
    	return b   	
    
    def bremsstrahlung_loss(self, E_mev, n_e):
        Z = self.material.atomic_number
        E_mev = math.sqrt(E_mev)
        frac = E_mev / (self.compt)
        exponent = frac * self.osc

        loss = (Z ** exponent) * n_e * alpha_fs * math.log(E_mev + 1)
        return loss

    def emf(self, mass1, mass2, r):
        cc1 = mass1 / prma * self.ec
        c2 = mass2 / prma * self.ec
        top = pen.getsteel().k * cc1 * c2
        return top / r

    def velfromen(self, mass, en):
        return math.sqrt(2 * (en / mass))

    def emvf(self, mass1, mass2, r):
        emff = self.emf(mass1, mass2, r)
        v1 = self.velfromen(mass1, emff)
        v2 = self.velfromen(mass2, emff)
        return min(v1,v2)

    def mhd_bolus(self, round_energy_j, round_diameter_cm, round_mas, round_ld):
        numpm = round_mas / pm
        perpm = round_energy_j / numpm if numpm != 0 else 0
        numpm = math.sqrt(numpm)
        peaken = numpm * perpm
        ch1 = getattr(pen.getsteel(), "ch1", None)
        if ch1 is None:
            ch1 = 1.0
        charger = (peaken / numpm) / ch1 if numpm != 0 else 0.0
        if charger > 1:
            print("ionization achieved",charger.evalf())
        else:
            return 0
        length = round_ld * round_diameter_cm / 100.0
        length = length / 2.0
        cov=pm*charger
        cov=(cov**(1/3))
        cov=cov/round_mas
        en = round_energy_j 
        roundspeed = self.velfromen(round_mas, en)
        print("speed ", roundspeed)
        em=self.emvf(round_mas,pm,length)
        print("flux flies at c% ",em/c)
        em1=em**(1/3)
        print("round speed % of flux ",roundspeed/(em1))
        v1=roundspeed/self.c3
        if(v1>1):
        	v1**=(2/3)
        else:
        	v1=1
        vdif=math.sqrt(roundspeed+em1)-math.sqrt(roundspeed)
        roundspeed=roundspeed+vdif
        c2=.5*round_mas*roundspeed
        round_energy_j=max(round_energy_j,c2)
        p=(round_energy_j/pen.estfix(self.material))*self.material.base_hvl_cm
        return ((p*cov)**phi)/v1

    def honeycomb_dissipation_factor(self, layers):
        return (1 + layers) ** 3

    def jtomev(self, num):
        return num * 6.242e6

    def roundld(self, round_diameter_cm, round_mas,roundmaterial):
        round_mas/=roundmaterial.fill
        round_front_vol = round_diameter_cm * round_diameter_cm *round_diameter_cm / 1000000.0
        round_front_mass = round_front_vol * roundmaterial.density
        if round_front_mass == 0:
            return 1
        return round_mas / round_front_mass

    def penetration(self, round_energy_j, round_diameter_cm, honeycomb_layers, round_mas,roundmaterial):
        round_ld = self.roundld(round_diameter_cm, round_mas,roundmaterial)
        print("round ld ", round_ld)
        E_mev_val = self.jtomev(round_energy_j)
        n_e_val = self.material.density * (1 / self.am)

        brems_loss_val = self.bremsstrahlung_loss(E_mev_val, n_e_val)

        base_penetration = (round_energy_j /pen.estfix( self.material)) * self.material.base_hvl_cm

        dissipation = self.honeycomb_dissipation_factor(honeycomb_layers)


        if brems_loss_val > E_mev_val:
            brems_loss_val = 0  

        mhd_var = self.mhd_bolus( round_energy_j, round_diameter_cm, round_mas, round_ld)
        adjusted_penetration = mhd_var + base_penetration / (1 + brems_loss_val * dissipation)
        if adjusted_penetration < self.material.base_hvl_cm:
            adjusted_penetration = 0
        
        return float(adjusted_penetration)


def nuclear_penetration(round_energy_j, round_diameter_cm, honeycomb_layers, round_mas, material,roundmaterial):
  
    
    model = NuclearPenetrationModel(material)
    return model.penetration(round_energy_j, round_diameter_cm, honeycomb_layers, round_mas,roundmaterial)
    
def baseobj():
	return NuclearPenetrationModel(pen.getsteel())




    