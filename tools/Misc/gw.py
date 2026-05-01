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
print(r,"latency")
print(r*1e9,"nanoseconds")
