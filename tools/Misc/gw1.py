import math

startuse=600_000
pct=.002
tot=startuse/pct
pc1=pct
months=12
rate=1.08
clock=6
peruse=(1/3)
pb=peruse
de=0
for i in range(84):
	print("year ",(i/12)+2025)
	pct*=rate
	peruse=pb+(pct**clock)
	if(peruse>1):
		peruse=1
	f=peruse**clock
	print(f)
	det=pct*f*tot
	de+=det
	print(de/1_000,"k")
	
	
	