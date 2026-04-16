import numpy as np

# ----------------------------
# Material parameters
# ----------------------------
rho = 7800
L_v = 6e6        # effective vaporization energy (J/m^3 scale lumped)
Tm = 1800

# ----------------------------
# Laser parameters
# ----------------------------
P_avg = 1.0
eta = 0.3
w = 0.5e-3

# femtosecond-like pulses
pulse_width = 100e-15
f = 1e6
duty = pulse_width * f

P_peak = P_avg / duty * eta

# ----------------------------
# Plasma threshold model (simplified)
# ----------------------------
I_plasma = 1e12  # W/m^2 threshold scale (order of magnitude)

# ----------------------------
# State variables
# ----------------------------
T = np.ones(100) * 300
mass_removed = np.zeros(100)

# spatial grid
R = 5e-3
r = np.linspace(0, R, 100)

gauss = np.exp(-2 * r**2 / w**2)
gauss /= np.trapz(gauss * 2*np.pi*r, r)

dt = 1e-13
Nt = 20000

for n in range(Nt):
    t = n * dt

    # pulse
    if (t % (1/f)) < pulse_width:
        I = P_peak * gauss
    else:
        I = np.zeros_like(r)

    for i in range(len(r)):

        # ----------------------------
        # Plasma regime trigger
        # ----------------------------
        if I[i] > I_plasma:

            # energy goes into ionization + ejection, not heating
            ablation_rate = (I[i] - I_plasma) * dt / L_v
            mass_removed[i] += ablation_rate

            # clamp temperature (energy leaves system)
            T[i] = Tm

        else:
            # normal heating (simplified)
            T[i] += I[i] * dt / (rho * 500)