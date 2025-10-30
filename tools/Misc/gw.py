mspe=200*17*(10**.4)
print("mach",mspe/200)
fe=45e6
gr=10
frr=fe/gr
print(frr/1000,"range km")
lat=1e-3
ls=lat*mspe
msi=1
ma=msi**2
wam=1000
ej=5e6
meh=ej*wam
ki=10e6
kp=meh/ki
ks=(kp/ma)**(1/3)
odds=ks/ls
print("interxep odd",odds)