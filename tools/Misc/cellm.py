import nuct
import sympy as sp
import pen

sk=pen.getskin()
cstr=pen.getsteel().j_high_estimate/36
cd=38
zc=pen.getsteel().zc
bol=pen.getsteel().bol
pm=nuct.baseobj().corprma()*34
ca=16
bs=nuct.baseobj().am**7
bs/=3
b1=(pen.getskin().atomic_radius*2)*(bs**(1/3))
amass=5.148e18
wr=nuct.baseobj().req
wa=4*sp.pi*(wr**2)
aper=amass/wa
ver=nuct.su/aper
moa=pen.getn().base_hvl
md=pen.getn().density
vper=((2*ver)/md)**.5
vt=(moa/vper)**.5
vt/=4
yy=nuct.year
rho_air=md
C_d=1
v_wind=vt
N_gusts=yy
rho_stalk=sk.density
k = 0.5 * rho_air * C_d * v_wind**2
yo=sk.base_hvl*sk.density*cstr/2
yo/=nuct.alpha
g=nuct.baseobj().getg()

R_max = ((2*sp.pi)**0.5 * k**1.5 / (rho_stalk * g))**(2/5)
L_max = (sp.pi**2 * yo * R_max**2 / (4 * rho_stalk * g))**(1/3)


def bucf(ba,l):
	return (sp.pi**2 / 64) * (ba**2 / l**2)	
	
def gpow():
	f=wa*nuct.su
	f*=nuct.year*nuct.baseobj().gettime()
	f*=nuct.alpha_fs**2
	f/=4
	return f
	
def avwork():
	w=gpow()
	w/=500
	w/=27
	w/=32
	return w
	
def fullq():
	return avwork()/81

class cellm:
	def __init__(self):
		pass
		
	def dof(self):
		pass
		
	def mden(self):
		b2=b1**3
		return b2*rho_stalk
		
	def evaps(self):
		fl=self.cwr()
		tt=self.kkber()
		rr=tt/fl
		fr=(rr**(1/3))*fl
		fr/=(2**3)*2
		return fr
		
	def cwr(self):
		ar=sk.atomic_radius
		fl=cd/ar/nuct.baseobj().am
		nn=138*(4+2/3)
		fl/=nn
		return 1/fl
		
	def pa(self):
		return 1
			
	def ps(self):
		return self.cwr()*cd*ca
		
	def kkber(self):
		return self.kber(zc*1.05,pm)
	
	def kber(self,t,m):
		return (3*bol*t/m)**.5
		
		
ffl=cellm()
print(sp.N(fullq()/1e14))