import numpy as np
import math

c=3e8
n=1e100
ev=1e-19
mp=1e6
mi=n*ev
ref=.001
to=mi/ref
ar=to/mp
dis=ar**.5
vol=dis**3

cr=1e-60         
vols=cr**3       
volm=vol/vols

cop=c/cr
cops=cop*n
cops*=n
re=volm/cops

print("chamber at watts ",mi," collides distance ",cr,"in seconds",re,"wall length",dis)