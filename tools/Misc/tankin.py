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
sker=pen.getskin()
nf=nuct.pm

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
        self.maxx = self.times * t1.rspe() * am/4
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
            t.tf*=self.hmm
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
            for i in range(0,maxx,self.rr):
            	self.doj(i,self.rr)
    
    def doj(self, i,rr):
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
    	return dif/self.hmm
    
    def gref(self,t):
            x=t.x
            y=t.y
            return self.grefx(x,y)
            
    def torc(self,x,y,t):
    	mo=self.grefx(x,y)
    	return self.torcc(mo,t)
    
    def torcc(self,mo,t):
      to=t.tf
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
            nn=nf
            sk=sker
            n1=nn/sk.density
            fr=(3**6)**12
            nn*=fr           
            nn/=nf
            nn**=(1/3)
            nn*=n1
            return nn
            
    def saved(self,s,fn):
    	filen=fn
    	with open(filen, "w") as f:
                json.dump(s, f)  
                print("exported to ",filen)
    
    def savet(self):
    	self.saved(self.cf,"re"+str(dt.now().timestamp())+".json")
    
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
    	for k in self.term.keys():
    		xin=int(k)
    		if (xin>=x):
    			for j in self.term[k].keys():
    				ji=int(j)
    				if(ji>=y):
    					return self.term[k][j]
    	return 0
    	
    def doc(self,x,y):
    	if not x in self.term:
    		self.term[x]={}
    	if(x<0 or y<0):
    		self.term[x][y]=0
    	if not y in self.term[x]:
    		self.term[x][y] = self.nearr(x,y)
    		
    def pethh(self,t,x,y):
    	if(t.power==0):
    		os.sys.exit()
    		return
    	she=(t.x,t.y)
    	if she in t.sh:
    		t.power=0
    		return
    	t.sh.append(she)
    	x1=t.x
    	y1=t.y
    	self.doc(x,y)
    	self.doc(x1,y1)
    	teh=self.gethx(t,x,y)
    	bl=self.mof(t,teh)
    	if bl is None:
    		t.power=0
    		return
    	self.move(t,bl)
    	
    def peto(self,t,x,y):
    	for _ in range(self.getmo(t)):
    		self.pethh(t,x,y)
    	
    def nex(self, t,heading_deg):
        heading_deg=float(heading_deg)
        rad = np.radians(heading_deg)
        dx = np.cos(rad)
        dy = np.sin(rad)
        nx = t.x + np.where(dx > 0.5, 1, np.where(dx < -0.5, -1, 0))
        ny = t.y + np.where(dy > 0.5, 1, np.where(dy < -0.5, -1, 0))
        return nx, ny
    
    def mof(self,t,ttl):
    	hj=45
    	for i in range(8):
    		ttl+=hj
    		if(ttl>360):
    			ttl=hj
    		t.heading=ttl
    		nx,ny=self.nex(t,ttl)
    		tes=self.torc(nx,ny,t)
    		if(tes):
    			return ttl
    	return None
    	
    def getmo(self,t):
    	return t.getrs(self.times)
    	
    def gettf(self,t):
    	return self.times/self.getmo(t)

    def move(self,t, heading_deg):
        t.heading=heading_deg
        ter=self.gettf(t)
        t.move(ter)
    	
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
            

tt = tankin()
yt2=tankin()
tt.termm()
tt.savem()
ts=""
cd=1
prx=0
pry=0
for ig in range(round(tt.midx+tt.midy)):	
	ttf=tt.cf[cd]
	tt.pethh(ttf,tt.midx,tt.midy)
	ts+=f"|{cd} tank moved to {ttf.x},{ttf.y}"
	print(round(ttf.x),round(ttf.y))
tt.saved(ts,"f2.json")