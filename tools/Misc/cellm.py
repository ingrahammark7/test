import nuct
import sympy as sp
import pen

sk=pen.getskin()
cd=38
zc=pen.getsteel().zc
bol=pen.getsteel().bol
pm=nuct.baseobj().corprma()*34
ca=16

class cellm:
	def __init__(self):
		pass
		
	def dof(self):
		fr=self.evaps()
		ti=self.ps()/fr
		print(sp.N(ti))
		
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
		
	def cstr(self):
		return pen.getsteel().j_high_estimate/(pen.getsteel().j_high_estimate/(50*10**6)) #intentionally explicit
		
	def ps(self):
		return self.cwr()*cd*ca
		
	def kkber(self):
		return self.kber(zc*1.05,pm)
	
	def kber(self,t,m):
		return (3*bol*t/m)**.5
		
		
ffl=cellm()
ffl.dof()