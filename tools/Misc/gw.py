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
print(ue,"ideal electron mobility m2/vs")
avta=.01
print("actual aluminum mobikity",avta)
cro=c/ald
all=(ald*ald)*cro
ue/=all
avta/=all
phi=(1+5**.5)/2
print(ue,avta,"in units of atom crossing rate")
ue**=(1/3)
print(ue/138/phi,"normed")
