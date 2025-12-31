import math

def separator_size_range(rho, mu, v, D, t_rxn, gamma=None, deltaP_hydro=None):
    """
    Calculate approximate separator/pore size range.
    
    Parameters:
    rho : float - melt density (kg/m^3)
    mu : float - dynamic viscosity (Pa.s)
    v   : float - characteristic fluid velocity (m/s)
    D   : float - ionic diffusion coefficient (m^2/s)
    t_rxn : float - chemical reaction timescale (s)
    gamma : float or None - surface tension (N/m) for capillary effect
    deltaP_hydro : float or None - hydrostatic pressure (Pa)
    
    Returns:
    L_min : float - minimum grid/pore size (m)
    L_max : float - maximum grid/pore size (m)
    """
    # Diffusion vs reaction (lower bound)
    L_min = math.sqrt(D * t_rxn)
    
    # Convection constraint (upper bound)
    L_Re = mu / (rho * v)           # Re << 1
    L_Pe = D / v                    # Pe << 1
    L_max = min(L_Re, L_Pe)
    
    # Optional: capillary effect for ceramic
    if gamma is not None and deltaP_hydro is not None:
        L_cap = 2 * gamma / deltaP_hydro
        L_max = min(L_max, L_cap)
    
    return L_min, L_max

# Example usage with typical conceptual numbers
rho = 1800      # kg/m^3 (molten salt density)
mu = 0.05       # Pa.s (molten salt viscosity)
v = 0.001       # m/s (fluid velocity)
D = 1e-9        # m^2/s (ionic diffusion coefficient)
t_rxn = 1e-3    # s (reaction timescale)
gamma = 0.2     # N/m (surface tension)
deltaP_hydro = 100  # Pa (hydrostatic pressure)

L_min, L_max = separator_size_range(rho, mu, v, D, t_rxn, gamma, deltaP_hydro)

print(f"Minimum pore/grid size (m): {L_min:.3e}")
print(f"Maximum pore/grid size (m): {L_max:.3e}")