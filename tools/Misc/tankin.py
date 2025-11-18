import json
import sympy as sp
import copy
from collections.abc import Iterable

import nuct 
import thull
import pen
from datetime import datetime

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
        self.hmm=sp.N(self.hm())
        t1 = thull.baseobj()
        t1 = en2(t1)
        f1 = t1.turn(90)
        f2,_ = t1.timett(90, 0)
        self.times = min(f1, f2) * 16
        self.maxx = self.times * t1.rspe() * nuct.baseobj().am
        self.times = sp.N(self.times)
        self.maxx = sp.N(self.maxx)
        self.maxy = self.maxx
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
        	dp=2
        	m=dp**nuct.phi
        	m=sp.N(m)
        	rr=round(self.hmm)
        	ct=datetime.now()
        	dif2=0
        	for i in range(0,round(self.maxx),rr):
        		if not i in self.term:
        			self.term[i]={}
        		zper=0
        		if(i>0 and j>0):
        			zper=self.term[i-rr][j-rr]
        		for j in range(0,round(self.maxy),rr):
        			fd=i*j+i+j
        			fd**=dp
        			fd=fd%m
        			fd/=m
        			fd-=.5
        			zper+=fd*self.hmm
        			self.term[i][j]=zper
        		prog=i/self.maxx
        		lt=datetime.now()
        		diff=(lt-ct).total_seconds()
        		dif2+=diff
        		if(dif2>50):
        			print(prog,"progress")
        			est=diff/prog
        			print(est*(1-prog),"est")
        			dif2=0
        	pass
        	
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

tt = tankin()
tt.termm()