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
        	for i in range(0,round(self.maxx),self.rr):
        		self.doj(m,i)
        			
    def doj(self, m, i):
        rr=self.rr
        if i not in self.term:
        	self.term[i] = {}
        zper = 0
        for j in range(0, round(self.maxy), rr):
            if i > 0 and j > 0:
                print(i,j)
                zper = self.term[i - rr][j - rr]
                z2 = self.term[i - rr][j]
                z3 = self.term[i][j - rr]
                zper += z2 + z3
                zper /= 3
                zper = float(zper)
            fd = i * j + i + j
            fd **= dp
            fd = fd % m
            fd /= m
            fd -= 0.5
            zper += (fd * self.hmm)
            self.term[i][j] = zper
        		
        		
        
        	
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

import json

# Export the terrain to a JSON file
with open("f.json", "w") as f:
    json.dump(tt.term, f)  # 'tt' is your tankin instance

print("Terrain exported to f.json")