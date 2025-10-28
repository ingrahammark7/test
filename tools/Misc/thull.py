import pen
import nuct
import sympy as sp

class thull:
	def __init__(self,name,length,ammo,armorfront):
		self.name=name
		self.fden=850
		self.fen=45.6e6
		self.vp=12
		self.gear=8
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
			em=self.engmassp()
			ex=self.extramass()
			to=ff+fs+fr+em+ex
			self.mass=to+self.fuel
			return self
			
	def extramass(self):
			return self.engmassp()*3.5
			
	def fuelcube(self):
			fh=self.height/2
			fd=self.fden
			self.fuel=(fh**3)*fd
			return self
			
	def getplate(self,thick,width,height):
			return thick*width*height*self.material.density
		
	def fuelen(self):
			defuel=self.fen
			return self.fuel*defuel
			
	def getaxr(self):
		axm=self.engmassp()/self.material.density
		axr=axm**(1/3)
		axr*=2/(sp.pi**.5)
		mu=self.length/(axr)
		axr*=mu**-.5
		return axr/2
		
	def getur(self):
		hv=self.material.base_hvl
		lenn=self.length/hv
		ra=self.getaxr()/hv
		return lenn,ra
		
	def getbuc(self):
		L,ba=self.getur()
		r = (sp.pi**2 / 64) * (ba**2 / L**2)	
		return r	
		
	def getbucm(self):
		buc=self.getbuc()
		axa=(self.getaxr()**2)*sp.pi
		hv=self.material.base_hvl
		hve=self.material.material_energy_density_j_per_hvl
		hv**=2
		axa/=hv
		axa*=hve
		axa*=buc
		return (axa/self.power)*self.getrps()
		
	def engmass(self):
			enr=self.enperkg()*self.matq
			enf=self.fuelen()
			return enf/enr
	
	def engmassp(self):
			pp=self.psize()*self.vp
			return self.engmass()+pp
			
	def enperkg(self):
			return self.material.j_high_estimate
			
	def nfor(self):
			gr=self.nuc.getg()
			m=self.mass
			fo=gr*m
			return fo
			
	def getfric(self):
			fo=self.nfor()
			to=self.getq()
			gs=self.gear
			to*=gs
			print(self.name)
			print(sp.N(self.pl()/sp.pi),"pisfon widtg")
			print(sp.N(self.mass),"mass")
			print(sp.N(self.engmassp()),"engine")
			print(sp.N(to/fo),"torque to fric")
			print(sp.N(self.getrps()),"rotate per sec")
			print(sp.N(self.psize()),"piston mass")
			print(sp.N(self.pl()),"piston stroke len")
			print(sp.N(self.getsp()),"speed")
			print(sp.N(self.power),"power")
			print(sp.N(self.getbucm()),"buck frac")
			
	def getsp(self):
			ac=self.power
			fr=nuct.alpha_fs*self.nfor()
			fs=ac/fr
			rpl=self.getrps()*self.pl()
			return min(fs,rpl)
			
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
			m=1
			ra=self.engmass()/(self.getcc())
			if(ra<1):
				ra=1
			ra**=(1/3)
			m=self.engmass()/((2**3)/ra)/vp
			return m
			
			
	def getpow(self):
		f=self.gethc()
		f*=self.engmassp()
		return f*self.gear*(sp.GoldenRatio)
		
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
			
	def getcc(self):
			strr=self.material.j_high_estimate
			he=self.gethc()
			vv=(2*he)**.5
			hvv=self.material.base_hvl**3
			hvd=self.material.base_hvl
			ti=hvd/vv
			poow=ti*he
			poow=strr/poow
			poow*=(1/self.matq)
			poow*=self.material.hvl_mass_kg()
			fde=self.fden*self.fen
			fde*=hvv
			r1=self.material.j_high_estimate/self.fen
			poow/=fde
			poow/=r1
			poow/=(self.gear**2)/self.vp		
			return poow
						
tt=thull("car",3,1,.01)
tt=tt.init()
eng=tt.engmass()
tt.getfric()
tt=thull("critical engine",5.3,1,0.01)
tt=tt.init()
print("")
tt.getfric()
tt=thull("abrams",10,1,.01)
tt=tt.init()
print("")
tt.getfric()
tt=thull("96c",44,1,.01)
tt=tt.init()
print("")
tt.getfric()
tt.getcc()