import pen
import nuct
import sympy as sp
from datetime import datetime as dt

thres=(nuct.baseobj().gethw()*nuct.alpha).evalf()

class thull:
	def __init__(self, name, length, ammo, armorfront):
		self.name = name
		self.fden = 850
		self.fen = 45.6e6
		self.vp = 12
		self.gear = 8
		self.mass = 1
		self.f4 = 1/3
		self.length = length
		self.width = self.length / 2
		self.height = self.width / 2
		self.power = 1
		self.fuel = 1
		self.thres = thres
		self.ammo = ammo
		self.armorfront = armorfront
		self.armorside = self.armorfront / 2
		self.armorrear = self.armorside / 2
		self.material = pen.getsteel()
		self.matq = 1 / self.gear
		self.mass = self.getmass()
		self.nuc = nuct.baseobj()
		self.rofric = nuct.alpha_fs
		self.heading = 0
		self.thead = 0
		self.tlen = 1/3
		self.tw = 1
		self.th = 1
		self.tzh = 0
		self.frontgfan = 45
		self.frontbfan = 45
		self.x=0
		self.y=0
		self.sh=[]
		self.bar=0
		self.gr=0
		self.tf=0
		self.tte=0
		self.ttr=0
		self.dd=[]
		self.so=0
		
	def firehead(self):
		self.ammo-=1
		return (self.thead+180)%360
		
	def turn(self,head):
		t1=self.timets(head,self.rspe())
		self.heading=head
		return t1
	
	def move(self,t):
		if self.fuel<=0:
			self.power=0
			return
		self.x,self.y=self.nm(t)
		
	def nm(self,t):
		spe=self.getrs(t)/t
		eff=.5
		poww=self.power
		fps=(poww/self.fen)*t/eff
		self.fuel-=fps
		rr=sp.rad(self.heading).evalf(nuct.PRECISION)
		dx=spe*sp.cos(rr).evalf(nuct.PRECISION)
		dy=spe*sp.sin(rr).evalf(nuct.PRECISION)
		fx=round(self.x+dx)
		fy=round(self.y+dy)
		return fx,fy
		
	def getrs(self,t):
		if(self.so==0):
			self.so=round(sp.N(self.rspe()*t))
			return self.so
		return self.so
		
	
	def turfrac(self):
		return self.th/2
	
	def takehit(self,xan,zan,roundd):
			turfrac=self.turfrac()
			turfrac=180*turfrac
			turfrac=90-turfrac
			print(self.heading,self.thead)
			if(zan>turfrac):
				return self.turhit(xan,zan,roundd)
			xfan=xan-self.heading
			efan=90-zan
			if(135>xfan>45 or -135<xfan<-45):
				return self.material.pen(roundd,xfan,efan),self.armorside
			if(xfan>135 or xfan<-135):
				if(xfan>135):
					xfan=270-xfan
					return self.material.pen(roundd,xfan,efan),self.armorrear
				else:
					xfan=270+xfan
					return self.material.pen(roundd,xfan,efan),self.armorrear
			xfan=90-xfan
			efan-=self.frontbfan
			return self.material.pen(roundd,xfan,efan),self.armorfront
			
	def turhit(self,xan,zan,roundd):
		xfan=xan-self.thead
		efan=90-zan
		if(-45<xfan<45):
			efan-=self.frontbfan
			xfan-=self.frontgfan
			xfan+=90
			print("front tur",xfan,efan)
			return self.material.pen(roundd,xfan,efan),self.armorfront
		if(45<xfan<135 or -45>xfan>-135):
			efan-=self.frontbfan
			print("side tur xfan efan",xfan,efan)
			return self.material.pen(roundd,xfan,efan),self.armorside
		print("rear tur",xfan,efan)
		return self.material.pen(roundd,xfan,efan),self.armorrear
	
	def getbar(self):
		rd,speed,mass,en,du=self.getdd()
		spee=pen.getspeed(du)
		ld=du.getldfm(mass,rd)
		du.bafac=ld
		du.f2=rd
		du.f3=spee/speed
		du.f4=1
		self.bar=du
		self.gr=self.bar.getrang()
		return du
		
	def getdd(self):
		if len(self.dd)!=0:
			fr=self.dd
			return fr[0],fr[1],fr[2],fr[3],fr[4]
		barm=self.getbarm()
		du=pen.getdu()
		rd,speed,mass,en=du.getparp(barm,du)
		self.dd.append(rd.evalf())
		self.dd.append(speed.evalf())
		self.dd.append(mass.evalf())
		self.dd.append(en)
		self.dd.append(du)
		return rd,speed,mass,en,du
		
	def getbarm(self):
		return self.engmassp()/pen.maxshot()
		
	def getbarmr(self):
		return self.getbarm()*pen.maxshot()
			
	def getmass(self):
			ff=self.getplate(self.armorfront,self.width,self.height)
			fs=self.getplate(self.armorside,self.length,self.height)*2
			fr=self.getplate(self.armorrear,self.width,self.height)
			self=self.fuelcube()
			em=self.engmassp()
			ex=self.extramass()
			bar=self.getbarm()
			to=ff+fs+fr+em+ex+bar
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
			
	def tofic(self):
		return self.tof1()
		
	def tof1(self):
		to=self.getq()*self.gear
		fo=self.nfor()
		return to/fo
	
	def getfric(self):
			print(self.name)
			print(sp.N(self.pl()/sp.pi),"pisfon widtg")
			print(sp.N(self.mass),"mass")
			print(sp.N(self.engmassp()),"engine")
			print(sp.N(self.getbarmr()),"barrel")
			print(sp.N(self.tofic()),"torque to fric")
			print(sp.N(self.getrps()),"rotate per sec")
			print(sp.N(self.psize()),"piston mass")
			print(sp.N(self.pl()),"piston stroke len")
			print(sp.N(self.getsp()),"speed")
			print(sp.N(self.power),"power")
			print(sp.N(self.getbucm()),"buck frac")
			print(sp.N(self.turspe()),"tur speed")
			print(sp.N(self.rspe()),"ms")
			print(sp.N(self.numg()),"numg")
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
			self.power=self.getpow().evalf()
			self.tf=self.tofic().evalf()
			self.turspe()
			self.rspe()
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
			return self.mass/(self.th*self.tlen*self.tw/2)
			
	def apup(self):
			return self.power*nuct.alpha_fs
			
	def rotd(self):
			sidel=self.length*self.tlen
			frontl=self.width*self.tw
			return sidel*frontl*2
			
	def turse(self):
			turf=self.turm()*nuct.baseobj().getg()
			tur=turf*self.rofric
			return self.apup()/tur
	
	def hse(self):
			hurf=self.mass*nuct.baseobj().getg()
			hur=hurf*self.rofric
			return self.power/hur
			
	def turspe(self):
		if self.ttr!=0:
			return self.ttr
		foo=self.ttspe(self.turse(),self.rotd()/2,self.apup(),self.turm())
		self.ttr=foo.evalf()
		return foo
		
	def hspe(self):
		return self.ttspe(self.hspe(),self.length,self.power,self.mass)		
			
	def ttspe(self,spe,d,poww,m):
		rr=d
		lenn=rr
		lenn/=spe
		spw=(2*poww/m)**.5
		spp=spw/rr
		if(spp<lenn):
			cc=1/spp
			cc**=.5
			cc=1/cc
			c1=1/lenn
			if(cc<c1):
				return spp
		return lenn
			
	def rspe(self):
		if(self.tte!=0):
			return self.tte
		gf=self.mass*nuct.baseobj().getg()*self.rofric
		gf.evalf()
		gf=self.power/gf
		gf**=1/3
		self.tte=gf.evalf()
		return gf
		
	def barrh(self):
		return (self.geturh()/2)
	
	def turh(self):
		return self.height-(self.turfrac()*self.height)
	
	def tbarh(self):
		ty=self.barrh()
		return self.turh()+ty
	
	def timett(self,angle,z):
		t1=self.timet(angle)
		t2=self.timet(z)
		maxm=max(t1,t2)
		maxr=1
		ll=self.getbar()
		roundl=ll.bafac*ll.f2
		barh=self.barrh()
		if(abs(z)>90):
			return maxm,0
		if(barh>roundl and z>0):
			return maxm,maxr
		tang=barh/(self.getursetb()+roundl)
		tfr=abs(z/90)
		if(tang>tfr and barh>roundl):
			return maxm,maxr
		rll=barh/roundl
		if(rll<tfr):
			return maxm,0
		if(z>0):
			return maxm,maxr
		if(tang>tfr):
			return maxm,maxr
		else:
			return maxm,0
	
	def ttimer(self,angle,z):
		g,h=self.timett(angle,z)
		if(h==1):
			self.tzh=z
			self.thead=angle
		return g,h
			
		
	def repa(self,angle,z):
		self,g,h=self.ttimer(angle,z)
		g=sp.N(g)
		h=sp.N(h)
		hh=sp.N(self.geturh()/2)
		if(h==0):
			return self
		return self
			
	def geturh(self):
		return (self.th/2)*self.height
		
	def getursetb(self):
		tf=1
		tf-=self.tlen
		tf/=2
		return tf*self.length
	
	def timet(self,angle):
			spe=self.turspe()
			return self.timets(angle,spe)
			
	def timets(self,angle,spe):
		delta = (angle-self.thead) % 360  # Normalize to 0–360
		if delta > 180:
			delta -= 360  # Choose the shorter rotation direction
		ds=delta/180
		tim=abs(ds/spe)
		return tim
		
	def numg(self):
		ging=self.getbar()
		actb=self.getbarmr()
		bmd=pen.getsteel().getbarrelmat(1).getbarmass(ging)
		if(actb<bmd):
			return 1
		return (actb/bmd/pen.maxshot()/nuct.phi)
		
	def addarmor(self):
		self.init()
		m=self.mass
		tvol=self.length*self.height*self.width*self.material.density
		r=m/tvol
		r*=self.width/2
		return thull(self.name,self.length,self.ammo,r)
		
def dof(name,l):
	tt1=thull(name,l,pen.maxshot(),0.0)
	return tt1.init()
	
def dofarm(l):
	tt1=dof("b",l)
	return tt1.addarmor().init()
	
def baseobj():
	d=dof("b",1)
	return d.getbaseobj().addarmor().init()
	
def scaleobj(tm):
	return baseobj().scalem(tm)
	
"""
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
tt1=thull("96c plus",40,1,.01)
tt1=tt1.init()
print("")
tt=baseobj()
print("afger",sp.N(tt.mass))
tt.getfric()
print("")
print(sp.N(tt.armorside))
tt=dofarm(2000)
tt.getfric()
print("mass",sp.N(tt.mass))
print("side",sp.N(tt.armorside))
"""