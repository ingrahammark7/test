kps=1
s=100
ts=200
dr=[]
import random
for i in range(10_000):
	dr.append(i)
for i in range(ts):
	tl=[]
	if(len(dr)<2):
		print("drones dead affer",i)
		break
	for j in range(s*kps):
		r=random.randint(1,len(dr))
		tl.append(r)
	dl=list(set(tl))
	for j in dl:
		dr.pop()
	