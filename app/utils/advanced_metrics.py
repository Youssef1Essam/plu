"""
Advanced Metrics Calculation

Additional product-level metrics for enhanced risk assessment.
"""

from typing import Dict, Tuple
from app.physics.dispersion_coeffs import compute_sigma_y


def calculate_impact_width(stability_class: str, peak_distance: float) -> float:
    """
    Calculate lateral spread width at peak concentration distance.
    
    Impact width = 4 * σy (covers ~95% of plume width)
    
    Args:
        stability_class: Atmospheric stability class (A-F)
        peak_distance: Distance where peak concentration occurs (m)
    
    Returns:
        float: Impact width in meters
    """
    if peak_distance <= 0:
        return 0.0
    
    sigma_y = compute_sigma_y(stability_class, peak_distance)
    impact_width = 4 * sigma_y  # 2 standard deviations on each side
    
    return impact_width


def calculate_time_to_impact(impact_distance: float, wind_speed: float) -> float:
    """
    Calculate time for pollutants to reach impact distance.
    
    Time = distance / wind_speed
    
    Args:
        impact_distance: Distance to impact zone (m)
        wind_speed: Wind speed (m/s)
    
    Returns:
        float: Time in minutes
    """
    if impact_distance <= 0 or wind_speed <= 0:
        return 0.0
    
    time_seconds = impact_distance / wind_speed
    time_minutes = time_seconds / 60.0
    
    return time_minutes


def calculate_uncertainty_range(
    base_concentration: float,
    wind_speed: float,
    compute_concentration_func,
    **kwargs
) -> Tuple[float, float]:
    """
    Calculate concentration uncertainty range due to wind speed variability.
    
    Recomputes concentration with wind_speed * 0.8 and wind_speed * 1.2
    to estimate uncertainty range.
    
    Args:
        base_concentration: Baseline concentration
        wind_speed: Nominal wind speed (m/s)
        compute_concentration_func: Function to compute concentration
        **kwargs: Other parameters for concentration calculation
    
    Returns:
        Tuple[float, float]: (min_concentration, max_concentration)
    """
    # Lower wind speed → higher concentration
    wind_low = wind_speed * 0.8
    conc_high = compute_concentration_func(u=wind_low, **kwargs)
    
    # Higher wind speed → lower concentration
    wind_high = wind_speed * 1.2
    conc_low = compute_concentration_func(u=wind_high, **kwargs)
    
    return (conc_low, conc_high)


def assess_population_risk(location_type: str, impact_distance: float) -> Dict[str, str]:
    """
    Assess population risk based on location type and impact distance.
    
    Args:
        location_type: Type of location (industrial, urban, rural)
        impact_distance: Distance of impact (m)
    
    Returns:
        Dict with population_risk field if applicable
    """
    result = {}
    
    if location_type == "urban" and impact_distance > 1000:
        result["population_risk"] = "May affect populated areas"
    
    return result
