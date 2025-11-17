import pen
import nuct 
import thull
import json
import sympy as sp
import copy
from collections.abc import Iterable

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
		co=5
		self.cf={}
		self.times=0
		t1=thull.baseobj()
		t1=en2(t1)
		for i in range (co):
			t=en2(t1)
			t.x=i
			t.y=0
			self.cf[i]=t		
		f1,ff1=t1.turn(90)
		f2,ff2=t1.timett(90,0)
		self.times=min(f1,f2)*16
		self.maxx=self.times*t1.rspe()*nuct.baseobj().am
		self.maxy=self.maxx
		self.times=sp.N(self.times)
		self.maxx=sp.N(self.maxx)
		self.maxy=sp.N(self.maxy)
		print("times",self.maxx)
		
tt=tankin()
	