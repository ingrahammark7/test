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
fobw=.004
fobs=fobw**2
fobv=fobt*fobs
de=2700
fobm=fobv*de
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
ppl=conc*pp
print("at focus",conc,"heat",ppl)
to=273
ln2=math.log(2)
kbt=bc*to*ln2
avm=((gap**3)*de)*av
print("number of atoms obstructing fob",avm)
lj=kbt*avm
print("loss j",lj)
alxhvl=.003
xf=1e17
rf=1e9
ra=xf/rf
alrhvl=ra*alxhvl
print("radio hvl km",alrhvl/1e3)
lo=(gap/alrhvl)*lj
print(lo*1e3,"actual milliwats loss")
print(lo/pr,"share of losses to actual power")
ald=.2e-9
alm=4.5e-26
vth=((3*bc*ppl)/alm)**.5
ags=1
powr=(2/ags)+1
ipo=1/powr
cr=ald/vth
pt=(ip**3)*cr
print("time to aggregate seconds",pt)
ro=pt/tih
print("uses before agg",ro)
userdpay=10
print("days to fail",ro/userdpay,"at purity 1 per",ip)
