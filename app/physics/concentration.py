import math

def compute_concentration(q: float, u: float, sy: float, sz: float, y: float, z: float, h: float) -> float:
    """
    Compute pollutant concentration C(x, y, z) using the Gaussian Plume Model.
    C(x,y,z) = (Q / (2π u σy σz)) * 
               exp(-y^2 / (2σy^2)) * 
               [exp(-(z-H)^2 / (2σz^2)) + exp(-(z+H)^2 / (2σz^2))]
    """
    # Pre-calculate terms to improve readability
    main_term = q / (2 * math.pi * u * sy * sz)
    crosswind_term = math.exp(-(y**2) / (2 * (sy**2)))
    
    # Vertical terms (including ground reflection)
    term_z_minus_h = math.exp(-((z - h)**2) / (2 * (sz**2)))
    term_z_plus_h = math.exp(-((z + h)**2) / (2 * (sz**2)))
    
    vertical_term = term_z_minus_h + term_z_plus_h
    
    concentration = main_term * crosswind_term * vertical_term
    return concentration
