import math

g=6.674e-11
nm=1.6749e-27
nr=0.8e-15
nr1=nr
ev=1.6e-19
vel=2200

def ger(r):
	return (g*(nm*nm)/(r**2))
def vele(en):
	return math.sqrt(2*(en/nm))
massen=939*(10**6)*ev
pc=6.626e-34
c=3e8
hc=c*pc
frn=hc/massen
frn=math.sqrt(frn)
gf=ger(nr)
cps=vel/nr
cps=cps*frn
print(cps)
nr=nr/cps
gf=ger(nr)
print(gf/ev)

	