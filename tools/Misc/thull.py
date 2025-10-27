import pen
import nuct
import math
import sympy as sp

class thull:
	def __init__(self,name,length,power,fuel,ammo,armorfront):
		self.name=name
		self.mass=1
		self.length=length
		self.width=self.length/2
		self.height=self.width/2
		self.power=power
		self.fuel=fuel
		self.ammo=ammo
		self.armorfront=armorfront
		self.armorside=self.armorfront/2
		self.armorrear=self.armorside/2
		self.material=pen.getsteel()
		self.matq=1/8
		self.mass=self.getmass()
		self.nuc=nuct.baseobj()
		
		
	def getmass(self):
			d=self.material.density
			ff=self.getplate(self.armorfront,self.width,self.height)
			fs=self.getplate(self.armorside,self.length,self.height)*2
			fr=self.getplate(self.armorrear,self.width,self.height)
			em=self.engmass()
			to=ff+fs+fr+em
			return to+self.fuel
			
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
			mm=self.hvlmass()
			jper=self.material.material_energy_density_j_per_hvl
			kgs=1/mm
			jper*=kgs
			return jper
			
	def hvlmass(self):
			hvl=self.material.base_hvl
			hvl**=3
			hvl*=self.material.density
			return hvl
			
	def getfric(self):
			bo=self.width*self.width
			coe=.5
			gr=self.nuc.getg()
			m=self.mass
			
			
tt=thull("fko",10,1000,2000,1,.1)
tt.mass=tt.getmass()
eng=tt.engmass()
print(sp.N(tt.mass),"abrams mass")
print(sp.N(eng),"engine mass")
tt.getfric()