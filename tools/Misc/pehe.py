import math

notchps=1
enperk=10
tensile=100_000_000
pico=math.pow(10,-12)
crad=70*pico
col=9*math.pow(10,9)
el=1.6*math.pow(10,-19)
forc1=col*el*el/(crad*crad)
forc=forc1
av=6*math.pow(10,23)
forc=av*forc*1000
forc=math.pow(forc,1/2)
forc=forc/12
masstrap=1/forc
masspy=20_000
trapy=masspy/masstrap/enperk
tril=math.pow(10,12)
placet=60
pctfuel=.5
trapy=trapy*pctfuel
trapvol=masstrap*1000/1_000_000
year=60*60*24*365
corr=0.001
corrs=corr/year
heatcoeff=1000
temp=1000
hc=heatcoeff*temp
kgar=0.01
hc=hc*kgar
ht=temp/hc*1000
ht=ht*ht/3
carry=10
corrsm=corrs*1000
corrsr=corrsm*ht
trapside=math.pow(trapvol,1/3)
trapc=1/trapside
trapc=math.pow(trapc,2)
timepe=1/10
etcht=trapc*timepe
day=60*60*24
lift=10
massm=lift/corrsr
timel=massm/(etcht/ht)
timel=math.pow(timel,.5)
compt=etcht*timel
compt=compt/year
runs=year/placet
tot=runs*trapc
sunm=1000
mi=2000*2000
mip=sunm*mi*year/100
bact=10
mip=mip/bact
micem=0.03
micet=micem*tensile
micec=mip/micet
cap=tot/micec
phi=1.618
r=math.pow(137,math.pow(phi,1))
r=cap/r
humperm=1
humas=100
ls=3*math.pow(10,8)
cps1=ls/crad
cps=math.pow(cps1,1/3)
cps=cps*forc1
ema=9*math.pow(10,-31)
ev=2*forc1/ema
ev=math.pow(ev,1/2)
ep=ls*ls*.5*ema*cps1
numcp=1*math.pow(10,18)
mu1=numcp/cps1
ep=math.pow(ep,1/2)
expm=2/3
fac=humas/1
fac=math.pow(fac,expm)
humpow=fac*ep
g=10
step=g*humas
stepd=0.5
cosw=step/stepd*4
spe=humpow/cosw/3
yspe=year*spe
dspe=day*spe
yr=yspe/dspe
yr=math.pow(yr,1/3)*dspe
gent=day*90
genm=math.pow(gent/day,1/3)*dspe
print(genm)