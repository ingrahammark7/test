import pen
import nuct
import sympy as sp

thres=(nuct.baseobj().gethw()*nuct.alpha).evalf()


class thull:
	def __init__(self,name,length,ammo,armorfront):
		self.name=name
		self.fden=850
		self.fen=45.6e6
		self.vp=12
		self.gear=8
		self.mass=1
		self.f4=1/3
		self.length=length
		self.width=self.length/2
		self.height=self.width/2
		self.power=1
		self.fuel=1
		self.thres=thres
		self.ammo=ammo
		self.armorfront=armorfront
		self.armorside=self.armorfront/2
		self.armorrear=self.armorside/2
		self.material=pen.getsteel()
		self.matq=1/self.gear
		self.mass=self.getmass()
		self.nuc=nuct.baseobj()
		self.rofric=nuct.alpha_fs
		self.heading=0
		self.thead=0
			
	def getbar(self):
		barm=self.engmassp()/pen.maxshot()
		du=pen.getdu()
		spee=pen.getspeed(du)
		rd,speed,mass,en=du.getparp(barm,du)
		ld=du.getldfm(mass,rd)
		du.bafac=ld
		du.f2=rd
		du.f3=spee/speed
		du.f4=1
		pen.dopen(du)
		return du
	
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
			self.material=pen.getsteel()
			enr=self.enperkg()*self.matq
			enf=self.fuelen()
			return enf/enr
	
	def engmassp(self):
			pp=self.psize()*self.vp
			return self.engmass()+pp
			
	def enperkg(self):
			return self.material.j_high_estimate*self.f4
			
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
			print(sp.N(self.turspe()),"tur speed")
			print(sp.N(self.rspe()),"ms")
			self.getbar()
			
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
			pl/=self.gear
			pl**=1
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
			mf=2**3
			m=self.engmass()/mf/vp
			if(self.power>self.thres):
				m*=mf
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
			p1=(self.gethc()**-(2/3))/(self.gear**(1/sp.E))
			p1*=(self.vp**(1/3))
			p1/=(self.material.j_high_estimate**(1/3))
			poow=p1*self.length**(1/self.length)
			poow*=(self.fen*self.fden)**(2)
			poow/=nuct.baseobj().am**4
			return poow
	
	def scalee(self,tm):
		return self.scale(tm,self.engmass())
	
	def scale(self,tm,rm):
		enr=rm/tm
		enr**=1/3
		l2=(self.length/enr)
		return thull(self.name,l2,self.ammo,self.armorfront).init()	
		
	def getbaseobj(self):			
		return self.scalee(self.getcc())
		
	def scalem(self,tm):
			return self.scale(tm,self.getbaseobj().mass)
			
	def turm(self):
			return self.mass/6
			
	def apup(self):
			return self.power*nuct.alpha_fs
			
	def rotd(self):
			sidel=self.length/3
			frontl=self.width
			return sidel*frontl*2
			
	def turse(self):
			turf=self.turm()*nuct.baseobj().getg()
			tur=turf*self.rofric
			return self.apup()/tur
			
	def turspe(self):
			rr=self.rotd()/2
			lenn=rr
			lenn/=self.turse()
			spw=(2*self.apup()/self.turm())**.5
			spp=spw/rr
			if(spp<lenn):
				cc=1/spp
				cc**=.5
				cc=1/cc
				c1=1/lenn
				if(cc<c1):
					print("turret accel braked")
					return spp
			return lenn
			
	def rspe(self):
		gf=self.mass*nuct.baseobj().getg()*self.rofric
		gf=self.power/gf
		gf**=1/3
		return gf
		
	def timet(self,angle):
			spe=self.turspe()
			delta = (angle-self.thead) % 360  # Normalize to 0–360
			if delta > 180:
			 delta -= 360  # Choose the shorter rotation direction
			 ds=delta/180
			 tim=abs(ds/spe)
			 self.thead=angle
			 return self,tim


			
			
def dof(name,l):
	print("")
	tt1=thull(name,l,1,0)
	tt1=tt1.init()
	tt1.getfric()
	return tt1
	
def baseobj():
	d=dof("b",1)
	return d.getbaseobj()
	
def scaleobj(tm):
	return baseobj().scalem(tm)

tt=thull("bacteria",1e-10,1,0)				
tt=tt.init()
tt.getfric()
print("")
dof("bac",1e-5)
dof("toy",.3)
dof("bike",2)
tt=thull("car",3,1,.01)
tt=tt.init()
eng=tt.engmass()
tt.getfric()
tt=thull("critical engine",5,1,0.01)
tt=tt.init()
print("")
tt.getfric()
dof("abrams",10)
dof("marine",20)
tt=thull("96c plus",40,1,.01)
tt=tt.init()
print("")
tt.getfric()
tt.getcc()
tt=baseobj()
print("")
tt.getfric()