import math

en=math.pow(10,12)
hvla=1
ev=math.pow(10,-19)
mev=math.pow(10,6)
hvlamec=mev*.5
gev=math.pow(10,9)
tev=math.pow(10,12)
pev=math.pow(10,15)
eev=math.pow(10,18)
planck=math.pow(10,-34)
depth=1

def shv(baseh,pow,basepow):
	t=math.sqrt(pow/basepow)
	return t*baseh

def sh(baseh,pow):
	if(pow<hvlamec):
		return hvla
	return shv(baseh,pow,hvlamec)
	
def co(pow,powev):
	powev=powev*ev	
	if(powev<planck):
		return pow/planck
	evf=ev*hvlamec
	s=powev/evf
	s=math.pow(s,1/2)
	return pow/powev/s
	
def penr(hvl,en,depth):
	t=math.pow(2,depth/hvl)
	return en/t

def funcm(ml):
	return penr(sh(hvla,ml),co(en,ml)*ml*ev,depth)

mevpow=funcm(mev)
print(mevpow/en)
