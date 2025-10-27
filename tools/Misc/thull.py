import pen
import nuct
import sympy as sp

class thull:
	def __init__(self,name,length,ammo,armorfront):
		self.name=name
		self.mass=1
		self.length=length
		self.width=self.length/2
		self.height=self.width/2
		self.power=1
		self.fuel=1
		self.ammo=ammo
		self.armorfront=armorfront
		self.armorside=self.armorfront/2
		self.armorrear=self.armorside/2
		self.material=pen.getsteel()
		self.matq=1/8
		self.mass=self.getmass()
		self.nuc=nuct.baseobj()
		self.vp=12
		
	def getmass(self):
			ff=self.getplate(self.armorfront,self.width,self.height)
			fs=self.getplate(self.armorside,self.length,self.height)*2
			fr=self.getplate(self.armorrear,self.width,self.height)
			self=self.fuelcube()
			em=self.engmass()
			to=ff+fs+fr+em
			self.mass=to+self.fuel
			return self
			
	def fuelcube(self):
			fh=self.height/2
			fd=850
			self.fuel=(fh**3)*fd
			return self
			
	def getplate(self,thick,width,height):
			return thick*width*height*self.material.density
		
	def fuelen(self):
			defuel=45.6e6
			return self.fuel*defuel
		
	def engmass(self):
			enr=self.enperkg()*self.matq
			enf=self.fuelen()
			return enf/enr
			
	def enperkg(self):
			return self.material.j_high_estimate
			
	def getfric(self):
			gr=self.nuc.getg()
			m=self.mass
			fo=gr*m
			pl=fo*self.pl()
			to=self.getq()
			gs=16
			to*=gs
			print(sp.N(to/fo))
			
	def getq(self):
			s=self.getrps()
			p=self.power
			return (p/(2*sp.pi))/s
			
	def getrps(self):
			ps=self.ps()
			pl=self.pl()
			pl=ps/pl
			pl**=2/3
			return pl
			
	def ps(self):
			pp=self.power/self.vp
			pm=self.psize()
			return (2*pp/pm)**.5
			
	def pl(self):
		m=self.psize()
		d=self.material.density
		m=m/d
		m**=1/3
		return m*sp.pi
	
	def psize(self):
			vp=self.vp
			m=self.engmass()/8/vp
			return m
			
	def getpow(self):
		f=self.gethc()
		f*=self.engmass()
		return f*8*(sp.GoldenRatio)
		
	def getht(self):
		return pen.getht(self.material)
		
	def gethc(self):
		har=self.material.base_hvl**2
		tr=har*self.getht()*self.getmp()
		hvlperkg=1/self.material.hvl_mass_kg()
		return tr*hvlperkg
		
	def getmp(self):
		return pen.getmp(self.material)				
	
	def init(self):
			self=self.getmass()
			self.power=self.getpow()
			return self
						
tt=thull("fko",13,1,.01)
tt=tt.init()
eng=tt.engmass()
print(sp.N(tt.mass),"abrams mass")
print(sp.N(eng),"engine mass")
tt.getfric()