mol=6e26
alt=7000
phi = (1 + 5**0.5) / 2
vol=alt**(3*phi)
amount=1e5
side=amount**(1/3)
print("salt cube side length meters",side,"atltirude",alt)
saltvol=amount
volr=vol/saltvol
print("number of interactions",volr)
waterk=2e9
raiseearth1c=5e21
rat=raiseearth1c/waterk
print("ratio of energy in salt to necessary",volr/rat)
print("95% loss occurs over year because average cloud life of 20 days is 5% of year")
