g=10
den=1
m=1
mt=m/den
hs=(2*mt*g)**.5
d=10000
v=1

mf=hs*hs*m*.5


def doer(v):
	x=0
	en=.5*v*v*m
	for i in range(100_000):
		if(x==d):
			print("energy at ",v,"is ",en)
			break
		x+=v
		en+=mf
		
for i in range (200):
	doer(v*i)
	
	