import json
import sympy as sp
import copy
from collections.abc import Iterable

import pen
import nuct 
import thull

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
        self.times = 0
        self.teams = {0, co}

        t1 = thull.baseobj()
        t1 = en2(t1)

        f1, _ = t1.turn(90)
        f2, _ = t1.timett(90, 0)

        self.times = min(f1, f2) * 16
        self.maxx = self.times * t1.rspe() * nuct.baseobj().am

        self.times = sp.N(self.times)
        self.maxx = sp.N(self.maxx)
        self.maxy = self.maxx

        for te in self.teams:
            maxe = self.maxx
            if te == 0:
                maxe = co

            # FIXED: do NOT assign to self
            self.dot(te, co, maxe - co, t1)

    def dot(self, st, co, x, t1):
        for i in range(co):
            t = en2(t1)
            t.x = x+i
            t.y = 0
            fj = i + st
            self.cf[fj] = t
            print(fj, "position", t.x, t.y, "gun mass", sp.N(t.getbarmr()))
        return self


tt = tankin()