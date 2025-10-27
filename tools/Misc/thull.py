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
			
	def getpow(self):
		f=self.gethc()
		n=self.numenghvl()
		n**=1/3
		f/=n
		f*=self.engmass()
		return f/2
		
	def getht(self):
		return pen.getht(self.material)
		
	def gethc(self):
		har=self.material.base_hvl**2
		tr=har*self.getht()*self.getmp()
		hvlperkg=1/self.material.hvl_mass_kg()
		return tr*hvlperkg
		
	def numenghvl(self):
		return self.engmass()/self.material.hvl_mass_kg()
		
	def getmp(self):
		return pen.getmp(self.material)				
	
	def init(self):
			self=self.getmass()
			self.power=self.getpow()
			return self
						
tt=thull("fko",10,1,.01)
tt=tt.init()
eng=tt.engmass()
print(sp.N(tt.mass),"abrams mass")
print(sp.N(eng),"engine mass")
tt.getfric()