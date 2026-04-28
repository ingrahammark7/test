import numpy as np

cr=126e-12
im=9.27e-23
em=1.25e-19
st=273
bc=1.38e-23
enf=1.5*bc*st
print(em/enf,"thuckness atoms")
si=(em/enf)*cr
print(si,"m equilibrium particle diameter at temp",st,"K")
