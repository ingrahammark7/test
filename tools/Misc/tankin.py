import json
import sympy as sp
import copy
from collections.abc import Iterable

import nuct 
import thull
import pen
from datetime import datetime
import numpy as np

dp=2
m=dp**nuct.phi
m=float(m)

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
        self.maxx = self.times * t1.rspe() * nuct.baseobj().am/100
        self.maxx = self.maxx.evalf()
        self.maxy = self.maxx
        self.rr=round(self.hmm)
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
    
    def termm(self):
        	r=self.rr
        	maxx=round(self.maxx)        
        	maxy=round(self.maxy)	
        	for i in range(0,round(self.maxx),self.rr):
        		self.doj(i,self.rr)
        	for i in range(round(self.maxx)-r,-1,-r):
        			self.doj(i,-r)
        	for j in range(0,maxy,r):
        		self.dov(j,r)
        	for j in range(maxy-r,-1,-r):
        			self.dov(j,-r)
        			
    def dov(self,j,rr):
    	if not j in self.term:
    		for i in self.term:
    			self.term[i][j]=0
    	zper=0
    	for i in range(0,round(self.maxx),abs(rr)):
    		if(i>0 and j>0 and (i-abs(rr))<self.maxx and (j-rr)<self.maxy):
    			zper=self.term[i-abs(rr)][j-rr]
    			z2=self.term.get(i-rr,{}).get(j,0)
    			z3=self.term.get(i,{}).get(j-abs(rr),0)
    			zper=float((zper+z2+z3)/3)
    		zper=self.dol(i,j,zper)
    
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
            
    def dol(self,i,j,zper):
        	fd = i * j + i + j
        	fd **= dp
        	fd = fd % m
        	fd /= m
        	fd -= 0.5
        	zper += (fd * self.hmm)
        	self.term[i][j] = zper
        	return zper
        	
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
        	filen="f.json"
        	with open(filen, "w") as f:
        		json.dump(self.term, f)  # 'tt' is your tankin instance
        	print("Terrain exported to ",filen)
        

tt = tankin()
tt.termm()
tt.savem()

# Export the terrain to a JSON file
