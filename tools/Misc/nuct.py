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
picor=sp.pi/4

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
        w=self.gethw()
        r=penn.req
        r=4*sp.pi*r*r
        wa=1361
        wa1=wa*year
        dur=year*10
        wa=r*wa*dur
        w=w*dur
        f=wa/w
        f*=1/self.am/3
        f*=alpha_fs        
        vesc=sp.sqrt((2*penn.getbigg()*penn.getearth())/penn.req)
        hm=penn.geth()
        hm**=2
        en=.5*hm*vesc*vesc
        stel=2*10e9
        corf=1
        sden=7.85
        shvl=(1.27/pen.cm_m)*(pen.mass_g)
        steelperm=(shvl*sden)
        steelperm*=stel*corf
        f1=wa1/steelperm
        w1=self.gethw()*(1/f1)*year
        w1=w1/en
        w1*=alpha_fs
        return w1
        
        
    def gethw(self):
    	p=penn
    	h=p.geth()
    	r=p.crad
    	gg=p.getbigg()
    	cc=self.getc()
    	crate=(cc/p.crad)
    	r=penn.crad
    	pr=self.corprma()
    	f=gg*(pr*pr)/(r**2)
    	f=f*crate
    	f=f*h*penn.avogadro*pen.mass_g*2
    	return f
    	
    def magc(self):
    	return 4*sp.pi*10e-7
    
    def getelm(self):
    	return self.evpr()*self.shellt
    	
    def getema(self):
    	return self.getelm()/(self.getc()**2)
 
    def getperm(self):
    	return 1/(self.magc()*self.getc()*self.getc())
    
    def getk(self):
    	return 1/(4*sp.pi*self.getperm())
    
    def corprma(self):
    	#cop=1.67262192595e-27	
    	hb=self.prmaen()*2
    	amf=1/self.am
    	fl=53+(1/(12-(1/(3+(1/(5/(4/(3.3/(1+alpha_fs*(.5*(1-amf*51)))))))))))
    	aml=sp.exp((fl))
    	aml=hb*aml
    	return aml
    	
    def prmaen(self):
    	hb=self.gethb()
    	cc=self.getc()
    	hb=hb/(cc*cc)
    	return hb
    
    def evpr(self):
    	#ra=0.00000000106578891869549
    	an=1/self.am
    	af=an**2.59
    	af=af/(1+alpha_fs*(1+2/3))
    	af=af/(1-an/(1.75-alpha_fs*(40+(.6+alpha_fs/8))))
    	cc=self.getc()**2
    	af=af*self.corprma()*(cc)
    
    	return af
    
    	
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

    
def baseobj():
	return NuclearPenetrationModel(penn)




    