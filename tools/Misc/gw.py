import math

insolation=1361
phi=1.618
fr=math.pow(2,phi)
afterf=insolation/4
afterconvec=afterf/fr
afterloss=afterconvec/fr
afterIR=afterloss/fr
print(afterIR, "W/m2 heating energy available")
mil=math.pow(10,6)
oceanar=386*mil*1000*1000
oceanen=oceanar*afterIR
time=60*60*24*365*100
toten=time*oceanen
oceanmass=math.pow(10,24)
oceanenergypergram=toten/oceanmass
specheat=4
tempbase=oceanenergypergram/specheat
carbonppm=380
dcarbon=2
tempc=math.log(dcarbon*carbonppm/carbonppm)*tempbase
print(tempc, " degrees change from " , dcarbon,"x ghg change over century")
co2pct=0.1
tempc=tempc*co2pct
print(tempc, " degrees change from " , dcarbon,"x co2 change over century")
#global warming is fake

earthmass=6*math.pow(10,27)
earthspecheat=1
earthheatcap=earthspecheat*earthmass
u238pow=8.5*math.pow(10,-9)
u235pow=6*math.pow(10,-8)
th232pow=2.6*math.pow(10,-9)
k40pow=5.6*math.pow(10,-9)
k40is=0.0001
u235is=0.992
u238is=0.007
uab=2.8/mil
thab=10.7/mil
kab=0.023
upow=u238pow*uab*u235is*earthmass+u235pow*uab*u235is*earthmass
thpow=th232pow*thab*1*earthmass
kpow=k40pow*kab*k40is*earthmass
radpow=(upow+thpow+kpow)
earthtemp=288
spacetemp=0
bolt=5.67*math.pow(10,-8)
hr=bolt*(earthtemp*earthtemp*earthtemp)
emis=0.61
hr=emis*hr
earthar=509*mil*mil
qr=hr*earthtemp
eh=qr*earthar
pctrad=radpow/eh
toteart=earthtemp*4
latentearth=earthspecheat*earthmass*toteart
ratetr=eh/latentearth
secsto=1/ratetr
year=60*60*24*365
irof=7.5*math.pow(10,5)
coremass=9.8*math.pow(10,25)
elatent=irof*coremass
k=0.6*math.pow(10,-6)
dept=math.sqrt(k*time)

