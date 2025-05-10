import math

dof=6
eff=2
recf=dof*eff
recyc=recf*recf
humpower=10000
airpower=recyc*humpower
mil=1000000
print("humans provide energy to planes ",airpower/mil)
englength=10
hvl=0.1
hvls=englength/hvl
hvls=math.pow(hvls,.33)
print("total ",hvls*airpower/mil)
fuelenperkg=36000000
missileweightkg=200
misfuel=fuelenperkg*missileweightkg/10
speed=100
airdenskgm3=1
misfrontm2=0.05
airfrontm2=10
airpersecair=airfrontm2*airdenskgm3*speed
mispersecair=misfrontm2*airdenskgm3*speed
print("aircraft moves ", airpersecair)
print("mis moges ",mispersecair)
airmass=10000
airpercentair=airpersecair/airmass
mispercentair=mispersecair/missileweightkg
print("relative air ",airpercentair)
print("relatigr mis ",mispercentair)
speedf=speed*speed*.5
airke=speedf*airmass
miske=speedf*missileweightkg
airloss=airpercentair*airke
misloss=miske*mispercentair
print("air power ",airloss/mil)
print("mis power ",misloss/mil)
airtemp=1000
g=10
buoyantacceleration=airtemp*airmass*g
mistemp=misfuel/1000/missileweightkg
print("mistemp ",mistemp)
alt=10000
gain=alt*g
misgain=missileweightkg*gain*2
climbtime=alt/speed*2
print("per clomb ",misgain)
numc=misgain/misfuel
print("num climbs ",numc)
print("time ",climbtime*numc)