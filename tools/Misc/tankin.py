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
        self.maxxr=round(self.maxx)
        self.maxyr=round(self.maxy)
        self.midx=self.maxx/2
        self.midy=self.maxy/2
        self.rr=round(self.hmm)
        self.l=0
        self.inw(t1)
        self.tse=""
        self.ro=round((self.rr**nuct.phi).evalf())
        self.r2=int(round(ran/self.rr))
        self.cou=2
        self.fm=self.fom()
        self.fr=self.refs(self.fm)
        self.mv=[]
        
        for te in self.teams:
            maxe = self.maxx
            if te == 0:
                maxe = co
            self.dot(te, co, maxe - co, t1)
            
    def inw(self,t):
            t.getrs(self.times)
            t.tf*=self.rr
            
    def fs(self,x,y):
    	for i in self.term.keys():
    		for j in self.term.keys():
    			if int(i) >= x and int(j) >= y:
    				return i,j
    	return 0,0
    
    def dot(self, st, co, x, t11):
        if not self.checkif():
        	self.termm()
        for i in range(co):
            t = en2(t11)
            t.name=i
            t.x = int(x+i+(co-st))
            t.y = 0
            t.z=self.getsl(t.x,t.y)
            fj = i + st
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
            rr=self.rr
            fl=0
            self.term[0]={}
            for i in range(0,self.maxyr,self.rr):
            	self.term[0][i]=fl
            self.term[0][0]=fl
            co=self.term[0].copy()
            for  i in range(0,self.maxxr,self.rr):
            	self.term[i]=co.copy()
            for i in range(rr,self.maxxr,self.rr): 
                self.doj(i,self.rr)
    
    def doj(self, i,rr):
          fof=self.term[i].copy().keys()
          self.term[i-rr][0-rr]=0
          self.term[i][0-rr]=0
          for j in fof:
                #zper=self.highz(i,j,rr)
                zper=1
                self.dol(i,j,zper)
    
    def highz(self,i,j,rr):
            zper = self.term[i - rr][j - rr]
            z2 = self.term[i - rr][j]
            z3=self.term[i][j-rr]
            zper=float((zper+z2+z3)/3)
            return zper
            
    def grefx(self,x,y,t11):
        dif=self.getsl(x,y)-t11.z
        return dif*.5
            
    def torc(self,x,y,t):
        mo=self.grefx(x,y,t)
        return self.torcc(mo,t)
    
    def torcc(self,mo,t):
        to=t.tf
        if(mo>to):
            return False
        return True
            
    def dol(self,i,j,zper):
            zper=zper*(i*j+i+j)
            zper=self.hash32(zper)
            zper/=self.r2
            zper-=wc1
            self.term[i][j] =1/abs(zper)
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
                self.term=self.ck(self.term)
                self.l=1
                return 1
        return 0
    
    def dcalc(self,x1,y1,x2,y2,z1,z2):
        return abs(x2-x1)+abs(y2-y1)+abs(z2-z1)
    
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
    
    def getsn(self,t):
            t.z=self.getsl(t.x,t.y)
            
    def getsl(self,x,y):
            rx,ry=self.getsll(x,y)
            return self.term[rx][ry]
            
    def getsll(self,x,y):
            rx=x-x%self.rr 
            ry=y-y%self.rr
            return rx,ry
            
    def ish(self,t,x,y,co):
        she=(x,y)
        if t.sh.count(she)>co:
            return True
        t.sh.append(she)
        return False
    
    def ishh(self,t):
        return self.ish(t,t.x,t.y,self.cou)
    
    def getm(self,t,x,y):
    	dx,dy,teh,mo,_,_=self.getmm(t,x,y)
    	return dx,dy,teh,mo
    
    def getmm(self,t,x,y):
    	dx,dy=self.getdd(t,x,y)
    	teh,dx,dy=self.gethx(dx,dy)
    	nx,ny=t.x+dx,t.y+dy
    	mo=self.grefx(nx,ny,t)
    	return dx,dy,teh,mo,nx,ny
    
    def donv(self,t,x,y):
    	dx,dy,teh,mo=self.getm(t,x,y)
    	t.heading=teh
    	t.thead=teh
    	tr=copy.copy(t)
    	tr.x,tr.y=self.getsll(t.x,t.y)
    	dcal=self.dcalc(t.x,t.y,x,y,0,0)
    	while(mo<tr.tf and len(t.nv)<dcal):
    		mo=self.domo(tr,t,dx,dy)
    
    def domo(self,tr,t,dx,dy):
    	self.smo(tr,t,dx,dy)
    	return self.grefx(tr.x,tr.y,t)
    	
    def smo(self,tr,t,dx,dy):
    	fof=(tr.x,tr.y)
    	t.nv.append(fof)
    	for _ in range(self.rr):
    		self.smm(tr,t,dx,dy)
    	return tr,t
    	
    def smm(self,tr,t,dx,dy):
    	tr.x+=dx
    	tr.y+=dy
    	fof=(tr.x,tr.y)
    	t.nv.append(fof)
    	self.getsn(tr)
    
    def pethh(self,t,x,y):
        """
        for i in t.nv:
        	x,y=i
        	t.nv.remove(i)
        	dx=x-t.x
        	dy=y-t.y
        	t.move(dx,dy)
        	return
        """
        dx,dy,teh,mo=self.getm(t,x,y)   
        while(mo<t.tf):
        	self.move(t,teh,dx,dy)
        	return
        while self.ishh(t):
            self.rm(t,teh,dx,dy)
            return
        self.rm(t,teh,dx,dy)
    
    def rm(self,t,teh,dx,dy):
    	bl,dx,dy=self.mof(t,teh,dx,dy)
    	if bl is None:
    	    if (t.x,t.y) in t.hc:
    	    	t.power=0
    	    	return
    	    t.hj=-1*t.hj
    	    t.sh=[]
    	    fo=(t.x,t.y)
    	    t.hc.append(fo)
    	    return
    	dx-=t.x
    	dy-=t.y 
    	self.move(t,bl,dx,dy)
    	
    def geg(self,t2):
    	self.gegr(t2.x,t2.y)
    	
    def gegr(self,x,y):
    	x-=x%self.rr
    	y-=y%self.rr
    	mul=5
    	inx=x-1*self.rr*mul
    	iny=y+1*self.rr*mul
    	for i in range(inx,inx+3*self.rr*mul,1*self.rr):
    		f2=[]
    		for j in range(iny,iny-3*self.rr*mul,-1*self.rr):
    			xz=0
    			try:
    				xz=round(self.term[i][j])
    			except Exception:
    				pass
    			f2.append(xz)
    		
    	
    def peto(self,t,x,y):
        """
        if t.power==0:
        	return
        if(len(t.nv)==0):
        	self.donv(t,int(x),int(y))
        """
        for _ in range(t.so):
            self.pethh(t,x,y)
            self.rmove(t)
            
     
    def rmove(self,t):
        ss=f"{t.name} tank moved to {t.x},{t.y}"
        self.mv.append(ss)
        
    def nex(self, t,dx,dy):
        nx = t.x + dx
        ny = t.y + dy
        return nx, ny
    
    def mof(self,t,ttl,dx1,dy1):
        for i in range(8):
            fof,dx,dy=self.ttlo(t,ttl,self.cou,i,dx1,dy1)
            if fof is not None:
                return fof,dx,dy
        return None,None,None
        
    def ttlo(self,t,ttl,co,i,dx,dy):
        tmp=ttl+t.hj*i
        tmp%=360
        t.heading=tmp
        tmp,dx,dy=self.frm(tmp)
        nx,ny=self.nex(t,dx,dy)
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
        t.move(dx,dy)
        self.getsn(t)
        
    def getdd(self,t11,x1,y1):
    	return x1-t11.x,y1-t11.y
    
    def fom(self):
    	df={}
    	df[180]=(-1,0)
    	df[225]=(-1,-1)
    	df[270]=(0,-1)
    	df[315]=(1,-1)
    	df[135]=(-1,1)
    	df[90]=(0,1)
    	df[0]=(1,0)
    	df[45]=(1,1)
    	return df
    
    def refs(self,arr):
    	re={}
    	for i in arr:
    		va=arr[i]
    		re[va]=i
    	return re
    
    def frm(self,d):
    	x,y=self.fm[d]
    	return d,x,y
    
    def gethx(self,dx,dy):
        if dx == 0 and dy == 0:
            return 0,0,0
        dy+=.01
        if(dy<0):
            if(dx<0):
                if(dx/dy>1):
                    return self.frm(180)
                else:
                    return self.frm(225)
            else:
                if(dx/dy>-1):
                    return self.frm(270)
                else:
                    return self.frm(315)
        else:
                if(dx<0):
                    if(dx/dy>-1):
                        return self.frm(135)
                    else:
                        return self.frm(90)
                else:
                    if(dx/dy>1):
                        return self.frm(0)
                    else:
                        return self.frm(45)		
        
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
dte=dt.now()
tt.termm()
print((dte-dt.now()).total_seconds())
ts=''
cd=1
dte=dt.now()
ttf=tt.cf[cd]
foj=int(tt.midx)*10
m=int(tt.midx)+1
mm=int(tt.midy)+1
for ig in range(foj):    
    tt.peto(ttf,m,mm)
tt.tse="|".join(tt.mv)
ts=tt.tse
dte=dte-dt.now()
dte=dte.total_seconds()
print(dte)
tt.saved(tt.term,"f.json") 
tt.savedd(ts,"f2.json")
