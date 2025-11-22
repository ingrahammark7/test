import json
import sympy as sp
import copy
from collections.abc import Iterable
import os

import nuct 
import thull
import pen
import numpy as np
from datetime import datetime as dt

dp=2
m=dp**sp.GoldenRatio
m=float(m)
an=nuct.baseobj()
am=an.am
ran=am**3
ran=int(round(ran))
rc=round(os.sys.getsizeof(ran)/4)
boh=thull.baseobj()

def doff(s):
    strr="0x"
    for i in range(s):
        strr+="f"
    return strr
    
wc=int(doff(rc),16)
wc1=(wc/ran)

class en(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, sp.Basic):
            if obj.free_symbols:
                return str(obj)
            else:  
                return float(sp.N(obj))

        elif hasattr(obj, "__dict__"):
            return {k: self.default(v) for k, v in obj.__dict__.items()}

        elif isinstance(obj, dict):
            return {self.default(k): self.default(v) for k, v in obj.items()}

        elif isinstance(obj, (set, tuple)):
            return [self.default(v) for v in obj]

        elif isinstance(obj, Iterable) and not isinstance(obj, str):
            return [self.default(v) for v in obj]
        elif callable(obj):
            return f"<function {obj.__name__}>"
        else:
            return str(obj)

def en2(tf):
    return copy.deepcopy(tf)
t1 = en2(boh)

