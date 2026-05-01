ald=2.5e-10
c=3e8
alh=5
alc=660
als=900
aldd=2700
dia=ald
vol=dia**3
ma=vol*aldd
hc=ma*als*alc
apm=alc*dia*dia*alh
ev=1.6e-19
r=apm/ev
print(r,"ev rate per s")
r=hc/apm
print(r*1e6,"microseconds")
rr=r
spe=1/(c/ald)
fo=rr/spe
alm=5e-9
evm=ev/(c**2)
bm=1.38e-23
almm=4.5e-26
tt=273
vt=((3*bm*tt)/almm)**.5
tik=alm/vt
ue=(ev*tik)/evm
rat=c/vt
rat**=(1/2)
te=r/rat
print(te*1e9,"nanoseconds damped surface delay")
print(ue,"ideal electron mobility m2/vs")
avta=.0012
print("actual aluminum mobikity",avta)
cro=c/ald
ar=ald*ald
fall=(ar)*cro
ue/=fall
avta/=fall
phi=(1+5**.5)/2
print(ue,avta,"in units of atom crossing rate")
ue**=(1/3)
print(ue/138/phi,"normed")
lins=avta/ald
alcc=1.81e29
neu=alcc*ev*avta
neu=1/neu
corr=12.6
neu*=corr
print(neu,"resistivity of standard aluminum ohm m")
rel=r/21
print(rel*1e6,"microseconds relaxation aluminun")
perm=8.854e-12
diel=10
cap=diel*perm*ar
cap/=ald
res=neu*(ald/ar)
to=res*cap
print(to,"rc time constant one atom")

