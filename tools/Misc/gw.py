import math

# -----------------------------
# Silicon thermal diffusivity
# -----------------------------
alpha_si = 9e-5  # m^2/s (thermal diffusivity of silicon)

# -----------------------------
# Feature definition (5nm-class logic feature)
# -----------------------------
feature_size_m = 1e-3# 20 nm lateral
feature_depth_m = 30e-9  # 30 nm etch depth

feature_volume = feature_size_m**2 * feature_depth_m

# -----------------------------
# Energy per feature (from your earlier scaling)
# -----------------------------
# previously derived: ~1e-5 J per feature (you used this)
E_feature = ((feature_size_m**2)/.1)*3000

# -----------------------------
# Convert energy → temperature rise
# -----------------------------
silicon_density = 2330
silicon_cp = 700

feature_mass = feature_volume * silicon_density
feature_heat_capacity = feature_mass * silicon_cp

delta_T_feature = E_feature / feature_heat_capacity

# -----------------------------
# Cooling by thermal diffusion (KEY FIX)
# -----------------------------
# characteristic relaxation time
tau_diffusion = feature_size_m**2 / alpha_si

# time to ~equilibrium (~95%)
t_relax = 3 * tau_diffusion

# -----------------------------
# Gas effect (ONLY perturbation term)
# -----------------------------
# helium vs argon does NOT control cooling at feature scale
# but we include tiny perturbation factors

helium_factor = 0.98
argon_factor  = 1.02

t_he = t_relax * helium_factor
t_ar = t_relax * argon_factor

# -----------------------------
# Atomic scale normalization
# -----------------------------
avogadro = 6.022e23
si_atomic_mass = 28.085

feature_moles = (feature_mass * 1000) / si_atomic_mass
feature_atoms = feature_moles * avogadro

energy_per_atom = E_feature / feature_atoms

# -----------------------------
# Output
# -----------------------------
print("=== PER-FEATURE 5nm ETCH MODEL ===")

print(f"Feature volume (m^3): {feature_volume:.3e}")
print(f"Feature heat capacity (J/K): {feature_heat_capacity:.3e}")
print(f"Energy per feature (J): {E_feature:.3e}")
print(f"ΔT per feature (no diffusion model): {delta_T_feature:.2f} K")

print("\n--- Thermal diffusion ---")
print(f"Relaxation time (Si diffusion): {tau_diffusion:.3e} s")
print(f"Effective equilibration time: {t_relax:.3e} s")

print("\n--- Gas perturbation (NOT dominant) ---")
print(f"Helium time: {t_he:.3e} s")
print(f"Argon time: {t_ar:.3e} s")

print("\n--- Atomic scale ---")
print(f"Atoms per feature: {feature_atoms:.3e}")
print(f"Energy per atom: {energy_per_atom:.3e} J")
bc=1.38e-23
vt=3*bc*delta_T_feature/4.66e-26
vt**=.5
ti=feature_size_m/vt
ht=t_he/ti
at=t_ar/ti
print("helium argon",ht,at)
condh=.15
conda=.02
enp=E_feature/delta_T_feature
tim=enp/condh
ag=enp/conda
print("helium time to leave",tim)
print("argon",ag)
print("he ag",tim/ti,ag/ti)