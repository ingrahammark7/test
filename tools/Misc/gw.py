import math

rpow=2
gap=.01
wv=.001
dt=(wv/(4*math.pi*gap))**2
pr=dt*rpow
print(pr*1000,"milliwats received by fob")
fobn=1e-6
lay=10
space=10
fobt=fobn*lay*space
fobs=.004**2
fobv=fobt*fobs
fobm=fobv*2700
print("fob chip mass milligrams",fobm*1e6)
ht=5
fair=ht*fobs
sh=900
mel=600
hc=sh*fobm
tih=hc/fair
print(tih*1e3,"millseconds fob relax")
pur=1e-4
ip=1/pur
alm=27
av=6e26
ac=fobm/alm
ac*=av
print("fob atoms",ac)
ac1=ac**(1/3)
print("fob side",ac1)
bc=1.38e-23
conc=1e3
pp=pr/fobm/sh
pp*=tih
print("heat c per relax",pp)
print("at focus",conc,"heat",pp)
to=273
ln2=math.log(2)
kbt=bc*to*ln2
