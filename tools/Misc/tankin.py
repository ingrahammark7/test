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
hj=45

def saf(x):
	if isinstance(x,sp.Basic):
		if(x.is_number):
			return float(x)
	if isinstance(x,dict):
		return {saf(k): saf(v) for k,v in x.items()}
	if isinstance(x,(list,tuple,set)):
		t=type(x)
		return t(saf(v) for v in x)
	return x

def doff(s):
    strr="0x"
    for _ in range(s):
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
    def __init__(self,mam=1):
        co = 5
        self.cf = {}
        self.term={}
        self.times = 0
        self.teams = {0, co}
        self.clo=0
        self.hmm=self.hm()
        f1=0
        f2=0
        if(mam!=0):
        	f1 = t1.turn(90)
        	f2,_ = t1.timett(90, 0)
        self.times = mam*(min(f1, f2) * 16).evalf()
        self.maxx = self.times * t1.rspe() * am
        self.maxx = self.maxx.evalf()
        self.maxy = self.maxx
        self.midx=self.maxx/2
        self.midy=self.maxy/2
        self.rr=round(self.hmm)
        self.l=0
        self.inw(t1)
        self.tse=""
        self.ro=round((self.rr**nuct.phi).evalf())
        for te in self.teams:
            maxe = self.maxx
            if te == 0:
                maxe = co
            self.dot(te, co, maxe - co, t1)
            
    def inw(self,t):
            t.getrs(self.times)
            
    def dot(self, st, co, x, t11):
        for i in range(co):
            t = en2(t11)
            t.x = x+i+(co-st)
            t.y = 0
            fj = i + st
            t.tf*=self.rr
            self.cf[fj] = t
        return self
    
    def tim2(self,x):
        tr=x%self.hmm
        x-=tr
        return x
    
    def timer(self):
        self.maxx=self.tim2(self.maxx)
        self.maxy=self.tim2(self.maxy)
    
    def termm(self):
            if(self.checkif()==1):
                return
            self.timer()
            maxx=self.maxx
            self.term[0]={}
            rr=self.rr
            fl=0
            dte=dt.now()
            self.term[0]={}
            for i in range(0,round(self.maxy),self.rr):
            	self.term[0][i]=fl
            co=en2(self.term[0])
            for  i in range(0,round(maxx),self.rr):
            	self.term[i]=en2(co)
            	#for j in range(0,round(self.maxy),self.rr):
            		#self.term[i][j]=fl
            print((dte-dt.now()).total_seconds())
            dte=dt.now()
            for i in range(rr,round(maxx),self.rr):
                self.doj(i,self.rr)
                print((dte-dt.now()).total_seconds())
    
    def doj(self, i,rr):
        zper = 0
        for j in range(rr, round(self.maxy), rr):
                """
                zper = self.term[i - rr][j - rr]
                z2 = self.term[i - rr][j]
                z3=self.term[i][j-rr]
                zper=float((zper+z2+z3)/3)
                """
                self.dol(i,j,zper)
            
    def grefx(self,x,y,t11):
        self.doc(x,y)
        z=self.term[x][y]
        x2=t11.x
        y2=t11.y
        self.doc(x2,y2)
        z2=self.term[x2][y2]
        dif=z2-z
        return dif/self.rr
            
    def torc(self,x,y,t):
        mo=self.grefx(x,y,t)
        return self.torcc(mo,t)
    
    def torcc(self,mo,t):
        to=t.tf
        if(mo>to):
            return False
        return True
            
    def dol(self,i,j,zper):
            #zper += i * j + i + j
            zper=self.hash32(zper)
            zper/=ran
            zper-=wc1
            ro=self.ro
            self.term[i][j] =round(saf((ro*zper)**2))
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
            
    def ck(self,s):
        if isinstance(s,dict):
            newd={}
            for k,v in s.items():
            	k=int(k)
            	newd[k]=self.ck(v)
            return newd
        elif isinstance(s,(list,tuple,set)):
          	return [self.ck(x) for x in s]
        return s
            
    def savedd(self,s,fn):
    	with open(fn,"w") as f:
    		f.write(s)
    
    def saved(self,s,fn):
        s=self.ck(s)
        self.wff(s,fn)
                
    def wff(self,s,fn):
     	with open(fn, "w") as f:
                json.dump(s, f)  
                print("exported to ",fn)
    
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
        difer=x%self.rr
        dify=y%self.rr
        difer=abs(int(x-difer))
        dify=abs(int(y-dify))
        if not dify in self.term[difer].keys():
        	return 0
        return self.term[difer][dify]
        
    def doc(self,x,y):
        if not x in self.term.keys():
            self.term[x]={}
            difx=x%self.rr
            difx=abs(int(x-difx))
            if not difx in self.term.keys():
            	for i in self.term.keys():
            		if i >=difx:
            			self.term[difx]=self.term[i]
            			break
            self.term[x]=en2(self.term[difx])
        if not y in self.term[x].keys():
            self.term[x][y] = self.nearr(x,y)        
            
    def ish(self,t,x,y,co):
        return False
        she=(x,y)
        if t.sh.count(she)>co:
            return True
        t.sh.append(she)
        return False
    
    def ishh(self,t):
        return self.ish(t,t.x,t.y,2)
    
    def pethh(self,t,x,y):
        if self.ishh(t):
            t.power=0
            return
        dx,dy=self.getdd(t,x,y)
        teh,dx,dy=self.gethx(dx,dy)
        nx,ny=t.x+dx,t.y+dy
        mo=self.grefx(nx,ny,t)
        if(mo<t.tf):
        	self.move(t,teh,dx,dy)
        	return
        bl,dx,dy=self.mof(t,teh)
        if bl is None:
            t.power=0
            return
        self.move(t,bl,dx,dy)

    def peto(self,t,x,y):
        if t.power==0:
        	return
        for _ in range(t.so):
            self.pethh(t,x,y)
            self.tse+=f"|1 tank moved to {t.x},{t.y}"
        
    def nex(self, t,heading_deg):
        dx,dy=t.dotr(heading_deg)
        nx = t.x + dx
        ny = t.y + dy
        return nx, ny
    
    def mof(self,t,ttl):
        for i in range(8):
            fo,dx,dy=self.ttlo(t,ttl,1,i)
            if fo is not None:
                return fo,dx,dy
        return None,None,None
        
    def ttlo(self,t,ttl,co,i):
        tmp=ttl+hj*i
        tmp%=360
        t.heading=tmp
        nx,ny=self.nex(t,tmp)
        if(self.ish(t,nx,ny,co)):
            return None,None,None
        tes=self.torc(nx,ny,t)
        if(tes):
            return tmp,nx,ny
        return None,None,None
        
    def gettf(self,t):
        return self.times/t.so

    def move(self,t, heading_deg,dx,dy):
        t.heading=heading_deg
        ter=self.gettf(t)
        t.move(ter,dx,dy)
        
    def getdd(self,t11,x1,y1):
    	return x1-t11.x,y1-t11.y
    
    def gethx(self,dx,dy):
        if dx == 0 and dy == 0:
            return 0
        dy+=.01
        if(dy<0):
            if(dx<0):
                if(dx/dy>1):
                    return 180,-1,0
                else:
                    return 225,-1,-1
            else:
                if(dx/dy>-1):
                    return 270,0,-1
                else:
                    return 315,1,-1
        else:
                if(dx<0):
                    if(dx/dy>-1):
                        return 135,-1,-1
                    else:
                        return 90,0,1
                else:
                    if(dx/dy>1):
                        return 0,1,0
                    else:
                        return 45,1,1		
        
    def loscheck(self,t11,t2):
        starx=round(self.maxc(t11.x))
        stary=round(self.maxyc(t11.y))
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

def baseobj():
	return tankin(0)            

tt = tankin()
tt.termm()
ts=''
cd=1
dte=dt.now()
for ig in range(int(tt.midx)):
    ttf=tt.cf[cd]
    tt.peto(ttf,tt.midx,tt.midy)
ts=tt.tse
dte=dte-dt.now()
dte=dte.total_seconds()
print(dte)
tt.saved(tt.term,"f.json") 
tt.savedd(ts,"f2.json")
