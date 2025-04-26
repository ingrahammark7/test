import math

cmround=100
melting=700
hvlcm=1
airm3g=1000
aircm3g=airm3g/1000000
steelaircoefcm2=5/10000
roundld=10
roundfront=cmround*cmround
airperhit=roundfront*aircm3g
roundside=cmround*roundld*4
roundarea=roundfront+roundside
roundpower=steelaircoefcm2*roundarea
roundheat=steelaircoefcm2*melting*roundarea
airperhitpercm2=airperhit/roundfront
massperhitperms=roundheat/airperhitpercm2/roundfront
vper=math.sqrt(massperhitperms*1000)*2
print("fel ", vper)
tungdensgcm3=10
mass=cmround*cmround*roundld*tungdensgcm3/1000
ke=mass*vper*vper*.5
steeldensgcm3=7
steeltens=2000000000
steeltenscm3=steeltens/1000*steeldensgcm3
penarea=steeltenscm3*roundfront
numpens=ke/penarea
lenn=numpens*10
print("mm rha ",lenn)
fac=cmround/hvlcm
fac=fac**2**1.618
lenn=lenn*fac
print("toa ", lenn)
basevol=hvlcm*roundfront*tungdensgcm3/1000*steeltens
print("kci ", basevol, "ke ", ke, " rst ",basevol/ke)