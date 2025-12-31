import math

def iron_screen_size(rho, mu, v, L_cell=None):
    """
    Estimate the maximum pore/grid size for an iron screen in a molten salt cell.
    
    Parameters:
    rho : float - melt density (kg/m^3)
    mu  : float - dynamic viscosity (Pa.s)
    v   : float - characteristic fluid velocity (m/s)
    L_cell : float or None - optional characteristic cell length (m)
    
    Returns:
    L_max : float - maximum grid/pore size (m)
    """
    # Reynolds number criterion: Re << 1 for laminar flow
    # Approximate maximum characteristic size to suppress convection:
    L_max = mu / (rho * v)
    
    # Optionally limit by cell size
    if L_cell is not None:
        L_max = min(L_max, L_cell)
    
    return L_max

# Example values
rho = 1800      # kg/m^3 (molten salt density)
mu = 0.05       # Pa.s (viscosity)
v = 0.001       # m/s (fluid velocity)
L_cell = 0.05   # 5 cm characteristic dimension of the cell

L_max = iron_screen_size(rho, mu, v, L_cell)
print(f"Maximum iron grid spacing (m): {L_max:.3e}")
print(f"Maximum iron grid spacing (mm): {L_max*1000:.2f}")