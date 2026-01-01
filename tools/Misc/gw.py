hetr=1000
misn=1
misa=misn*misn
mel=300
silmel=1000
silfrac=0
mel=((silmel*silfrac)+(mel*(1-silfrac)))
powr=hetr*misa*mel
sh=1*1000
shc=sh*mel
dens=1000
thi=.05
vol=misa*thi
ma=dens*vol
shm=ma*shc
spe=200*6
aird=1
altitude=20e3
airg=10e3
aird/=(altitude/airg)
airph=vol*aird
hps=spe/(vol**(1/3))
airp=airph*hps
airen=.5*spe*spe*airp
print("ratio of air energy to convection",airen/powr)
effic=9
shm*=effic
re=shm/powr
re1=shm/airen
print("seconds to ablate",re)
print("range",spe*re)
print("dens",aird)
str=10e6/shc
re1*=str
print("mechanicsl ablation",re1)
print("range",spe*re1)