class tankin:
    def __init__(self):
        co = 5
        self.cf = {}
        self.term={}
        self.times = 0
        self.teams = {0, co}
        self.clo=0
        self.hmm=float(self.hm())
        f1 = t1.turn(90)
        f2,_ = t1.timett(90, 0)
        self.times = (min(f1, f2) * 16).evalf()
        self.maxx = self.times * t1.rspe() * am/50
        self.maxx = self.maxx.evalf()
        self.maxy = self.maxx
        self.midx=self.maxx/2
        self.midy=self.maxy/2
        self.rr=round(self.hmm)
        self.l=0
        for te in self.teams:
            maxe = self.maxx
            if te == 0:
                maxe = co
            self.dot(te, co, maxe - co, t1)
            
    def dot(self, st, co, x, t1):
        for i in range(co):
            t = en2(t1)
            t.x = x+i+(co-st)
            t.y = 0
            fj = i + st
            self.cf[fj] = t
        return self
    
    def tim2(self,x):
        x=round(x)
        tr=x%round(self.hmm)
        x-=tr
        return x
    
    def timer(self):
        self.maxx=self.tim2(self.maxx)
        self.maxy=self.tim2(self.maxy)
    
    def termm(self):
            if(self.checkif()==1):
                return
            r=self.rr
            self.timer()
            maxx=self.maxx    
            maxy=self.maxy
            passes=3   	
            for p in range(passes):	
                for i in range(0,maxx,self.rr):
                    self.doj(i,self.rr)
                for i in range(maxx-r,0,-r):
                    self.doj(i,-r)
                for j in range(0,maxy,r):
                    self.dov(j,r)
                for j in range(maxy-r,0,-r):
                    self.dov(j,-r)
                    
    def dov(self,j,rr):
        if(j%1000==0):
            print("p2",j/self.maxy)
        if not j in self.term:
            for i in self.term:
                self.term[i][j]=0
        zper=0
        rf=abs(rr)
        mx=round(self.maxx-rf)
        my=round(self.maxy-rf)
        if(j>=my or j<rf):
            self.dol(0,j,0)
            return
        for i in range(rf,mx,rf):
                    zper=self.term[i-rf][j-rr]
                    z2=self.term[i-rr][j]
                    z3=self.term[i][j-rf]
                    zper=float((zper+z2+z3)/3)
                    zper=self.dol(i,j,zper)
    
    def doj(self, i,rr):
        if(i%1000==0):
            print("pct",i/self.maxx)
        if i not in self.term:
            self.term[i] = {}
        zper = 0
        for j in range(0, round(self.maxy), rr):
            if i > 0 and j > 0:
                zper = self.term[i - rr][j - rr]
                if i in self.term and j in self.term[i]:
                    zper=(zper+self.term[i][j])/2
                z2 = self.term[i - rr][j]
                z3 = self.term[i][j - rr]
                zper=float((zper+z2+z3)/3)
            zper=self.dol(i,j,zper)
            
    def grefx(self,x,y):
    	self.doc(x,y)
    	z=self.term[x][y]
    	x2=x-self.hmm
    	y2=y-self.hmm
    	self.doc(x2,y2)
    	z2=self.term[x2][y2]
    	dif=z2-z
    	if(dif==0):
    	       return 0
    	return dif/self.hmm
    
    def gref(self,t):
            x=t.x
            y=t.y
            return self.grefx(x,y)
            
    def torc(self,x,y,t):
    	mo=self.grefx(x,y)
    	return self.torcc(mo,t)
    
    def torcc(self,mo,t):
      to=t.tofic()
      if(mo>to):
            return False
      return True
      
    def torct(self,t):
      mm=self.gref(t)
      return self.torcc(mm,t)
            
    def dol(self,i,j,zper):
            zper += i * j + i + j
            zper=self.hash32(zper)
            zper/=ran
            zper-=wc1
            self.term[i][j] = (-self.hmm/zper)**.5
            return zper
    
    def hash32(self,x):
        x=int(x)
        x *= ran
        return x & wc
            
    def hm(self):
            nn=nuct.pm
            sk=pen.getskin()
            n1=nn/sk.density
            fr=3**6
            fr**=12
            nn*=fr
            nn/=nuct.pm
            nn**=(1/3)
            nn*=n1
            return nn
            
    def saved(self,s,fn):
    	filen=fn
    	with open(filen, "w") as f:
                json.dump(s, f)  
                print("exported to ",filen)
    
    def savet(self):
    	self.saved(self.cf,str(dt.now().timestamp())+".json")
    
    def savem(self):
            if(self.l==1):
                return
            self.saved(self.term,"f.json")

    def checkif(self):
        p="fin.json"
        if os.path.exists(p):
            with open(p,'r') as file:
                self.term=json.load(file)
                self.l=1
                return 1
        return 0
    
    def dcalc(self,x1,y1,x2,y2,z1,z2):
        return (abs(x2-x1)+1)*(abs(y2-y1)+1)*(abs(z2-z1)+1)
    
    def maxc(self,x):
    	if(x<0):
    		x=0
    	maxx=max(self.term)
    	if(x>maxx):
    		x=maxx
    	return x
    	
    def maxyc(self,y):
    	if(y<0):
    		y=0
    	maxx=max(self.term[max(self.term)])
    	if(y>maxx):
    		y=maxx
    	return y
    	
    def nearr(self,x,y):
    	rj=round(self.hmm+1)
    	for i in range(rj):
    		xi=x+i-1
    		if xi in self.term:
    			for j in range(rj):
    				ji=y+j-1
    				if ji in self.term[xi]:
    					return self.term[xi][ji]
    	return 0
    	
    def doc(self,x,y):
    	if not x in self.term:
    		self.term[x]={}
    	if not y in self.term[x]:
    		self.term[x][y] = self.nearr(x,y)
    		
    def pethh(self,t,x,y):
    	she=str(x) +"," + str(y)
    	if(she==t.sh):
    		t.power=0
    		return
    	x1=t.x
    	y1=t.y
    	self.doc(x,y)
    	self.doc(x1,y1)
    	al=[]
    	if(x==x1 and y==y1):
    		return
    	teh=self.gethx(t,x,y)
    	bl=self.mof(t,teh)
    	if bl is None:
    		t.power=0
    		return
    	self.move(t,bl)
    	
    def mof(self,t,ttl):
    	hj=45
    	for i in range(8):
    		ttl+=hj
    		if(ttl>360):
    			ttl=hj
    		nx,ny=self.nex(t,ttl)
    		tes=self.torc(nx,ny,t)
    		if(tes):
    			return ttl
    	return None
    	
    def nex(self, t,heading_deg):
        heading_deg=float(heading_deg)
        rad = np.radians(heading_deg)
        dx = np.cos(rad)
        dy = np.sin(rad)
        nx = t.x + np.where(dx > 0.5, 1, np.where(dx < -0.5, -1, 0))
        ny = t.y + np.where(dy > 0.5, 1, np.where(dy < -0.5, -1, 0))
        return nx, ny

    def move(self,t, heading_deg):
        nx, ny = self.nex(t,heading_deg)
        t.x, t.y = nx, ny
        return nx, ny
    	
    def gethx(self,t1,x1,y1):
    	x=t1.x
    	y=t1.y
    	dx = x1 - x
    	dy = y1 - y
    	if dx == 0 and dy == 0:
    		return 0
    	ang = sp.deg(sp.atan2(dy, dx))
    	return ang if ang >= 0 else ang + 360
    
    def geth(self,t1,t2):
    	x1,y1=t2.x,t2.y
    	return self.gethx(t1,x1,y1)
    	
    	
    def loscheck(self,t1,t2):
        starx=round(self.maxc(t1.x))
        stary=round(self.maxyc(t1.y))
        self.doc(starx,stary)
        starz=round(self.term[starx][stary]+t1.tbarh())
        ex=round(self.maxc(t2.x))
        ey=round(self.maxyc(t2.y))
        self.doc(ex,ey)
        eh=round(t2.height+self.term[ex][ey])
        dis=self.dcalc(starx,stary,ex,ey,starz,eh)
        rann=t1.gr
        if(dis>rann):
            return False
        dx=abs(ex-starx)
        dy=abs(ey-stary)
        x,y=starx,stary
        sx=1 if starx<ex else -1
        sy=1 if stary<ey else -1
        grid=self.term
        if dx > dy:
            err=dx/2
            while x != ex:
                print(x)
                t=np.hypot(x-starx,y-stary)/np.hypot(ex-starx,ey-stary)
                hol=starz+t*(eh-starz)
                self.doc(x,y)
                if grid[x][y]>hol:
                    return False
                err-=dy
                if err <0:
                    y+=sy
                    err+=dx
                x+=sx
            else:
                err=dy/2
                while y!=ey:
                    t=np.hypot(x-starx,y-stary)/np.hypot(ex-starx,ey-stary)
                    hol=starz+t*(eh-starz)
                    self.doc(x,y)
                    if grid[x][y] >hol:
                        return False
                    err -= dx
                    if err <0:
                        x+=sx
                        err+=dy
                    y+=sy
            if grid[ex][ey]>eh:
                return False
            return True
from datetime import datetime
dt=datetime.now()
tt = tankin()
dt=dt-datetime.now()
print(dt.total_seconds()) 
tt.termm()
tt.savem()

for ig in range(len(tt.cf)):
	ttf=tt.cf[1]
	print("star",ttf.x,ttf.y)
	dt=datetime.now()
	tt.pethh(ttf,tt.midx,tt.midy)
	dt=dt-datetime.now()
	print(dt.total_seconds())
	print("en",ttf.x,ttf.y)
# Export the terrain to a JSON filedt=datetime.now()