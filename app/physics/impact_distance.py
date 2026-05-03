"""
Impact Distance Calculation Module

Computes how far pollution spreads by simulating concentration
along the downwind axis until it drops below threshold.
"""

from app.physics.dispersion_coeffs import compute_sigma_y, compute_sigma_z
from app.physics.concentration import compute_concentration
from app.utils.constants import THRESHOLD_LOW, IMPACT_DISTANCE_MAX, IMPACT_DISTANCE_STEP


def compute_impact_distance(
    q: float,
    u: float,
    h_eff: float,
    stability_class: str,
    threshold: float = THRESHOLD_LOW
) -> tuple[float, float, float]:
    """
    Compute impact distance, peak concentration, and peak distance.
    
    Simulates concentration along downwind axis (x) at ground level (z=0, y=0)
    until concentration drops below threshold.
    
    Args:
        q: Emission rate (g/s)
        u: Wind speed (m/s)
        h_eff: Effective stack height (m)
        stability_class: Atmospheric stability class (A-F)
        threshold: Concentration threshold (g/m³)
    
    Returns:
        tuple: (impact_distance_meters, peak_concentration, peak_distance_meters)
    """
    peak_concentration = 0.0
    peak_distance = 0.0
    impact_distance = 0.0
    found_above_threshold = False
    
    # Simulate along downwind axis
    x = IMPACT_DISTANCE_STEP  # Start at first step (avoid x=0)
    
    while x <= IMPACT_DISTANCE_MAX:
        # Compute dispersion coefficients at this distance
        sy = compute_sigma_y(stability_class, x)
        sz = compute_sigma_z(stability_class, x)
        
        # Compute concentration at ground level, centerline (y=0, z=0)
        conc = compute_concentration(q, u, sy, sz, y=0.0, z=0.0, h=h_eff)
        
        # Track peak concentration and its location
        if conc > peak_concentration:
            peak_concentration = conc
            peak_distance = x
        
        # Update impact distance if above threshold
        if conc >= threshold:
            impact_distance = x
            found_above_threshold = True
        else:
            # Once below threshold after finding values above it, we can stop
            if found_above_threshold:
                break
        
        x += IMPACT_DISTANCE_STEP
    
    # If peak concentration never exceeded threshold, impact distance is 0
    # (negligible impact)
    if not found_above_threshold:
        impact_distance = 0.0
    
    return impact_distance, peak_concentration, peak_distance
