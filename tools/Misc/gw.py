import numpy as np
import math

# Constants
G = 6.67430e-11  # gravitational constant (m^3 kg^-1 s^-2)
mass_sun = 1.989e30  # kg
mass_venus = 4.867e24  # kg
mass_mercury = 3.301e23  # kg

# Orbital parameters
AU = 1.496e11  # meters
r_mercury = 0.387 * AU  # m
r_venus = 0.723 * AU  # m

# Orbital velocities assuming circular orbits
v_mercury = np.sqrt(G * mass_sun / r_mercury)
v_venus = np.sqrt(G * mass_sun / r_venus)

# Time step and simulation time (one synodic period ≈ 144 days)
dt = 60  # seconds
days = 144
T = days * 24 * 3600
steps = int(T / dt)

far=r_mercury+r_venus
near=r_venus-r_mercury
top=G*mass_mercury*mass_venus
max=top/(near*near)
min=top/(far*far)
maxac=max/mass_mercury
minac=min/mass_mercury
dur=60*60*24*365*100
maxt=maxac*dur
maxd=(maxt/2)*dur
mint=minac*dur
mind=(mint/2)*dur
maxd=math.sqrt(maxd)
mind=math.sqrt(mind)

arc=180
oarc=AU/arc
arcs=oarc/3600
maxp=maxd/arcs
minp=mind/arcs
av=(maxp+minp)/2
print(av)

