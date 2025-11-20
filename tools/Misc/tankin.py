import json
import sympy as sp
import copy
from collections.abc import Iterable
import os

import nuct 
import thull
import pen
import numpy as np

dp=2
m=dp**sp.GoldenRatio
m=float(m)
am=nuct.baseobj().am
fif=8*8-5
fi2=9*11+1+fif
ran=am*(fi2*5-2)
ran-=32
ran+=.5
ran*=am
ran=int(round(ran))
rc=round(os.sys.getsizeof(ran)/4)

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


class tankin:
    def __init__(self):
        co = 5
        self.cf = {}
        self.term={}
        self.times = 0
        self.teams = {0, co}
        self.clo=0
        self.hmm=float(self.hm())
        t1 = thull.baseobj()
        t1 = en2(t1)
        f1 = t1.turn(90)
        f2,_ = t1.timett(90, 0)
        self.times = (min(f1, f2) * 16).evalf()
        self.maxx = self.times * t1.rspe() * nuct.baseobj().am/4
        self.maxx = self.maxx.evalf()
        self.maxy = self.maxx
        self.rr=round(self.hmm)
        self.ranf=np.log(ran/self.hmm)
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
            
    def dol(self,i,j,zper):
        	zper += i * j + i + j
        	zper=self.hash32(zper)
        	zper/=ran
        	zper-=wc1
        	self.term[i][j] = -1/zper
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
        	
    def savem(self):
        	if(self.l==1):
        		return
        	filen="f.json"
        	with open(filen, "w") as f:
        		json.dump(self.term, f)  # 'tt' is your tankin instance
        	print("Terrain exported to ",filen)
      
    def checkif(self):
        p="fin.json"
        if os.path.exists(p):
        	with open(p,'r') as file:
        		self.term=json.load(file)
        		self.l=1
        		return 1
        return 0
        

tt = tankin() 
tt.termm()
tt.savem()

# Export the terrain to a JSON file
