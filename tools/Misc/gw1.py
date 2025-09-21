import sympy as sp

# Define constants symbolically
pi = sp.pi
phi = sp.GoldenRatio

# Step 1: alpha_fs and alpha (symbolic)
alpha_fs = (-6 + 4*pi)**(-phi**2)
alpha = (-6 + 4*pi)**(phi**2)

# Step 2: symbolic prefactor for getearth
av = ((alpha**phi)**7)/3
avogadro = sp.Rational('6.02214076e23')  # Avogadro number
f_factor = (av*3)*(alpha**phi)*8 / avogadro / 1000

# Step 3: full symbolic getearth expression
getearth_symbolic = f_factor * av / 6 / (1 + 1/(16 + sp.Rational(1, 22)/10))

# Step 4: evaluate numerically
getearth_numeric = getearth_symbolic.evalf()
prefactor_numeric = f_factor.evalf()

# Step 5: real Earth mass
actual_earth_mass = 5.9722e24  # kg

# Step 6: percent error as fraction of 1/alpha
fraction_of_inv_alpha =( (getearth_numeric / actual_earth_mass) / (1/alpha)/alpha)+(1/alpha)-(1/alpha/(1.25+(4+(1-1/(38-1/(4/(2.8+1/(17-1/(32-1/(1/(2+8/9)))))))))*(1/alpha)))

print("Numeric getearth:", getearth_numeric)
print("Actual Earth mass:", actual_earth_mass)
print("Error as fraction of 1/alpha:", fraction_of_inv_alpha.evalf())