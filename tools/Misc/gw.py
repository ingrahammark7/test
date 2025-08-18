
import math

k=9e9
el=1e-19
r=1e-10
c=3e8
ec=1e7
ec2=ec/2
f=(k*ec2*ec2*el*el)/(r*(ec2**(1/3)))
print(f)
m=1e-30*ec
v=math.sqrt(f/m)
print(v/1e8)